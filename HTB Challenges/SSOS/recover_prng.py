#!/usr/bin/env python3
from fractions import Fraction

from z3 import BitVec, LShR, Solver, UGE, ULT, sat

SCORES = [
    85, 79, 86, 89, 93, 77, 96, 85, 73, 77, 77, 85, 93,
    72, 88, 88, 77, 70, 82, 84, 99, 89, 94, 73, 71, 94,
    99, 77, 82, 78, 99, 72, 97, 75, 90, 94, 97, 78, 75,
    96, 89, 92, 79, 79, 81, 84, 73, 73, 88, 76, 77, 99,
]
MASK = (1 << 64) - 1
DENOM = 1 << 53


def ceil_fraction(value):
    return -(-value.numerator // value.denominator)


def bounds(score):
    bucket = score - 70
    low = ceil_fraction(Fraction(bucket * DENOM, 31))
    high = ceil_fraction(Fraction((bucket + 1) * DENOM, 31))
    return low, high


def forward_z3(s0, s1):
    x = s0
    new_s0 = s1
    x ^= x << 23
    x ^= LShR(x, 17)
    x ^= s1
    x ^= LShR(s1, 26)
    return new_s0, x


def undo_right(value, shift):
    result = value
    for amount in range(shift, 64, shift):
        result ^= value >> amount
    return result & MASK


def undo_left(value, shift):
    result = value
    for amount in range(shift, 64, shift):
        result ^= (value << amount) & MASK
    return result & MASK


def reverse_concrete(new_s0, new_s1):
    old_s1 = new_s0
    mixed = new_s1 ^ old_s1 ^ (old_s1 >> 26)
    after_left = undo_right(mixed, 17)
    old_s0 = undo_left(after_left, 23)
    return old_s0, old_s1


def forward_concrete(s0, s1):
    x = s0
    new_s0 = s1
    x ^= (x << 23) & MASK
    x ^= x >> 17
    x ^= s1
    x ^= s1 >> 26
    return new_s0, x & MASK


solver = Solver()
solver.set(timeout=300_000)
start_s0 = BitVec("start_s0", 64)
start_s1 = BitVec("start_s1", 64)
s0, s1 = start_s0, start_s1

for score in SCORES:
    s0, s1 = forward_z3(s0, s1)
    random = s0 + s1
    mantissa = LShR(random, 11)
    low, high = bounds(score)
    solver.add(UGE(mantissa, low), ULT(mantissa, high))

result = solver.check()
print(result)
if result != sat:
    raise SystemExit(1)

model = solver.model()
state_before_observed = (model[start_s0].as_long(), model[start_s1].as_long())
print("state_before_observed", *(hex(x) for x in state_before_observed))

# Earlier calls: generated student password, flag auto-score, and two test submissions.
s0, s1 = state_before_observed
for _ in range(4):
    s0, s1 = reverse_concrete(s0, s1)
state_before_password = (s0, s1)
password_s0, password_s1 = forward_concrete(*state_before_password)
password_integer = ((password_s0 + password_s1) & MASK) >> 11
print("state_before_password", *(hex(x) for x in state_before_password))
print("password_integer", password_integer)
print("password_double", password_integer / DENOM)

# Check the recovered model against every observed score.
s0, s1 = state_before_observed
predicted = []
for _ in SCORES:
    s0, s1 = forward_concrete(s0, s1)
    predicted.append((((s0 + s1) & MASK) >> 11) * 31 // DENOM + 70)
print("scores_match", predicted == SCORES)
