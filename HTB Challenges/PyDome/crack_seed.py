#!/usr/bin/env python3
import random, sys

selected_indices = [4,320,285,311,189,488,488,317,327,324,46,189,314,189,314,488,327,41,46,285,46,488,189,324,327,327,506,46,285,327,317,488,317,92,41,4,488,314,4,488,506,488,327,285,327,320,488,189,41,488,327,507,327,327,314,285,92,324,507,317,285,324,507,507]
observed_chars = [488,285,507,4,327,507,324,314,189,488,189,327,4,327,327,314,327,488,46,506]
allowed = [{i for i, value in enumerate(selected_indices) if value == seen} for seen in observed_chars]
with open(sys.argv[1], "rb") as source:
    for raw in source:
        try:
            candidate = raw.rstrip(b"\r\n").decode()
        except UnicodeDecodeError:
            continue
        rng = random.Random(",".join(candidate.split("A")))
        if rng.randrange(64) % 2 and all(rng.randrange(64) in choices for choices in allowed):
            print(repr(candidate), flush=True)
