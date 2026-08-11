#!/usr/bin/env python3
import ast
from itertools import product
from pathlib import Path


DET = 6297
ADJUGATE = (
    (11622, 14253, 2780),
    (7701, 9498, 1815),
    (-624, -723, -107),
)


def decrypt(ciphertexts, offset):
    plaintext = []
    for ciphertext in ciphertexts:
        shifted = [ciphertext[i] - offset[i] for i in range(3)]
        numerators = [
            sum(shifted[k] * ADJUGATE[k][j] for k in range(3))
            for j in range(3)
        ]

        if any(value % DET for value in numerators):
            return None

        char, noise_a, noise_b = (value // DET for value in numerators)
        if not (32 <= char < 127 and 0 <= noise_a <= 100 and 0 <= noise_b <= 100):
            return None
        plaintext.append(chr(char))

    return "".join(plaintext)


def main():
    output = Path(__file__).with_name("output.txt")
    ciphertexts = [ast.literal_eval(line) for line in output.read_text().splitlines()]

    for offset in product(range(11), repeat=3):
        plaintext = decrypt(ciphertexts, offset)
        if plaintext is not None and plaintext.startswith("HTB{") and plaintext.endswith("}"):
            print(f"r = {offset}")
            print(plaintext)
            return

    raise RuntimeError("No valid offset found")


if __name__ == "__main__":
    main()
