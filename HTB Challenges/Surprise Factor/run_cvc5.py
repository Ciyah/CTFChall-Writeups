#!/usr/bin/env python3
import argparse

import cvc5

parser_args = argparse.ArgumentParser()
parser_args.add_argument("file")
parser_args.add_argument("--int-bv", type=int, default=0)
parser_args.add_argument("--miplib", action="store_true")
args = parser_args.parse_args()

solver = cvc5.Solver()
if args.int_bv:
    solver.setOption("incremental", "false")
solver.setLogic("QF_LIA")
solver.setOption("produce-models", "true")
if args.int_bv:
    solver.setOption("solve-int-as-bv", str(args.int_bv))
if args.miplib:
    solver.setOption("miplib-trick", "true")
parser = cvc5.InputParser(solver)
parser.setFileInput(cvc5.InputLanguage.SMT_LIB_2_6, args.file)
symbols = parser.getSymbolManager()
while True:
    command = parser.nextCommand()
    if command.isNull():
        break
    result = command.invoke(solver, symbols)
    if result:
        print(result, flush=True)

denominator = next(
    term for term in symbols.getDeclaredTerms() if str(term) == "denominator"
)
print(solver.getValue(denominator))
