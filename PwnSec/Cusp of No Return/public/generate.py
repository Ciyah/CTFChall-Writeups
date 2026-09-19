#!/usr/bin/env python3
"""Instance generator for Cusp of No Return. Safe to distribute as source.

The actual flag, secret slope, change of marking and RNG state are NEVER part
of the public output. Production generation uses SystemRandom exclusively.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import re
import secrets
import time

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from algebra import (apply_columns, automorphism_columns, combine, det2,
                     exp_nilpotent, free_lie_representation, inverse2,
                     inverse_unit_pivots, mul)
from curve import (certified_prime, encode_point, key_from_j, quotient_j,
                   torsion_basis)

VERSION = 'pwnsec/cusp-of-no-return/v1'
AAD = VERSION.encode('ascii')


def unit(rng, n: int) -> int:
    while True:
        x = rng.randrange(n)
        if math.gcd(x, n) == 1:
            return x


def make_instance(flag: bytes, e5: int = 64, e7: int = 48, rng=None):
    if not re.fullmatch(rb'(?:pwnsec|flag)\{[!-~]+\}', flag):
        raise ValueError('flag must have format pwnsec{...} or flag{...} with printable ASCII contents')
    if e5 < 1 or e7 < 1:
        raise ValueError('both prime-power factors are required')
    rng = secrets.SystemRandom() if rng is None else rng
    factors = [(5, e5), (7, e7)]
    n = 5 ** e5 * 7 ** e7
    p, cofactor, certificate = certified_prime(n, rng)
    E, P, Q = torsion_basis(p, n, cofactor, rng)
    # Public P,Q are chosen before the secret, hence carry no secret slope.
    s = rng.randrange(n)
    R = E.add(P, E.mul(s, Q))
    j = quotient_j(E, R, factors)

    # Deliberately use a primitive hidden vector with neither coordinate a unit
    # over the composite ring. Local projective coordinates still exist.
    v = [5 * unit(rng, n) % n, 7 * unit(rng, n) % n]
    while True:
        w = [rng.randrange(n), rng.randrange(n)]
        V = [[v[0], w[0]], [v[1], w[1]]]
        if math.gcd(det2(V, n), n) == 1:
            break
    a, d = rng.randrange(n), unit(rng, n)
    W = [[1, a], [s, (s * a + d) % n]]
    M = mul(W, inverse2(V, n), n)  # M*v = (1,s).
    Acoords = [M[0][0], M[1][0]] + [rng.randrange(n) for _ in range(3)]
    Bcoords = [M[0][1], M[1][1]] + [rng.randrange(n) for _ in range(3)]

    base = free_lie_representation(n)
    while True:
        S = [[rng.randrange(n) for _ in range(15)] for _ in range(15)]
        try:
            Sinv = inverse_unit_pivots(S, n)
            break
        except ValueError:
            pass
    hidden_basis = [mul(mul(S, b, n), Sinv, n) for b in base]

    def encode(coords):
        return exp_nilpotent(combine(coords, hidden_basis, n), n)

    def random_lift(m):
        x = [m[0][0] % n, m[1][0] % n] + [rng.randrange(n) for _ in range(3)]
        y = [m[0][1] % n, m[1][1] % n] + [rng.randrange(n) for _ in range(3)]
        return automorphism_columns(x, y, n)

    actions = {}
    for name, matrix in [('frobenius_p', [[1, 0], [0, -1]]),
                         ('cm_i', [[0, -1], [1, 0]])]:
        lift = random_lift(matrix)
        actions[name] = [encode(apply_columns(lift, g, n)) for g in (Acoords, Bcoords)]

    # log([exp(x),exp(y)]) = z + (u+v)/2. A common unknown
    # basepoint change adds wx*u+wy*v. Further transports are in the cover.
    half = pow(2, -1, n)
    c0, c1 = (half + rng.randrange(n)) % n, (half + rng.randrange(n)) % n
    t0 = rng.randrange(n)
    transports = [t0, (t0 + unit(rng, n)) % n]
    transports += [rng.randrange(n) for _ in range(8)]
    packets = []
    for t in transports:
        power = unit(rng, n)
        log_cusp = [0, 0, power, power * (c0 + t) % n,
                    power * (c1 + t * s) % n]
        packets.append(encode(log_cusp))

    # AES-GCM nonce need not be secret. SystemRandom is used in production;
    # the injectable RNG exists only for deterministic organizer tests.
    nonce = bytes(rng.randrange(256) for _ in range(12))
    ciphertext = AESGCM(key_from_j(j)).encrypt(nonce, flag, AAD)
    public = {
        'version': VERSION,
        'modulus': n,
        'factors': [[ell, e] for ell, e in factors],
        'field': {'p': p, 'extension': 'i^2+1', 'prime_certificate': certificate},
        'curve': {'a': [1, 0], 'b': [0, 0], 'P': encode_point(P), 'Q': encode_point(Q)},
        'generators': [encode(Acoords), encode(Bcoords)],
        'class_two_outer_lifts': actions,
        'cuspidal_packet': packets,
        'seal': {'algorithm': 'AES-256-GCM', 'nonce': nonce.hex(),
                 'ciphertext_and_tag': ciphertext.hex(), 'aad': AAD.hex()},
    }
    private = {'secret_slope': s, 'marking': M, 'hidden_line_vector': v,
               'target_j': j.pair(), 'flag': flag.decode('ascii')}
    return public, private


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--flag-file', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--private-json', type=Path,
                    help='optional organizer-only diagnostics; never distribute')
    ap.add_argument('--e5', type=int, default=64)
    ap.add_argument('--e7', type=int, default=48)
    args = ap.parse_args()
    if args.out.exists() or (args.private_json and args.private_json.exists()):
        ap.error('refusing to overwrite an existing output')
    if args.private_json and args.out.resolve() == args.private_json.resolve():
        ap.error('public and private paths must be different')
    flag = args.flag_file.read_bytes().rstrip(b'\r\n')
    start = time.perf_counter()
    public, private = make_instance(flag, args.e5, args.e7)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(public, separators=(',', ':')) + '\n', encoding='utf-8')
    if args.private_json:
        args.private_json.parent.mkdir(parents=True, exist_ok=True)
        # Restrict permission before writing any diagnostic secret.
        import os
        fd = os.open(args.private_json, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(private, f, indent=2)
            f.write('\n')
    print(f'created {args.out}; p={public["field"]["p"].bit_length()} bits; '
          f'N={public["modulus"].bit_length()} bits; '
          f'time={time.perf_counter()-start:.3f}s')


if __name__ == '__main__':
    main()
