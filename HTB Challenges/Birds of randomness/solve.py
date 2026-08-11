#!/usr/bin/env python3
import itertools
import math
import re
import socket

from ecdsa import ellipticcurve as ecc
from sympy import factorint, isprime
from sympy.ntheory.modular import crt

HOST, PORT = "154.57.164.82", 30828
P = 17101937747109687265202713197737423
N = 17101937747109687496599931614463506
GX = 3543321030468950376213178213609418
GY = 14807290861072031659976937040569354
ORDER_FACTORS = {2: 1, 3: 1, 7: 2, 1487: 1, 3761: 1,
                 176489: 1, 439693: 1, 3113111: 1, 43054831: 1}

E = ecc.CurveFp(P, 2, 3)
G = ecc.Point(E, GX, GY, N)
INF = ecc.INFINITY


def point_key(point):
    if point == INF:
        return None
    return int(point.x()), int(point.y())


def dlog_prime(base, target, order):
    """Baby-step/giant-step in a subgroup of prime order."""
    m = math.isqrt(order) + 1
    table = {}
    point = INF
    for j in range(m):
        table.setdefault(point_key(point), j)
        point = point + base
    forward_stride = m * base
    stride = INF if forward_stride == INF else -forward_stride
    point = target
    for i in range(m + 1):
        j = table.get(point_key(point))
        if j is not None:
            answer = i * m + j
            if answer < order:
                return answer
        point = point + stride
    raise ValueError("discrete log not found")


def pohlig_hellman(target):
    residues, moduli = [], []
    for prime, exponent in ORDER_FACTORS.items():
        modulus = prime ** exponent
        digit_base = (N // prime) * G
        value = 0
        for k in range(exponent):
            difference = target if value == 0 else target + -(value * G)
            reduced = (N // (prime ** (k + 1))) * difference
            digit = dlog_prime(digit_base, reduced, prime)
            value += digit * (prime ** k)
        residues.append(value)
        moduli.append(modulus)
    return int(crt(moduli, residues)[0])


def destination_candidates(d):
    factorization = factorint(d)
    factors = [prime for prime, exponent in factorization.items()
               for _ in range(exponent)]
    if len(factors) != 3:
        raise ValueError(f"expected three prime factors, got {factorization}")
    candidates = set()
    for state in set(itertools.permutations(factors)):
        x, y, z = state
        if not (0 < x < 30269 and 0 < y < 30307 and 0 < z < 30323):
            continue
        while True:
            x = 171 * x % 30269
            y = 172 * y % 30307
            z = 170 * z % 30323
            if isprime(x) and isprime(y) and isprime(z):
                point = (x * y * z) * G
                candidates.add((int(point.x()), int(point.y())))
                break
    return candidates


def recv_until(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def main():
    with socket.create_connection((HOST, PORT)) as sock:
        banner = recv_until(sock, b"Enter the x coordinate: ")
        print(banner.decode(), end="")
        match = re.search(rb"station were: \((\d+), (\d+)\)", banner)
        if not match:
            raise ValueError("could not parse departing coordinates")
        departure = ecc.Point(E, int(match[1]), int(match[2]), N)
        d = pohlig_hellman(departure)
        candidates = destination_candidates(d)
        print(f"Recovered d={d}; trying {len(candidates)} candidate(s)")
        for x, y in candidates:
            sock.sendall(f"{x}\n".encode())
            recv_until(sock, b"Enter the y coordinate: ")
            sock.sendall(f"{y}\n".encode())
            reply = recv_until(sock, b"Enter the x coordinate: ")
            print(reply.decode(), end="")
            if b"HTB{" in reply:
                return
        raise RuntimeError("all destination candidates failed")


if __name__ == "__main__":
    main()
