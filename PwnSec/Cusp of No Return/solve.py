#!/usr/bin/env python3
"""Solve a Cusp of No Return instance."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).with_name("public")))

from algebra import bracket, flatten, log_unipotent  # noqa: E402
from curve import Curve, Fp2, decode_point, key_from_j, quotient_j  # noqa: E402
from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # noqa: E402


def invert_matrix(a: list[list[int]], modulus: int, prime: int) -> list[list[int]]:
    """Invert a square matrix over Z/prime^e using unit pivots."""
    n = len(a)
    r = [[x % modulus for x in row] + [int(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if r[i][col] % prime)
        r[col], r[pivot] = r[pivot], r[col]
        inv = pow(r[col][col], -1, modulus)
        r[col] = [x * inv % modulus for x in r[col]]
        for i in range(n):
            if i != col:
                t = r[i][col]
                r[i] = [(x - t * y) % modulus for x, y in zip(r[i], r[col])]
    return [row[n:] for row in r]


def mat_vec(a: list[list[int]], v: list[int], modulus: int) -> list[int]:
    return [sum(x * y for x, y in zip(row, v)) % modulus for row in a]


def coordinates(target: list[list[int]], basis: list[list[list[int]]],
                modulus: int, prime: int) -> list[int]:
    """Coordinates in a free matrix span over a local prime-power ring."""
    cols = [flatten(b) for b in basis]
    rhs = flatten(target)
    width = len(cols)
    rows = [[cols[j][i] % modulus for j in range(width)]
            for i in range(len(rhs))]

    # Select independent equations using elimination modulo the residue field.
    work = [[x % prime for x in row] + [i] for i, row in enumerate(rows)]
    selected: list[int] = []
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(work))
                      if work[i][col] % prime), None)
        if pivot is None:
            raise ValueError("matrix basis is not free locally")
        work[rank], work[pivot] = work[pivot], work[rank]
        selected.append(work[rank][-1])
        inv = pow(work[rank][col], -1, prime)
        work[rank][:-1] = [x * inv % prime for x in work[rank][:-1]]
        for i in range(rank + 1, len(work)):
            t = work[i][col]
            if t:
                work[i][:-1] = [(x - t * y) % prime
                                 for x, y in zip(work[i][:-1], work[rank][:-1])]
        rank += 1

    square = [rows[i] for i in selected]
    answer = mat_vec(invert_matrix(square, modulus, prime),
                     [rhs[i] % modulus for i in selected], modulus)
    if any(sum(c * col[i] for c, col in zip(answer, cols)) % modulus
           != rhs[i] % modulus for i in range(len(rhs))):
        raise ValueError("coordinate reconstruction failed")
    return answer


def kernel_vector(equations: list[list[int]], modulus: int,
                  prime: int) -> list[int]:
    """Return a primitive vector spanning a rank-one homogeneous kernel."""
    a = [[x % modulus for x in row] for row in equations]
    rows, cols = len(a), len(a[0])
    pivot_cols: list[int] = []
    row = 0
    for col in range(cols):
        pivot = next((i for i in range(row, rows) if a[i][col] % prime), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(a[row][col], -1, modulus)
        a[row] = [x * inv % modulus for x in a[row]]
        for i in range(rows):
            if i != row and a[i][col]:
                t = a[i][col]
                a[i] = [(x - t * y) % modulus for x, y in zip(a[i], a[row])]
        pivot_cols.append(col)
        row += 1
    free = [j for j in range(cols) if j not in pivot_cols]
    if len(free) != 1:
        raise ValueError(f"expected a rank-one kernel, got {len(free)} free variables")
    v = [0] * cols
    v[free[0]] = 1
    for i, col in reversed(list(enumerate(pivot_cols))):
        v[col] = -sum(a[i][j] * v[j] for j in free) % modulus
    if any(sum(x * y for x, y in zip(eq, v)) % modulus for eq in equations):
        raise ValueError("kernel reconstruction failed")
    return v


def conjugated_action(action_pair, lie_basis, modulus, prime):
    columns = []
    for encoded_image in action_pair:
        image = log_unipotent(encoded_image, modulus)
        columns.append(coordinates(image, lie_basis, modulus, prime)[:2])
    return [[columns[0][0], columns[1][0]],
            [columns[0][1], columns[1][1]]]


def recover_local(instance: dict, prime: int, exponent: int) -> int:
    modulus = prime ** exponent
    X, Y = [log_unipotent(g, modulus) for g in instance["generators"]]
    Z = bracket(X, Y, modulus)
    U = bracket(X, Z, modulus)
    V = bracket(Y, Z, modulus)
    lie_basis = [X, Y, Z, U, V]

    packet = [coordinates(log_unipotent(g, modulus), lie_basis,
                          modulus, prime)
              for g in instance["cuspidal_packet"][:2]]
    points = []
    for c in packet:
        if c[2] % prime == 0:
            raise ValueError("non-unit cusp coordinate")
        inv = pow(c[2], -1, modulus)
        points.append([c[3] * inv % modulus, c[4] * inv % modulus])
    direction = [(points[1][i] - points[0][i]) % modulus for i in range(2)]

    actions = instance["class_two_outer_lifts"]
    C_f = conjugated_action(actions["frobenius_p"], lie_basis, modulus, prime)
    C_i = conjugated_action(actions["cm_i"], lie_basis, modulus, prime)
    F = [[1, 0], [0, -1]]
    I = [[0, -1], [1, 0]]

    # T*C = m*T, where T is the hidden marking M up to a unit scalar.
    equations = []
    for C, m in ((C_f, F), (C_i, I)):
        for i in range(2):
            for j in range(2):
                row = [0] * 4
                for k in range(2):
                    row[2 * i + k] += C[k][j]
                    row[2 * k + j] -= m[i][k]
                equations.append([x % modulus for x in row])
    flat_T = kernel_vector(equations, modulus, prime)
    T = [flat_T[:2], flat_T[2:]]
    target = mat_vec(T, direction, modulus)
    if target[0] % prime == 0:
        raise ValueError("recovered target has non-unit first coordinate")
    return target[1] * pow(target[0], -1, modulus) % modulus


def crt(a: int, m: int, b: int, n: int) -> int:
    return (a + ((b - a) * pow(m, -1, n) % n) * m) % (m * n)


def solve(instance: dict) -> tuple[int, list[int], bytes]:
    locals_ = []
    for prime, exponent in instance["factors"]:
        locals_.append((recover_local(instance, prime, exponent), prime ** exponent))
    slope = crt(locals_[0][0], locals_[0][1], locals_[1][0], locals_[1][1])

    p = instance["field"]["p"]
    E = Curve(Fp2(p, *instance["curve"]["a"]),
              Fp2(p, *instance["curve"]["b"]))
    P = decode_point(p, instance["curve"]["P"])
    Q = decode_point(p, instance["curve"]["Q"])
    R = E.add(P, E.mul(slope, Q))
    j = quotient_j(E, R, [tuple(x) for x in instance["factors"]])

    seal = instance["seal"]
    flag = AESGCM(key_from_j(j)).decrypt(bytes.fromhex(seal["nonce"]),
                                         bytes.fromhex(seal["ciphertext_and_tag"]),
                                         bytes.fromhex(seal["aad"]))
    return slope, j.pair(), flag


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", type=Path, nargs="?", default=Path("instance.json"))
    args = parser.parse_args()
    instance = json.loads(args.instance.read_text())
    slope, j, flag = solve(instance)
    print(f"secret slope = {slope}")
    print(f"target j = {j}")
    print(flag.decode())


if __name__ == "__main__":
    main()
