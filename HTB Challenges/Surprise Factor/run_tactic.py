#!/usr/bin/env python3
import sys
import z3

goal = z3.Goal()
goal.add(z3.parse_smt2_file(sys.argv[1]))
tactic = z3.Then(
    z3.Tactic("simplify"),
    z3.With(z3.Tactic("solve-eqs"), solve_eqs_max_occs=1000000),
    z3.Tactic("propagate-values"),
    z3.Tactic("qflia"),
)
print(tactic(goal))
