#!/usr/bin/env python3
"""Reproduce key recovery from the supplied Wine core and recorded trace data.

Usage: python3 recover_keys.py [after-check.dump.56803]
No third-party Python packages are required. This reproduces the algebra after
tracing; it does not automatically unpack or instrument the original executable.
"""
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parent
BASE = 0x140000000


def extract_image(path):
    data = path.read_bytes()
    assert data[:6] == b'\x7fELF\x02\x01', 'Expected a little-endian ELF64 core'
    phoff = struct.unpack_from('<Q', data, 32)[0]
    entsize, count = struct.unpack_from('<HH', data, 54)
    image = bytearray(0x5161000)
    for i in range(count):
        typ, flags, offset, address, _, size, _, _ = struct.unpack_from(
            '<IIQQQQQQ', data, phoff + i * entsize)
        if typ == 1 and BASE <= address < BASE + len(image):
            rva = address - BASE
            image[rva:rva + size] = data[offset:offset + size]
    return image


def solve_square(matrix, targets, prime):
    n = len(targets)
    rows = [list(row) + [target] for row, target in zip(matrix, targets)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if rows[i][col] % prime)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        inverse = pow(rows[col][col], -1, prime)
        rows[col] = [x * inverse % prime for x in rows[col]]
        for i in range(n):
            if i != col:
                factor = rows[i][col]
                rows[i] = [(x - factor * y) % prime
                           for x, y in zip(rows[i], rows[col])]
    return [row[-1] for row in rows]


def discrete_log(base, target, prime):
    width = math.isqrt(prime - 1) + 1
    baby, value = {}, 1
    for j in range(width):
        baby.setdefault(value, j)
        value = value * base % prime
    factor = pow(pow(base, width, prime), -1, prime)
    value = target
    for i in range(width + 1):
        if value in baby:
            answer = i * width + baby[value]
            assert pow(base, answer, prime) == target
            return answer
        value = value * factor % prime
    raise ValueError('No discrete logarithm found')


def main():
    core = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'after-check.dump.56803'
    image = extract_image(core)
    trace = json.loads((ROOT / 'solve_artifacts/trace_data.json').read_text())
    sbox = image[0x1137500:0x1137600]
    assert len(set(sbox)) == 256
    inverse_sbox = {value: i for i, value in enumerate(sbox)}

    key1 = bytes((target - 128 * i - 89) * pow(115, -1, 256) % 256
                 for i, target in enumerate(trace['key1_targets']))

    previous, key2 = 250, bytearray()
    for i, target in enumerate(trace['key2_targets']):
        value = inverse_sbox[target]
        key2.append((value - 181 * previous - 89 * i) % 256)
        previous = value

    state = list(image[0x1137600:0x1137608])
    permutation = image[0x1137608:0x1137610]
    round_keys = image[0x1137610:0x1137614]
    for round_key in reversed(round_keys):
        before_permutation = [0] * 8
        for i, j in enumerate(permutation):
            before_permutation[j] = state[i]
        state = [(inverse_sbox[value] - round_key) % 256
                 for value in before_permutation]
    key3 = bytes(state)

    coefficients, targets = trace['key4_coefficients'], trace['key4_targets']
    transformed = solve_square(coefficients[:23], targets[:23], 7681)
    assert all(0 <= x < 256 for x in transformed)
    key4 = bytes(inverse_sbox[(inverse_sbox[value] - 75) % 256]
                 for value in transformed)
    residuals = [(sum(a * x for a, x in zip(row, transformed)) - target) % 7681
                 for row, target in zip(coefficients, targets)]
    assert all(x == 0 for x in residuals[:23])
    assert all(min(x, 7681 - x) <= 2 for x in residuals[23:])

    key5 = str(discrete_log(3, 847494038, 1607920157)).encode()
    # Obtained by the separate AVX2 search in search_nonce.c.
    nonce = 3923306276
    keys = [key1, bytes(key2), key3, key4, key5, str(nonce).encode()]
    digest = hashlib.blake2s(b''.join(keys[:5]) + struct.pack('<Q', nonce)).digest()
    assert digest[:4] == bytes(4)
    for i, key in enumerate(keys, 1):
        print(f'Key {i}: {key.decode("ascii")}')
    print(f'BLAKE2s: {digest.hex()}')
    print('Key 4 residuals:', [x if x <= 3840 else x - 7681 for x in residuals])


if __name__ == '__main__':
    main()
