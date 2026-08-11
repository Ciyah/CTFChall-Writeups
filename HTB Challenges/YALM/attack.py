#!/usr/bin/env python3
from fpylll import IntegerMatrix, LLL
from sympy import Poly, symbols, gcd

x = symbols("x")
N = int("ac49887178dcc71f99bd953912f2576d15768a0c227e2b43c3430a6ee0873cdc5aff3607999968c2c8291d0115fbe3835acdd752080a46ba05192766f0d424adaf28925c63954fc5d83f3dec7c5dbf9a71550ea4049c26f8d545ddb677d2a82e8bd6854896bf0b215e5e82ae8904e929012ccf4e8411be63c0e03a2a5989c86eda2e76cae45f832c62d6a4af005ba8a2a3f06b2fdff0390d1cb57b5c709c62c413f10e1ca7fe5f8b0cb5ca380d5b1799509a3510e984c47cb6146c6ccaaf7504c8a9e981fd709728b3a2ad136736dc20f5ae57135a6820d266bfab6eec46e35569215ebf48731c2d188c1e8bdb2b0b90acedbea915ec1cbdd7a7428ebb2dc3af", 16)
C = int("7112004e371290a40266dbedbff093e39631f716972c4700e6f5d01d7316ff1a2368657624917f8c1e0637621ca3c4de2ce8bffe97faefb62e7f21079fa750aa8e3a8b8e1181c064e2cda7688fa0986a8412aa2cbbc256d33556aeecdc51420b4f39f29723bf70f8d0d1100332caf2dcd6f37ee7e018b2bc6e3c2a8ff1cb87e12fb155671b9188b75dbf16ac9c1e6074b80132134b5e77f8de9e271e66897140e1a5cf412395e3644d0a2a8f6a361388580509c88ca28519eea86ab04e5e2e0738070f0729ff76696900020f78076f6f1d3544603b91492597e19f8094753fa7c7086e1d33df768b5ddb12ef86d604535accc9c3d8f83db90a8ab2960e3bcfbb", 16)
PREFIX = b"Hey! This is my secret... it is secure because RSA is extremely strong and very hard to break... Here you go: HTB{"


def coppersmith(f, bound, m=3):
    d = f.degree()
    polys = []
    for i in range(m):
        for j in range(d):
            polys.append(Poly((x ** j) * (N ** (m-i)) * (f.as_expr() ** i), x))
    dim = d * m
    lattice = IntegerMatrix(dim, dim)
    for row, p in enumerate(polys):
        for col in range(dim):
            lattice[row, col] = int(p.nth(col)) * bound ** col
    LLL.reduction(lattice)

    reduced = []
    for row in range(dim):
        coeffs = [int(lattice[row, col]) // (bound ** col) for col in range(dim)]
        reduced.append(Poly(sum(a*x**i for i, a in enumerate(coeffs)), x, domain="ZZ"))
    for i in range(dim):
        for j in range(i):
            g = gcd(reduced[i], reduced[j])
            if g.degree() > 0:
                for root, multiplicity in g.ground_roots().items():
                    if root.q == 1:
                        yield int(root)


for unknown_len in range(2, 76):
    shift = 8 * unknown_len
    known = int.from_bytes(PREFIX, "big") << shift
    f = Poly((known + x) ** 3 - C, x, domain="ZZ")
    # The polynomial is monic, and the unknown suffix is below this exact bound.
    for root in coppersmith(f, 1 << shift):
        if 0 <= root < (1 << shift) and pow(known + root, 3, N) == C:
            suffix = root.to_bytes(unknown_len, "big")
            flag = b"HTB{" + suffix
            if flag.endswith(b"}"):
                print(flag.decode())
                raise SystemExit
    print(f"tried flag length {unknown_len + 4}", flush=True)

raise SystemExit("root not found")
