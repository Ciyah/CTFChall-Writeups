#!/usr/bin/env python3
import json
import sys

from solve import N, division_tail, parse_groups


def scale(expr, amount):
    a, b = expr
    factor = 1 << amount
    return a * factor, b * factor


def plus(left, right):
    return left[0] + right[0], left[1] + right[1]


def possible_v(v):
    """Can a*w+b equal N for a positive odd integer w?"""
    a, b = v
    if b > N:
        return False
    if a == 0:
        return b == N
    remainder = N - b
    return remainder >= a and remainder % a == 0 and ((remainder // a) & 1)


def loose_v(v):
    # A partial reverse path can only increase both nonnegative coefficients.
    a, b = v
    return b <= N and a <= N - b


def recover_denominators(sample):
    groups = parse_groups(division_tail(sample["trace"]))
    # Expressions are a*w+b, where w is the unknown non-unit terminal value.
    # Include both possible terminal orientations.
    states = {((0, 1), (1, 0), -1), ((1, 0), (0, 1), -1)}

    # branch is the side reduced by the preceding subtraction: 1=u, 0=v.
    # First choose it to undo the shifts in the terminal group.
    initial = set()
    terminal_shifts = len(groups[-1])
    for u, v, _ in states:
        for branch in (0, 1):
            if branch:
                u2, v2 = scale(u, terminal_shifts), v
            else:
                u2, v2 = u, scale(v, terminal_shifts)
            if loose_v(v2):
                initial.add((u2, v2, branch))
    states = initial

    for j in range(len(groups) - 2, -1, -1):
        out = set()
        for u, v, branch_j in states:
            # Undo subtraction j. Positivity automatically makes the forward
            # comparison choose this same side.
            if branch_j:
                before_u, before_v = plus(u, v), v
            else:
                before_u, before_v = u, plus(v, u)

            shifts = len(groups[j])
            if j == 0:
                candidates = (1,)  # the initial denominator is shifted
            else:
                candidates = (0, 1)  # branch j-1, also the shifted side
            for previous in candidates:
                if previous:
                    u2, v2 = scale(before_u, shifts), before_v
                else:
                    u2, v2 = before_u, scale(before_v, shifts)
                if loose_v(v2):
                    out.add((u2, v2, previous))
        states = out
        if j % 20 == 0 or j < 5:
            print(f"reverse j={j} states={len(states)}", file=sys.stderr, flush=True)

    answers = set()
    for u, v, _ in states:
        if not possible_v(v):
            continue
        a, b = v
        if a == 0:
            continue
        w = (N - b) // a
        denominator = u[0] * w + u[1]
        if 0 < denominator < N * N:
            answers.add(denominator)
    return answers


if __name__ == "__main__":
    with open(sys.argv[1] if len(sys.argv) > 1 else "sample.json", encoding="ascii") as f:
        sample = json.load(f)
    for value in sorted(recover_denominators(sample)):
        print(hex(value))
