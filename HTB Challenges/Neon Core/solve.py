#!/usr/bin/env python3
"""Chosen-plaintext solver for HTB Neon Core (no Sage dependency)."""

import re
import socket

HOST, PORT = "154.57.164.71", 30389
P = 257


def recvuntil(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise EOFError("server closed the connection")
        data += chunk
    return data


def parse_block(s):
    """Decode 16 fields; 0..255 use 2 hex digits while 256 is '100'."""
    answers = []

    def walk(pos, vals):
        if len(vals) == 16:
            if pos == len(s):
                answers.append(vals)
            return
        left = 16 - len(vals)
        if not (2 * left <= len(s) - pos <= 3 * left):
            return
        if s.startswith("100", pos):
            walk(pos + 3, vals + [256])
        if pos + 2 <= len(s):
            walk(pos + 2, vals + [int(s[pos:pos + 2], 16)])

    walk(0, [])
    if not answers:
        raise ValueError(f"cannot parse ciphertext block {s!r}")
    return answers[0]


def solve_linear(a, b):
    """Solve A*x=b modulo P by Gauss-Jordan elimination."""
    m = [[a[r][c] % P for c in range(16)] + [b[r] % P] for r in range(16)]
    for col in range(16):
        pivot = next(r for r in range(col, 16) if m[r][col])
        m[col], m[pivot] = m[pivot], m[col]
        inv = pow(m[col][col], -1, P)
        m[col] = [(v * inv) % P for v in m[col]]
        for r in range(16):
            if r != col and m[r][col]:
                q = m[r][col]
                m[r] = [(m[r][j] - q * m[col][j]) % P for j in range(17)]
    return [m[r][16] for r in range(16)]


def main():
    with socket.create_connection((HOST, PORT)) as sock:
        recvuntil(sock, b"> ")

        def encrypt_raw(msg):
            sock.sendall(b"1\n")
            recvuntil(sock, b"raw text): ")
            sock.sendall(msg + b"\n")
            out = recvuntil(sock, b"> ")
            return re.search(rb"Ciphertext \(hex\): ([0-9a-f]+)", out).group(1).decode()

        # Empty input encrypts one full PKCS#7 padding block. Every 16-byte
        # chosen message appends that identical block, giving an unambiguous
        # delimiter despite the server's variable-width encoding of field 256.
        padding_hex = encrypt_raw(b"")

        def encrypt(msg):
            hx = encrypt_raw(msg)
            if not hx.endswith(padding_hex):
                raise ValueError("unexpected padding block")
            return parse_block(hx[:-len(padding_hex)])

        base = b"A" * 16
        y0 = encrypt(base)
        delta = (pow(ord("B"), 3, P) - pow(ord("A"), 3, P)) % P
        inv_delta = pow(delta, -1, P)
        columns = []
        for i in range(16):
            msg = bytearray(base)
            msg[i] = ord("B")
            yi = encrypt(bytes(msg))
            columns.append([((yi[r] - y0[r]) * inv_delta) % P for r in range(16)])
        a = [[columns[c][r] for c in range(16)] for r in range(16)]

        sock.sendall(b"2\n")
        out = recvuntil(sock, b"> ")
        flag_hex = re.search(rb"Encrypted configuration \([^)]*\): ([0-9a-f]+)", out).group(1).decode()

        def candidates(pos, plaintext):
            if pos == len(flag_hex):
                if plaintext.startswith(b"HTB{") and plaintext:
                    n = plaintext[-1]
                    if 1 <= n <= 16 and plaintext.endswith(bytes([n]) * n):
                        return plaintext[:-n]
                return None
            for size in range(32, min(49, len(flag_hex) - pos + 1)):
                try:
                    y = parse_block(flag_hex[pos:pos + size])
                    rhs = [(y[r] - y0[r]) % P for r in range(16)]
                    diff = solve_linear(a, rhs)
                    cubes = [(diff[i] + pow(base[i], 3, P)) % P for i in range(16)]
                    block = bytes(pow(v, 171, P) for v in cubes)
                except (ValueError, StopIteration, OverflowError):
                    continue
                combined = plaintext + block
                if pos == 0 and not b"HTB{".startswith(combined[:4]):
                    continue
                result = candidates(pos + size, combined)
                if result is not None:
                    return result
            return None

        plaintext = candidates(0, b"")
        if plaintext is None:
            raise ValueError("no valid HTB flag decryption found")
        print(plaintext.decode())


if __name__ == "__main__":
    main()
