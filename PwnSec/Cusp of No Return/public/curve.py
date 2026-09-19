"""Reference Fp2, short-Weierstrass arithmetic, and small-degree Velu maps.

Intentionally portable rather than constant-time. This is CTF code, not a
production cryptographic library.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd, isqrt
import hashlib
from typing import Any


@dataclass(frozen=True, slots=True)
class Fp2:
    p: int
    a: int = 0
    b: int = 0

    def __post_init__(self):
        object.__setattr__(self, 'a', self.a % self.p)
        object.__setattr__(self, 'b', self.b % self.p)

    def coerce(self, other: Any) -> Fp2:
        if isinstance(other, int):
            return Fp2(self.p, other)
        if not isinstance(other, Fp2) or other.p != self.p:
            raise TypeError('incompatible field element')
        return other

    def __add__(self, other: Any) -> Fp2:
        o = self.coerce(other)
        return Fp2(self.p, self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self) -> Fp2:
        return Fp2(self.p, -self.a, -self.b)

    def __sub__(self, other: Any) -> Fp2:
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> Fp2:
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> Fp2:
        if isinstance(other, int):
            return Fp2(self.p, self.a * other, self.b * other)
        o = self.coerce(other)
        return Fp2(self.p, self.a * o.a - self.b * o.b,
                   self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def inverse(self) -> Fp2:
        norm = (self.a * self.a + self.b * self.b) % self.p
        t = pow(norm, -1, self.p)
        return Fp2(self.p, self.a * t, -self.b * t)

    def __truediv__(self, other: Any) -> Fp2:
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other: Any) -> Fp2:
        return self.coerce(other) * self.inverse()

    def __pow__(self, k: int) -> Fp2:
        if k < 0:
            return self.inverse() ** (-k)
        x, out = self, Fp2(self.p, 1)
        while k:
            if k & 1:
                out = out * x
            x = x * x
            k >>= 1
        return out

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def pair(self) -> list[int]:
        return [self.a, self.b]


Point = tuple[Fp2, Fp2] | None


@dataclass(frozen=True, slots=True)
class Curve:
    a: Fp2
    b: Fp2

    def on_curve(self, P: Point) -> bool:
        return P is None or P[1] * P[1] == P[0] ** 3 + self.a * P[0] + self.b

    def add(self, P: Point, Q: Point) -> Point:
        if P is None:
            return Q
        if Q is None:
            return P
        x, y = P
        u, v = Q
        if x == u:
            if (y + v).is_zero():
                return None
            slope = (3 * x * x + self.a) / (2 * y)
        else:
            slope = (v - y) / (u - x)
        xx = slope * slope - x - u
        yy = slope * (x - xx) - y
        return xx, yy

    def mul(self, k: int, P: Point) -> Point:
        if k < 0:
            return self.mul(-k, None if P is None else (P[0], -P[1]))
        out = None
        while k:
            if k & 1:
                out = self.add(out, P)
            k >>= 1
            if k:
                P = self.add(P, P)
        return out

    def j(self) -> Fp2:
        return 1728 * (4 * self.a ** 3) / (4 * self.a ** 3 + 27 * self.b ** 2)

    def velu(self, T: Point, ell: int) -> tuple[Curve, Any]:
        if ell not in (5, 7) or T is None or not self.on_curve(T):
            raise ValueError('invalid small kernel')
        if self.mul(ell, T) is not None:
            raise ValueError('small kernel has wrong order')
        kernel = []
        q = T
        for _ in range(1, ell):
            if q is None:
                raise ValueError('kernel generator has smaller order')
            kernel.append(q)
            q = self.add(q, T)
        t = sum((3 * x * x + self.a for x, _ in kernel), Fp2(self.a.p))
        w = sum((5 * x ** 3 + 3 * self.a * x + 2 * self.b for x, _ in kernel),
                Fp2(self.a.p))
        target = Curve(self.a - 5 * t, self.b - 7 * w)

        def evaluate(P: Point) -> Point:
            if P is None or P in kernel:
                return None
            xx, yy = P
            for Q in kernel:
                S = self.add(P, Q)
                if S is None:
                    raise ValueError('unexpected kernel intersection')
                xx = xx + S[0] - Q[0]
                yy = yy + S[1] - Q[1]
            out = xx, yy
            if not target.on_curve(out):
                raise ArithmeticError('Velu image is not on the codomain')
            return out

        return target, evaluate


def quotient_j(E: Curve, R: Point, factors: list[tuple[int, int]],
               progress=None) -> Fp2:
    N = 1
    for ell, e in factors:
        if ell not in (5, 7) or e < 1:
            raise ValueError('unsupported factorization')
        N *= ell ** e
    if R is None or not E.on_curve(R) or E.mul(N, R) is not None:
        raise ValueError('bad full kernel generator')
    if any(E.mul(N // ell, R) is None for ell, _ in factors):
        raise ValueError('full kernel does not have exact advertised order')
    remaining = N
    count = 0
    for ell, e in factors:
        for _ in range(e):
            T = E.mul(remaining // ell, R)
            E, phi = E.velu(T, ell)
            R = phi(R)
            remaining //= ell
            count += 1
            if progress:
                progress(count, ell, remaining)
    if remaining != 1 or R is not None:
        raise ArithmeticError('isogeny chain did not exhaust the kernel')
    return E.j()


def encode_point(P: Point) -> list[list[int]] | None:
    return None if P is None else [P[0].pair(), P[1].pair()]


def decode_point(p: int, obj) -> Point:
    if obj is None:
        return None
    return Fp2(p, *map(int, obj[0])), Fp2(p, *map(int, obj[1]))


def key_from_j(j: Fp2) -> bytes:
    width = (j.p.bit_length() + 7) // 8
    blob = j.a.to_bytes(width, 'big') + j.b.to_bytes(width, 'big')
    return hashlib.sha256(b'pwnsec/cusp-of-no-return/j/v1\x00' + blob).digest()


def _mat2_mul(x, y, n):
    a, b, c, d = x
    e, f, g, h = y
    return ((a*e+b*g) % n, (a*f+b*h) % n,
            (c*e+d*g) % n, (c*f+d*h) % n)


def lucas_u(k: int, parameter: int, n: int) -> int:
    # U_0=0, U_1=1, U_{r+2}=parameter*U_{r+1}-U_r.
    out = (1, 0, 0, 1)
    m = (parameter % n, -1 % n, 1, 0)
    while k:
        if k & 1:
            out = _mat2_mul(out, m, n)
        m = _mat2_mul(m, m, n)
        k >>= 1
    return out[2]


def verify_prime_certificate(p: int, N: int, cert: dict) -> bool:
    """Lucas-order certificate; the proof is in organizer/MATHEMATICS.md.

    N has ONLY the known prime factors 5 and 7. A probable-prime test is not
    relied upon for acceptance.
    """
    if p <= 3 or p % 2 == 0 or (p + 1) % N or N - 1 <= isqrt(p):
        return False
    t = N
    for q in (5, 7):
        if t % q:
            return False
        while t % q == 0:
            t //= q
    if t != 1:
        return False
    a = int(cert['parameter'])
    if gcd(a * a - 4, p) != 1:
        return False
    if lucas_u(p + 1, a, p) != 0:
        return False
    return all(gcd(lucas_u((p + 1) // q, a, p), p) == 1 for q in (5, 7))


def probable_prime(n: int) -> bool:
    """Candidate filter only; every accepted output gets a certificate."""
    if n < 2:
        return False
    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for a in bases:
        if n % a == 0:
            return n == a
    d, s = n - 1, 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def certified_prime(N: int, rng) -> tuple[int, int, dict]:
    bound = min(65536, max(2, (N - 2) // 8))
    start = rng.randrange(1, bound)
    for offset in range(bound - 1):
        c = 1 + (start - 1 + offset) % (bound - 1)
        if gcd(c, 35) != 1:
            continue
        p = 4 * c * N - 1
        if not probable_prime(p):
            continue
        for a in range(3, 260):
            cert = {'parameter': a}
            if verify_prime_certificate(p, N, cert):
                return p, 4 * c, cert
    raise RuntimeError('prime search range exhausted; retry or use larger exponents')


def torsion_basis(p: int, N: int, cofactor: int, rng) -> tuple[Curve, Point, Point]:
    if p % 4 != 3 or p + 1 != cofactor * N or gcd(cofactor, 35) != 1:
        raise ValueError('bad elliptic-curve parameters')
    E = Curve(Fp2(p, 1), Fp2(p))
    for _ in range(10000):
        x = rng.randrange(p)
        y2 = (x * x * x + x) % p
        y = pow(y2, (p + 1) // 4, p)
        if y * y % p != y2:
            continue
        P = E.mul(cofactor, (Fp2(p, x), Fp2(p, y)))
        if P is None or E.mul(N, P) is not None:
            continue
        if any(E.mul(N // q, P) is None for q in (5, 7)):
            continue
        Q = (-P[0], Fp2(p, 0, P[1].a))
        if not E.on_curve(Q) or E.mul(N, Q) is not None:
            raise ArithmeticError('distortion map failed')
        return E, P, Q
    raise RuntimeError('torsion basis search exhausted')
