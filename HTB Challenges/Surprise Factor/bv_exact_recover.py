#!/usr/bin/env python3
"""Recover the masked division denominator with a bounded-memory BV model."""

import argparse
import json

import z3

from fast_recover import N, division_tail, parse_groups


def recover(sample, timeout_ms, memory_mb):
    groups = parse_groups(division_tail(sample["trace"]))
    s_value = int(sample["s"], 0)

    # D is below N^2 (512 bits).  The 768-bit product s*D cannot overflow.
    d_width, product_width, x_width = 512, 768, 258
    z3.set_param("memory_max_size", memory_mb)
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=timeout_ms)

    denominator = z3.BitVec("denominator", d_width)
    solver.add(z3.UGT(denominator, z3.BitVecVal(1 << 500, d_width)))
    solver.add(z3.ULT(denominator, z3.BitVecVal(N * N, d_width)))

    wide_d = z3.ZeroExt(product_width - d_width, denominator)
    numerator = z3.BitVec("numerator", 256)
    quotient = z3.BitVec("quotient", d_width)
    solver.add(z3.ULT(numerator, z3.BitVecVal(N, 256)))
    solver.add(z3.ULT(quotient, z3.BitVecVal(s_value * N, d_width)))
    # All terms are strictly below 2^768, so this BV equality is also an
    # ordinary integer equality: s*D = q*N + numerator.
    solver.add(
        wide_d * z3.BitVecVal(s_value, product_width)
        == z3.ZeroExt(product_width - d_width, quotient)
        * z3.BitVecVal(N, product_width)
        + z3.ZeroExt(product_width - 256, numerator)
    )

    u = denominator
    v = z3.BitVecVal(N, d_width)
    x1 = z3.ZeroExt(x_width - 256, numerator)
    x2 = z3.BitVecVal(0, x_width)
    n_x = z3.BitVecVal(N, x_width)
    previous_branch = None

    for group_index, parity_bits in enumerate(groups):
        side_u = z3.BoolVal(True) if group_index == 0 else previous_branch
        for shift_index, parity in enumerate(parity_bits):
            selected_u = z3.If(side_u, u, v)
            selected_x = z3.If(side_u, x1, x2)
            solver.add(z3.Extract(0, 0, selected_u) == 0)
            solver.add(z3.Extract(0, 0, selected_x) == parity)

            next_u = z3.BitVec(f"u_{group_index}_{shift_index}", d_width)
            next_v = z3.BitVec(f"v_{group_index}_{shift_index}", d_width)
            next_x1 = z3.BitVec(f"x1_{group_index}_{shift_index}", x_width)
            next_x2 = z3.BitVec(f"x2_{group_index}_{shift_index}", x_width)
            adjusted_x = (selected_x + (n_x if parity else 0)) >> 1
            solver.add(next_u == z3.If(side_u, z3.LShR(u, 1), u))
            solver.add(next_v == z3.If(side_u, v, z3.LShR(v, 1)))
            solver.add(next_x1 == z3.If(side_u, adjusted_x, x1))
            solver.add(next_x2 == z3.If(side_u, x2, adjusted_x))
            u, v, x1, x2 = next_u, next_v, next_x1, next_x2

        solver.add(z3.Extract(0, 0, u) == 1)
        solver.add(z3.Extract(0, 0, v) == 1)
        if group_index == len(groups) - 1:
            solver.add(z3.Or(u == 1, v == 1))
            break

        branch = z3.Bool(f"subtract_u_{group_index}")
        solver.add(branch == z3.UGE(u, v))
        next_u = z3.BitVec(f"u_after_{group_index}", d_width)
        next_v = z3.BitVec(f"v_after_{group_index}", d_width)
        next_x1 = z3.BitVec(f"x1_after_{group_index}", x_width)
        next_x2 = z3.BitVec(f"x2_after_{group_index}", x_width)
        solver.add(next_u == z3.If(branch, u - v, u))
        solver.add(next_v == z3.If(branch, v, v - u))
        solver.add(next_x1 == z3.If(branch, x1 - x2, x1))
        solver.add(next_x2 == z3.If(branch, x2, x2 - x1))
        u, v, x1, x2 = next_u, next_v, next_x1, next_x2
        previous_branch = branch

    print(f"groups={len(groups)} shifts={sum(map(len, groups))}", flush=True)
    result = solver.check()
    print(result, flush=True)
    if result != z3.sat:
        print(solver.reason_unknown(), flush=True)
        return None
    value = solver.model().eval(denominator).as_long()
    print(hex(value), flush=True)
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sample", nargs="?", default="sample.json")
    parser.add_argument("--timeout-ms", type=int, default=300_000)
    parser.add_argument("--memory-mb", type=int, default=1400)
    args = parser.parse_args()
    with open(args.sample, encoding="ascii") as source:
        recover(json.load(source), args.timeout_ms, args.memory_mb)
