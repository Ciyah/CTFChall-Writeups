#!/usr/bin/env python3
import argparse
import json
import sys

from solve import N, division_tail, parse_groups


def undo_halves(x, parities):
    for parity in reversed(parities):
        x = 2 * x - parity * N
    return x


def recover(sample, max_terminal=65536, coefficient_bound=8, state_cap=2_000_000):
    s = int(sample["s"], 0)
    groups = parse_groups(division_tail(sample["trace"]))
    assert not groups[-1]
    last = len(groups) - 2
    bound = coefficient_bound * N

    states = set()
    offsets = range(-coefficient_bound, coefficient_bound + 1)
    for w in range(2, max_terminal + 1, 2):
        rw = (s * w) % N
        # If u=1, the final subtraction necessarily reduced v, and vice versa.
        for t1 in offsets:
            x_unit = s + t1 * N
            if abs(x_unit) > bound:
                continue
            for t2 in offsets:
                x_other = rw + t2 * N
                if abs(x_other) <= bound:
                    states.add((1, w, x_unit, x_other, 0))
                    states.add((w, 1, x_other, x_unit, 1))
    print(f"terminal states={len(states)}", file=sys.stderr)

    for j in range(last, -1, -1):
        out = set()
        for u, v, x1, x2, branch in states:
            # Undo subtraction j for both the operands and Bezout coefficients.
            if branch:
                u += v
                x1 += x2
            else:
                v += u
                x2 += x1
            if abs(x1) > bound or abs(x2) > bound:
                continue

            choices = (1,) if j == 0 else (0, 1)
            for previous in choices:
                if previous:
                    u2 = u << len(groups[j])
                    v2 = v
                    y1 = undo_halves(x1, groups[j])
                    y2 = x2
                else:
                    u2 = u
                    v2 = v << len(groups[j])
                    y1 = x1
                    y2 = undo_halves(x2, groups[j])
                if v2 <= N and u2 < N * N and abs(y1) <= bound and abs(y2) <= bound:
                    out.add((u2, v2, y1, y2, previous))
        states = out
        if len(states) > state_cap:
            raise RuntimeError(f"state cap exceeded at group {j}: {len(states)}")
        if j % 20 == 0 or j < 5:
            print(f"j={j} states={len(states)}", file=sys.stderr, flush=True)

    answers = set()
    for denominator, v, numerator, x2, _ in states:
        if v != N or x2 != 0 or not (0 <= numerator < N):
            continue
        if numerator != (s * denominator) % N:
            continue
        answers.add(denominator)
    return answers


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("sample", nargs="?", default="sample.json")
    p.add_argument("--max-terminal", type=int, default=65536)
    p.add_argument("--bound", type=int, default=8)
    p.add_argument("--cap", type=int, default=2_000_000)
    args = p.parse_args()
    with open(args.sample, encoding="ascii") as f:
        sample = json.load(f)
    for answer in sorted(recover(sample, args.max_terminal, args.bound, args.cap)):
        print(hex(answer))
