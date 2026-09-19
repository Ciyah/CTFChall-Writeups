"""Small exact matrix routines over Z/nZ. No floating point arithmetic."""
from __future__ import annotations
from math import gcd
from typing import Sequence

Matrix = list[list[int]]


def eye(d: int) -> Matrix:
    return [[int(i == j) for j in range(d)] for i in range(d)]


def zero(d: int) -> Matrix:
    return [[0] * d for _ in range(d)]


def add(a: Matrix, b: Matrix, n: int) -> Matrix:
    return [[(x + y) % n for x, y in zip(r, s)] for r, s in zip(a, b)]


def sub(a: Matrix, b: Matrix, n: int) -> Matrix:
    return [[(x - y) % n for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(a: Matrix, k: int, n: int) -> Matrix:
    return [[x * k % n for x in row] for row in a]


def mul(a: Matrix, b: Matrix, n: int) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) % n for col in bt] for row in a]


def bracket(a: Matrix, b: Matrix, n: int) -> Matrix:
    return sub(mul(a, b, n), mul(b, a, n), n)


def combine(coeffs: Sequence[int], basis: Sequence[Matrix], n: int) -> Matrix:
    d = len(basis[0])
    return [[sum(c * b[i][j] for c, b in zip(coeffs, basis)) % n
             for j in range(d)] for i in range(d)]


def flatten(a: Matrix) -> list[int]:
    return [x for row in a for x in row]


def reduce_matrix(a: Matrix, n: int) -> Matrix:
    return [[x % n for x in row] for row in a]


def exp_nilpotent(a: Matrix, n: int) -> Matrix:
    """Matrix exponential, for a**4 = 0 and gcd(6,n)=1."""
    a2 = mul(a, a, n)
    a3 = mul(a2, a, n)
    if mul(a3, a, n) != zero(len(a)):
        raise ValueError('nilpotency index exceeds four')
    return add(eye(len(a)), combine([1, pow(2, -1, n), pow(6, -1, n)],
                                   [a, a2, a3], n), n)


def log_unipotent(g: Matrix, n: int) -> Matrix:
    """Exact finite logarithm. Also checks the advertised truncation."""
    a = sub(g, eye(len(g)), n)
    a2 = mul(a, a, n)
    a3 = mul(a2, a, n)
    if mul(a3, a, n) != zero(len(g)):
        raise ValueError('not a valid class-three unipotent record')
    return combine([1, -pow(2, -1, n), pow(3, -1, n)], [a, a2, a3], n)


def inverse_unit_pivots(a: Matrix, n: int) -> Matrix:
    """Invert using unit pivots; may reject invertible composite-ring matrices.

    The generator retries after rejection. Over each local factor used by the
    solver, an invertible matrix always admits these row pivots.
    """
    d = len(a)
    r = [list(row) + eye(d)[i] for i, row in enumerate(a)]
    for c in range(d):
        p = next((j for j in range(c, d) if gcd(r[j][c], n) == 1), None)
        if p is None:
            raise ValueError('no unit pivot; split the modulus or choose another matrix')
        r[c], r[p] = r[p], r[c]
        inv = pow(r[c][c], -1, n)
        r[c] = [x * inv % n for x in r[c]]
        for j in range(d):
            if j != c and r[j][c] % n:
                t = r[j][c]
                r[j] = [(x - t * y) % n for x, y in zip(r[j], r[c])]
    out = [row[d:] for row in r]
    if mul(a, out, n) != eye(d):
        raise ValueError('matrix inversion failed')
    return out


def det2(a: Matrix, n: int) -> int:
    return (a[0][0] * a[1][1] - a[0][1] * a[1][0]) % n


def inverse2(a: Matrix, n: int) -> Matrix:
    d = pow(det2(a, n), -1, n)
    return [[a[1][1] * d % n, -a[0][1] * d % n],
            [-a[1][0] * d % n, a[0][0] * d % n]]


def lie_bracket(v: Sequence[int], w: Sequence[int], n: int) -> list[int]:
    # Basis: x, y, [x,y], [x,[x,y]], [y,[x,y]].
    return [0, 0, (v[0] * w[1] - v[1] * w[0]) % n,
            (v[0] * w[2] - v[2] * w[0]) % n,
            (v[1] * w[2] - v[2] * w[1]) % n]


def free_lie_representation(n: int) -> list[Matrix]:
    """Left multiplication on words of length <=3, dimension 1+2+4+8."""
    words = [()]
    for k in range(1, 4):
        words.extend(tuple((i >> j) & 1 for j in range(k - 1, -1, -1))
                     for i in range(2 ** k))
    index = {w: i for i, w in enumerate(words)}
    x, y = zero(15), zero(15)
    for j, w in enumerate(words):
        if len(w) < 3:
            x[index[(0,) + w]][j] = 1
            y[index[(1,) + w]][j] = 1
    z = bracket(x, y, n)
    return [x, y, z, bracket(x, z, n), bracket(y, z, n)]


def automorphism_columns(x: list[int], y: list[int], n: int) -> list[list[int]]:
    z = lie_bracket(x, y, n)
    return [x, y, z, lie_bracket(x, z, n), lie_bracket(y, z, n)]


def apply_columns(columns: list[list[int]], v: Sequence[int], n: int) -> list[int]:
    return [sum(c[j] * t for c, t in zip(columns, v)) % n for j in range(len(v))]
