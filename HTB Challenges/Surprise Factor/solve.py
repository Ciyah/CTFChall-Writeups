#!/usr/bin/env python3
import json
import sys

import z3

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


def recover_denominator(sample):
    s_value = int(sample["s"], 0)
    groups = parse_groups(division_tail(sample["trace"]))
    solver = z3.Solver()
    solver.set(threads=8)
    solver.set("arith.int_eq_branch", True)
    solver.set("theory_aware_branching", True)

    denominator = z3.Int("denominator")
    numerator = z3.Int("numerator")
    quotient = z3.Int("quotient")
    solver.add(denominator > 0, denominator < N * N)
    solver.add(numerator >= 0, numerator < N)
    solver.add(numerator == s_value * denominator - quotient * N)
    solver.add(quotient >= 0, quotient < s_value * N)

    u, v = denominator, z3.IntVal(N)
    x1, x2 = numerator, z3.IntVal(0)
    previous_branch = None

    for group_index, parity_bits in enumerate(groups):
        if group_index == 0:
            side_u = z3.BoolVal(True)
        else:
            side_u = previous_branch

        for shift_index, parity in enumerate(parity_bits):
            next_u = z3.Int(f"u_{group_index}_{shift_index}")
            next_v = z3.Int(f"v_{group_index}_{shift_index}")
            next_x1 = z3.Int(f"x1_{group_index}_{shift_index}")
            next_x2 = z3.Int(f"x2_{group_index}_{shift_index}")

            selected_value = z3.If(side_u, u, v)
            selected_x = z3.If(side_u, x1, x2)
            solver.add(selected_value % 2 == 0)
            solver.add(selected_x % 2 == parity)
            solver.add(next_u == z3.If(side_u, u / 2, u))
            solver.add(next_v == z3.If(side_u, v, v / 2))
            solver.add(next_u > 0, next_v > 0)
            adjusted_x = (selected_x + parity * N) / 2
            solver.add(next_x1 == z3.If(side_u, adjusted_x, x1))
            solver.add(next_x2 == z3.If(side_u, x2, adjusted_x))
            u, v, x1, x2 = next_u, next_v, next_x1, next_x2

        solver.add(u % 2 == 1, v % 2 == 1)

        if group_index == len(groups) - 1:
            solver.add(z3.Or(u == 1, v == 1))
            break

        branch = z3.Bool(f"subtract_u_{group_index}")
        solver.add(branch == (u >= v))
        next_u = z3.Int(f"u_after_{group_index}")
        next_v = z3.Int(f"v_after_{group_index}")
        next_x1 = z3.Int(f"x1_after_{group_index}")
        next_x2 = z3.Int(f"x2_after_{group_index}")
        solver.add(next_u == z3.If(branch, u - v, u))
        solver.add(next_v == z3.If(branch, v, v - u))
        solver.add(next_u > 0, next_v > 0)
        solver.add(next_x1 == z3.If(branch, x1 - x2, x1))
        solver.add(next_x2 == z3.If(branch, x2, x2 - x1))
        u, v, x1, x2 = next_u, next_v, next_x1, next_x2
        previous_branch = branch

    print(f"groups={len(groups)}, shifts={sum(map(len, groups))}", file=sys.stderr)
    if "--dump" in sys.argv:
        with open("constraints.smt2", "w", encoding="ascii") as output:
            output.write(solver.to_smt2())
        return 0
    if solver.check() != z3.sat:
        raise RuntimeError("division trace constraints are unsatisfiable")
    model = solver.model()
    value = model[denominator].as_long()
    # The trace should pin the input down uniquely.
    solver.add(denominator != value)
    unique = solver.check() == z3.unsat
    print(f"unique={unique}", file=sys.stderr)
    return value


def recover_from_shift_counts(sample):
    groups = parse_groups(division_tail(sample["trace"]))
    solver = z3.SolverFor("QF_LIA")
    denominator = z3.Int("simple_denominator")
    solver.add(denominator > 0, denominator < N * N)
    u, v = denominator, z3.IntVal(N)
    previous_branch = None
    for group_index, parity_bits in enumerate(groups):
        side_u = z3.BoolVal(True) if group_index == 0 else previous_branch
        for shift_index in range(len(parity_bits)):
            next_u = z3.Int(f"su_{group_index}_{shift_index}")
            next_v = z3.Int(f"sv_{group_index}_{shift_index}")
            solver.add(z3.If(side_u, u, v) % 2 == 0)
            solver.add(next_u == z3.If(side_u, u / 2, u))
            solver.add(next_v == z3.If(side_u, v, v / 2))
            u, v = next_u, next_v
        solver.add(u % 2 == 1, v % 2 == 1)
        if group_index == len(groups) - 1:
            solver.add(z3.Or(u == 1, v == 1))
            break
        branch = z3.Bool(f"simple_subtract_u_{group_index}")
        solver.add(branch == (u >= v))
        next_u = z3.Int(f"su_after_{group_index}")
        next_v = z3.Int(f"sv_after_{group_index}")
        solver.add(next_u == z3.If(branch, u - v, u))
        solver.add(next_v == z3.If(branch, v, v - u))
        u, v = next_u, next_v
        previous_branch = branch
    print(f"simple groups={len(groups)}, shifts={sum(map(len, groups))}", file=sys.stderr)
    if solver.check() != z3.sat:
        raise RuntimeError("shift-count constraints are unsatisfiable")
    value = solver.model()[denominator].as_long()
    solver.add(denominator != value)
    print(f"simple unique={solver.check() == z3.unsat}", file=sys.stderr)
    return value


def recover_bitvector(sample):
    groups = parse_groups(division_tail(sample["trace"]))
    width = 512
    denominator = z3.BitVec("bv_denominator", width)
    u, v = denominator, z3.BitVecVal(N, width)
    solver = z3.Solver()
    solver.add(z3.UGT(denominator, z3.BitVecVal(1 << 480, width)))
    solver.add(z3.ULT(denominator, z3.BitVecVal(N * N, width)))
    previous_branch = None
    for group_index, parity_bits in enumerate(groups):
        side_u = z3.BoolVal(True) if group_index == 0 else previous_branch
        for shift_index in range(len(parity_bits)):
            solver.add((z3.If(side_u, u, v) & 1) == 0)
            next_u = z3.BitVec(f"bu_{group_index}_{shift_index}", width)
            next_v = z3.BitVec(f"bv_{group_index}_{shift_index}", width)
            solver.add(next_u == z3.If(side_u, z3.LShR(u, 1), u))
            solver.add(next_v == z3.If(side_u, v, z3.LShR(v, 1)))
            u, v = next_u, next_v
        solver.add((u & 1) == 1, (v & 1) == 1)
        if group_index == len(groups) - 1:
            solver.add(z3.Or(u == 1, v == 1))
            break
        branch = z3.Bool(f"bv_subtract_u_{group_index}")
        solver.add(branch == z3.UGE(u, v))
        next_u = z3.BitVec(f"bu_after_{group_index}", width)
        next_v = z3.BitVec(f"bv_after_{group_index}", width)
        solver.add(next_u == z3.If(branch, u - v, u))
        solver.add(next_v == z3.If(branch, v, v - u))
        u, v = next_u, next_v
        previous_branch = branch
    print(f"bv groups={len(groups)}, shifts={sum(map(len, groups))}", file=sys.stderr)
    if solver.check() != z3.sat:
        raise RuntimeError("bit-vector constraints are unsatisfiable")
    value = solver.model()[denominator].as_long()
    solver.add(denominator != value)
    print(f"bv unique={solver.check() == z3.unsat}", file=sys.stderr)
    return value


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "sample.json"
    with open(path, encoding="ascii") as source:
        sample = json.load(source)
    if "--bv" in sys.argv:
        denominator = recover_bitvector(sample)
    elif "--simple" in sys.argv:
        denominator = recover_from_shift_counts(sample)
    else:
        denominator = recover_denominator(sample)
    print(hex(denominator))
