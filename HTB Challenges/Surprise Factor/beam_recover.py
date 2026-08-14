#!/usr/bin/env python3
import argparse
import json
import math
import sys

from solve import N, division_tail, parse_groups


def expected_maps(groups):
    # E[j][branch] = (a,b), expected final v = a*u+b*v from the
    # state immediately after subtraction j.
    maps = [{0: (1.0, 1.0), 1: (0.0, 1.0)}]
    for j in range(1, len(groups) - 1):
        level = {}
        factor = float(1 << len(groups[j]))
        for branch in (0, 1):
            total_a = total_b = 0.0
            # Undo subtraction j.
            # branch u: (u+v,v); branch v: (u,v+u)
            for previous in (0, 1):
                ea, eb = maps[j - 1][previous]
                if previous:  # scale u for group j
                    ea *= factor
                else:         # scale v for group j
                    eb *= factor
                if branch:
                    ca, cb = ea, ea + eb
                else:
                    ca, cb = ea + eb, eb
                total_a += ca * 0.5
                total_b += cb * 0.5
            level[branch] = total_a, total_b
        maps.append(level)
    return maps


def recover(sample, width, max_terminal):
    groups = parse_groups(division_tail(sample["trace"]))
    assert not groups[-1], "expected trace to end immediately after subtraction"
    maps = expected_maps(groups)
    last = len(groups) - 2

    # The non-unit terminal operand is even. The final subtraction side is
    # forced: it is the non-unit side, since the other operand was already 1.
    states = []
    for w in range(2, max_terminal + 1, 2):
        states.append((1, w, 0))  # u=1 => last subtraction reduced v
        states.append((w, 1, 1))  # v=1 => last subtraction reduced u

    logn = math.log2(N)
    for j in range(last, -1, -1):
        advanced = {}
        shifts = len(groups[j])
        factor = 1 << shifts
        for u, v, branch in states:
            if branch:
                u, v = u + v, v
            else:
                u, v = u, v + u
            if j == 0:
                u *= factor
                if v == N and u < N * N:
                    advanced[(u, v, 1)] = None
                continue
            for previous in (0, 1):
                u2, v2 = (u * factor, v) if previous else (u, v * factor)
                if v2 <= N and u2 < N * N:
                    advanced[(u2, v2, previous)] = None

        states = list(advanced)
        if j == 0:
            break
        if len(states) > width:
            ea0, eb0 = maps[j - 1][0]
            ea1, eb1 = maps[j - 1][1]
            def score(state):
                u, v, branch = state
                ea, eb = (ea1, eb1) if branch else (ea0, eb0)
                estimate = ea * u + eb * v
                return abs(math.log2(estimate) - logn)
            states.sort(key=score)
            states = states[:width]
        if j % 20 == 0 or j < 5:
            print(f"j={j} states={len(states)}", file=sys.stderr, flush=True)
    return {u for u, v, _ in states if v == N}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sample", nargs="?", default="sample.json")
    parser.add_argument("--width", type=int, default=200_000)
    parser.add_argument("--max-terminal", type=int, default=4096)
    args = parser.parse_args()
    with open(args.sample, encoding="ascii") as f:
        sample = json.load(f)
    for answer in sorted(recover(sample, args.width, args.max_terminal)):
        print(hex(answer))
