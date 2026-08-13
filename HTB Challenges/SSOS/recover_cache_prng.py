#!/usr/bin/env python3
from fractions import Fraction

from z3 import BitVec, LShR, Or, Solver, UGE, ULT, sat

SCORES = [
    85, 79, 86, 89, 93, 77, 96, 85, 73, 77, 77, 85, 93,
    72, 88, 88, 77, 70, 82, 84, 99, 89, 94, 73, 71, 94,
    99, 77, 82, 78, 99, 72, 97, 75, 90, 94, 97, 78, 75,
    96, 89, 92, 79, 79, 81, 84, 73, 73, 88, 76, 77, 99,
]
MASK = (1 << 64) - 1
DENOM = 1 << 52


def ceil_fraction(value):
    return -(-value.numerator // value.denominator)


def bounds(score):
    bucket = score - 70
    return (
        ceil_fraction(Fraction(bucket * DENOM, 31)),
        ceil_fraction(Fraction((bucket + 1) * DENOM, 31)),
    )


def forward_z3(s0, s1):
    x = s0
    new_s0 = s1
    x ^= x << 23
    x ^= LShR(x, 17)
    x ^= s1
    x ^= LShR(s1, 26)
    return new_s0, x


def forward(s0, s1):
    x = s0
    new_s0 = s1
    x ^= (x << 23) & MASK
    x ^= x >> 17
    x ^= s1
    x ^= s1 >> 26
    return new_s0, x & MASK


solver = Solver()
solver.set(timeout=300_000)
base_s0 = BitVec("base_s0", 64)  # state after transition 8
base_s1 = BitVec("base_s1", 64)
s0, s1 = base_s0, base_s1

# V8 fills cache[0..63] forward, then Math.random returns it backward.
# Calls 5..56 expose transitions 60..9, hence reverse the observations.
for score in reversed(SCORES):
    s0, s1 = forward_z3(s0, s1)
    mantissa = LShR(s0, 12)
    low, high = bounds(score)
    solver.add(UGE(mantissa, low), ULT(mantissa, high))

print(solver.check())
model = solver.model()
concrete_base = (model[base_s0].as_long(), model[base_s1].as_long())
print("state_after_t8", *(hex(x) for x in concrete_base))

s0, s1 = concrete_base
predicted_forward = []
for _ in SCORES:
    s0, s1 = forward(s0, s1)
    predicted_forward.append((s0 >> 12) * 31 // DENOM + 70)
print("scores_match", list(reversed(predicted_forward)) == SCORES)

# We are now at transition 60. Transitions 61, 62, 63, 64 were returned as
# calls 4, 3, 2, 1 respectively; the first call generated the password.
for _ in range(4):
    s0, s1 = forward(s0, s1)
password_integer = s0 >> 12
print("password_integer", password_integer)
print("password_double", password_integer / DENOM)

# Check whether the 128-bit state is unique under all collected constraints.
solver.add(Or(base_s0 != concrete_base[0], base_s1 != concrete_base[1]))
print("second_model", solver.check())
