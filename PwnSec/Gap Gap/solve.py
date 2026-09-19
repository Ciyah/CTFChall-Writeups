#!/usr/bin/env python3
import ast
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).with_name(".deps")))
from fpylll import IntegerMatrix, LLL
import sympy as sp


def load_values(path: str):
    values = {}
    for line in Path(path).read_text().splitlines():
        name, raw = line.split(" = ", 1)
        values[name] = ast.literal_eval(raw)
    return values


def coeff_vector(poly, x, dimension, scale):
    p = sp.Poly(sp.expand(poly.subs(x, x * scale)), x)
    return [int(p.nth(i)) for i in range(dimension)]


def small_root_unknown_factor(f, modulus, bound, beta, m=3, t=7):
    """Howgrave-Graham univariate small root for a divisor >= modulus**beta."""
    x = next(iter(f.free_symbols))
    degree = sp.degree(f, x)
    assert degree == 1 and sp.LC(sp.Poly(f, x)) == 1

    polys = []
    for i in range(m):
        for j in range(degree):
            polys.append(x**j * modulus ** (m - i) * f**i)
    for i in range(t):
        polys.append(x**i * f**m)

    dimension = len(polys)
    rows = [
        coeff_vector(poly, x, dimension, bound) for poly in polys
    ]
    lattice = IntegerMatrix.from_matrix(rows)
    LLL.reduction(lattice)

    candidates = []
    for row_index in range(dimension):
        row = [int(lattice[row_index, i]) for i in range(dimension)]
        # LLL polynomial was constructed in the variable x*bound.
        q = sum(sp.Rational(row[i], bound**i) * x**i for i in range(dimension))
        _, primitive = sp.Poly(q, x, domain=sp.QQ).clear_denoms()
        for root in sp.polys.polytools.ground_roots(primitive).keys():
            if root.is_Integer:
                value = int(root)
                if 0 <= value < bound:
                    candidates.append(value)
    return sorted(set(candidates))


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "public/output.txt"
    vals = load_values(input_path)
    N, e, c, leak = (vals[k] for k in ("N", "e", "c", "d_leak"))
    prefix, suffix = leak.split("*" * 30)

    place = 10**47
    d_known = int(prefix) * 10 ** (30 + 47) + int(suffix)

    # Divide the common even factor out. Then g | (e*d-1)/2 and
    # (N-1)/2 = g*h. The coefficient of the unknown is invertible modulo g*h.
    modulus = (N - 1) // 2
    constant = (e * d_known - 1) // 2
    coefficient = e * place // 2
    assert math.gcd(coefficient, modulus) == 1

    x = sp.symbols("x")
    monic_constant = constant * pow(coefficient, -1, modulus) % modulus
    f = x + monic_constant

    # g has 600 bits, while modulus has 2047 bits. The root is below 10^30.
    beta = 599 / modulus.bit_length()
    roots = small_root_unknown_factor(f, modulus, 10**30, beta)

    for missing in roots:
        d = d_known + missing * place
        common = math.gcd(N - 1, e * d - 1)
        if common.bit_length() not in range(599, 602):
            continue
        g = common // 2
        h = (N - 1) // (2 * g)

        # h = 2gab+a+b and N=pq imply p+q = 2g(a+b)+2.
        # Since a+b = h - lambda and lambda=(ed-1)/k, recover k from
        # the RSA relation by testing the narrow estimate k ~= ed/h.
        estimate = e * d // h
        for k in range(max(1, estimate - 4), estimate + 5):
            numerator = e * d - 1
            if numerator % k:
                continue
            lam = numerator // k
            s = 2 * g * (h - lam) + 2
            discriminant = s * s - 4 * N
            if discriminant < 0:
                continue
            r = math.isqrt(discriminant)
            if r * r != discriminant:
                continue
            p, q = (s + r) // 2, (s - r) // 2
            if p * q != N:
                continue
            plaintext = pow(c, d, N)
            flag = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, "big")
            print(f"missing = {missing:030d}")
            print(f"g = {g}")
            print(f"p = {p}")
            print(f"q = {q}")
            print(flag.decode())
            return
    raise RuntimeError(f"no valid key among roots: {roots}")


if __name__ == "__main__":
    main()
