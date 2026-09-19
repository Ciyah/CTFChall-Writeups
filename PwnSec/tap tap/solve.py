#!/usr/bin/env python3
"""Solve PwnSec 'tap tap' with a truncated Fibonacci-LFSR lattice attack.

Temporary dependencies used by this script:
    python3 -m pip install fpylll cysignals python-flint
"""

import ast
import hashlib
import math
import re
from pathlib import Path

from flint import fmpz, fmpz_mod_poly_ctx, fmpz_poly
from fpylll import BKZ, IntegerMatrix, LLL


N, K, H, ELL = 25, 128, 80, 48
LOW, HALF = 1 << ELL, 1 << (ELL - 1)


def load_instance():
    text = (Path(__file__).parent / "public" / "chall.py").read_text()
    outputs = ast.literal_eval(re.search(r"'''\s*(\[[^]]+\])", text, re.S).group(1))
    ciphertext = bytes.fromhex(re.search(r"\]\s*\n([0-9a-f]+)\s*\n'''", text).group(1))
    return outputs, ciphertext


def reduce_rows(rows, block_size=10):
    basis = IntegerMatrix.from_matrix(rows)
    LLL.reduction(basis, delta=0.99)
    if block_size:
        BKZ.reduction(basis, BKZ.Param(block_size=block_size))
    return [[int(basis[i, j]) for j in range(basis.ncols)] for i in range(basis.nrows)]


def primitive_poly(coeffs):
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    if len(coeffs) < 2:
        return None
    g = math.gcd(*map(abs, (x for x in coeffs if x)))
    coeffs = [x // g for x in coeffs]
    if coeffs[-1] < 0:
        coeffs = [-x for x in coeffs]
    return fmpz_poly(coeffs)


def annihilating_polynomials_unknown_modulus(outputs, r=90, t=90, rows_to_keep=40):
    dim = r + t
    rows = [[0] * dim for _ in range(dim)]
    for i in range(t):
        rows[i][i] = 1 << H
    for i in range(r):
        rows[t + i][:t] = outputs[i:i + t]
        rows[t + i][t + i] = 1

    print(f"[*] Reducing unknown-modulus lattice ({dim} x {dim})")
    reduced = reduce_rows(rows)
    polys, seen = [], set()
    for row in reduced[:rows_to_keep]:
        poly = primitive_poly(row[t:])
        if poly is not None and tuple(poly) not in seen:
            polys.append(poly)
            seen.add(tuple(poly))
    print(f"[*] Retained {len(polys)} annihilating-polynomial candidates")
    return polys


def integer_nth_root(value, n):
    lo, hi = 0, 1 << ((value.bit_length() + n - 1) // n)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**n <= value:
            lo = mid
        else:
            hi = mid
    return lo


def recover_modulus(polys, max_resultants=12):
    vals = []
    for i, left in enumerate(polys):
        for right in polys[i + 1:]:
            value = abs(int(left.resultant(right)))
            if value:
                vals.append(value)
                print(f"[*] resultant #{len(vals)}: {value.bit_length()} bits")
            if len(vals) == max_resultants:
                break
        if len(vals) == max_resultants:
            break
    common = math.gcd(*vals)
    print(f"[*] gcd(resultants): {common.bit_length()} bits")

    # Usually the gcd is exactly p^N.  If it has a small cofactor, trial-divide
    # that cofactor after taking the approximate Nth root.
    root = integer_nth_root(common, N)
    candidates = set()
    for guess in range(max(2, root - 4), root + 5):
        if common % guess**N == 0:
            candidates.add(guess)
    lower, upper = (1 << K) - (1 << 50) - 256, 1 << K
    candidates = [p for p in candidates if lower < p < upper and fmpz(p).is_prime()]
    if not candidates:
        # FLINT is very effective here because the gcd consists mostly of p^N.
        for factor, _exponent in fmpz(common).factor():
            p = int(factor)
            if lower < p < upper:
                candidates.append(p)
    if len(candidates) != 1:
        raise RuntimeError(f"expected one modulus candidate, got {candidates}")
    print(f"[+] p = {candidates[0]}")
    return candidates[0]


def recover_coefficients(polys, modulus):
    polynomial_ring = fmpz_mod_poly_ctx(modulus)
    reduced = []
    for poly in polys:
        candidate = polynomial_ring([int(c) % modulus for c in poly])
        if candidate.degree() >= N:
            reduced.append(candidate.monic())
    for start in reduced:
        g = start
        for candidate in reduced:
            h = g.gcd(candidate)
            if h.degree() >= N:
                g = h.monic()
            if g.degree() == N:
                coeffs = [(-int(g[i])) % modulus for i in range(N)]
                print("[+] Recovered the degree-25 characteristic polynomial")
                return coeffs
    raise RuntimeError("characteristic polynomial recovery failed")


def q_vectors(coeffs, modulus, count):
    q = [[int(i == j) for i in range(N)] for j in range(N)]
    for j in range(N, count):
        q.append([
            sum(coeffs[i] * q[j - N + i][column] for i in range(N)) % modulus
            for column in range(N)
        ])
    return q


def recover_observed_values(coeffs, modulus, outputs, count=52):
    outputs = outputs[:count]
    q = q_vectors(coeffs, modulus, count)
    gammas = []
    for j in range(N, count):
        sy = sum(q[j][i] * outputs[i] for i in range(N))
        sq = sum(q[j])
        gammas.append((HALF * (sq - 1) - LOW * (outputs[j] - sy)) % modulus)

    dim = count + 1
    rows = [[0] * dim for _ in range(dim)]
    rows[0] = [HALF] + [0] * N + gammas
    for i in range(N):
        rows[1 + i][1 + i] = 1
        for offset, j in enumerate(range(N, count)):
            rows[1 + i][1 + N + offset] = q[j][i]
    for offset in range(count - N):
        rows[1 + N + offset][1 + N + offset] = modulus

    print(f"[*] Reducing low-bit recovery lattice ({dim} x {dim})")
    reduced = reduce_rows(rows)
    for row in reduced:
        if abs(row[0]) != HALF:
            continue
        if row[0] < 0:
            row = [-x for x in row]
        lows = [x + HALF for x in row[1:]]
        if not all(0 <= z < LOW for z in lows):
            continue
        values = [LOW * y + z for y, z in zip(outputs, lows)]
        if all(
            (sum(q[j][i] * values[i] for i in range(N)) - values[j]) % modulus == 0
            for j in range(N, count)
        ):
            print("[+] Recovered the hidden low 48 bits")
            return values
    raise RuntimeError("low-bit recovery failed")


def rewind(observed, coeffs, modulus, steps=N):
    seq = observed[:]
    inv_c0 = pow(coeffs[0], -1, modulus)
    for _ in range(steps):
        target = seq[N - 1]
        tail = sum(coeffs[j] * seq[j - 1] for j in range(1, N))
        seq.insert(0, (target - tail) * inv_c0 % modulus)
    return seq


def extend(seq, coeffs, modulus, total):
    while len(seq) < total:
        seq.append(sum(c * a for c, a in zip(coeffs, seq[-N:])) % modulus)
    return seq


def main():
    outputs, ciphertext = load_instance()
    polys = annihilating_polynomials_unknown_modulus(outputs)
    modulus = recover_modulus(polys)
    coeffs = recover_coefficients(polys, modulus)
    observed = recover_observed_values(coeffs, modulus, outputs)
    full = extend(rewind(observed, coeffs, modulus), coeffs, modulus, N + len(outputs))
    assert [a >> ELL for a in full[N:]] == outputs

    seed = hashlib.sha256("".join(map(str, full)).encode()).digest()
    key = hashlib.shake_256(seed).digest(len(ciphertext))
    flag = bytes(a ^ b for a, b in zip(ciphertext, key))
    print(f"[+] flag = {flag.decode()}")


if __name__ == "__main__":
    main()
