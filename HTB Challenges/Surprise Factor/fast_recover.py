#!/usr/bin/env python3
import json
import sys

N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551


def division_tail(trace):
    marker = max(index for index, symbol in enumerate(trace) if symbol == "y")
    return trace[marker + 1:]


def parse_groups(tail):
    groups = []
    shifts = []
    index = 0
    while index < len(tail):
        if tail[index:index + 2] == ["s", "s"]:
            groups.append(shifts)
            shifts = []
            index += 2
        elif tail[index:index + 2] == ["h", "h"]:
            shifts.append(0)
            index += 2
        elif tail[index:index + 3] == ["h", "a", "h"]:
            shifts.append(1)
            index += 3
        else:
            raise ValueError(f"unrecognized division trace at {index}: {tail[index:index+8]}")
    groups.append(shifts)
    return groups


def feasible(lo, hi, residue, bits):
    modulus = 1 << bits
    first = lo + ((residue - lo) % modulus)
    return first <= hi


def impose_bit(state, expr, bit):
    lo, hi, residue, bits, u, v, side = state
    a, b, shift = expr
    need_bits = shift + 1
    modulus = 1 << need_bits
    target = bit << shift
    if bits >= need_bits:
        candidates = [residue]
        out_bits = bits
    else:
        candidates = [residue + (offset << bits) for offset in range(1 << (need_bits - bits))]
        out_bits = need_bits
    output = []
    for candidate in candidates:
        if (a * candidate + b * N - target) % modulus:
            continue
        candidate %= 1 << out_bits
        if feasible(lo, hi, candidate, out_bits):
            output.append((lo, hi, candidate, out_bits, u, v, side))
    return output


def difference(left, right):
    la, lb, ls = left
    ra, rb, rs = right
    common = max(ls, rs)
    return (la << (common - ls)) - (ra << (common - rs)), (lb << (common - ls)) - (rb << (common - rs)), common


def constrain_sign(state, expr, nonnegative):
    lo, hi, residue, bits, u, v, side = state
    a, b, _ = expr
    constant = b * N
    if a == 0:
        ok = constant >= 0 if nonnegative else constant < 0
        return state if ok else None
    # a*x + constant >= 0 (or < 0), with exact integer endpoints.
    if nonnegative:
        if a > 0:
            lo = max(lo, (-constant + a - 1) // a)
        else:
            hi = min(hi, (-constant) // a)
    else:
        if a > 0:
            hi = min(hi, (-constant - 1) // a)
        else:
            lo = max(lo, (-constant) // a + 1)
    if lo > hi or not feasible(lo, hi, residue, bits):
        return None
    return (lo, hi, residue, bits, u, v, side)


def recover(sample):
    groups = parse_groups(division_tail(sample["trace"]))
    # expression (A, B, t) means (A*d + B*N) / 2^t
    initial = (1 << 480, N * N - 1, 0, 0, (1, 0, 0), (0, 1, 0), True)
    states = [initial]
    for group_index, shifts in enumerate(groups):
        next_states = []
        for state in states:
            lo, hi, residue, bits, u, v, stored_side = state
            side_u = True if group_index == 0 else stored_side
            partial = [state]
            for _ in shifts:
                advanced = []
                for item in partial:
                    expr = item[4] if side_u else item[5]
                    for constrained in impose_bit(item, expr, 0):
                        values = list(constrained)
                        a, b, shift = expr
                        values[4 if side_u else 5] = (a, b, shift + 1)
                        advanced.append(tuple(values))
                partial = advanced
            for item in partial:
                odd_states = impose_bit(item, item[4], 1)
                odd_states = [z for x in odd_states for z in impose_bit(x, x[5], 1)]
                if group_index == len(groups) - 1:
                    next_states.extend(odd_states)
                    continue
                for odd in odd_states:
                    diff = difference(odd[4], odd[5])
                    for branch_u in (True, False):
                        signed = constrain_sign(odd, diff, branch_u)
                        if signed is None:
                            continue
                        values = list(signed)
                        if branch_u:
                            values[4] = diff
                        else:
                            values[5] = (-diff[0], -diff[1], diff[2])
                        values[6] = branch_u
                        next_states.append(tuple(values))
        states = next_states
        print(group_index, len(states), max((s[3] for s in states), default=0))
    answers = set()
    for state in states:
        lo, hi, residue, bits, u, v, side = state
        for a, b, shift in (u, v):
            if a == 0:
                continue
            numerator = (1 << shift) - b * N
            if numerator % a:
                continue
            value = numerator // a
            if lo <= value <= hi and value % (1 << bits) == residue:
                answers.add(value)
    return answers


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "sample.json"
    with open(path, encoding="ascii") as source:
        print([hex(x) for x in recover(json.load(source))])
