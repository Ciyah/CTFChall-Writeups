#!/usr/bin/env python3
import ast
import hashlib
import math
import random
import re
import socket

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HOST = "154.57.164.67"
PORT = 30759
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
BOUND = 8748541127929402731638
INF = None

# The six possible orders of j=0 curves over this field.
ORDERS = [
    115792089237316195423570985008687907852837564279074904382605163141518161494337,
    115792089237316195423570985008687907853702405052206223696310004874299507848991,
    115792089237316195423570985008687907852598652813156864395638497411212089444244,
    115792089237316195423570985008687907853508896131558604026424249738214906721757,
    115792089237316195423570985008687907853031073199722524052490918277602762621571,
    115792089237316195423570985008687907853941316518124263683276670604605579899084,
]

# Enough pairwise-coprime factors to uniquely identify a key below BOUND.
WANTED = [3319, 22639, 20412485227, 199, 18979]


def inv(x):
    return pow(x % P, -1, P)


def add(u, v):
    if u is INF:
        return v
    if v is INF:
        return u
    x1, y1 = u
    x2, y2 = v
    if x1 == x2 and (y1 + y2) % P == 0:
        return INF
    if u == v:
        lam = 3 * x1 * x1 * inv(2 * y1) % P
    else:
        lam = (y2 - y1) * inv(x2 - x1) % P
    x3 = (lam * lam - x1 - x2) % P
    return x3, (lam * (x1 - x3) - y1) % P


def mul(k, point):
    out = INF
    while k:
        if k & 1:
            out = add(out, point)
        point = add(point, point)
        k >>= 1
    return out


def random_point(b):
    while True:
        x = random.randrange(P)
        rhs = (x * x * x + b) % P
        y = pow(rhs, (P + 1) // 4, P)
        if y * y % P == rhs and y:
            return x, y


def identify_curve_and_point(q):
    """Find a curve y^2=x^3+b and a point of exact prime order q."""
    for b in range(1, 100):
        r = random_point(b)
        order = next((n for n in ORDERS if mul(n, r) is INF), None)
        if order is None or order % q:
            continue
        point = mul(order // q, r)
        if point is not INF and mul(q, point) is INF:
            return point
    raise RuntimeError(f"could not make point of order {q}")


def bsgs(g, h, order):
    if h is INF:
        return 0
    m = math.isqrt(order) + 1
    table = {}
    cur = INF
    for j in range(m):
        table.setdefault(cur, j)
        cur = add(cur, g)
    step = mul(m, g)
    step = INF if step is INF else (step[0], (-step[1]) % P)
    cur = h
    for i in range(m + 1):
        if cur in table:
            ans = i * m + table[cur]
            if ans < order:
                return ans
        cur = add(cur, step)
    raise RuntimeError("discrete log not found")


def crt(residues, moduli):
    x, modulus = 0, 1
    for residue, q in zip(residues, moduli):
        t = ((residue - x) * pow(modulus, -1, q)) % q
        x += modulus * t
        modulus *= q
    return x, modulus


class Tube:
    def __init__(self):
        self.s = socket.create_connection((HOST, PORT), timeout=15)
        self.buf = b""

    def until(self, marker):
        marker = marker.encode()
        while marker not in self.buf:
            chunk = self.s.recv(4096)
            if not chunk:
                raise EOFError(self.buf)
            self.buf += chunk
        pos = self.buf.index(marker) + len(marker)
        out, self.buf = self.buf[:pos], self.buf[pos:]
        return out.decode()

    def sendline(self, value):
        self.s.sendall(str(value).encode() + b"\n")


def oracle_point(tube, point):
    tube.until("> ")
    tube.sendline(1)
    tube.until("Enter your point x,y: ")
    tube.sendline(f"{point[0]},{point[1]}")
    reply = tube.until("Public Key: ")
    tail = tube.until("\n")[:-1].strip()
    # The marker can refer to the initial key only if protocol synchronization
    # changes; normally this is "Here's your new Public Key: ...".
    if tail == "Origin":
        return INF
    return tuple(ast.literal_eval(tail))


def quantum_query(tube, private):
    rng = random.Random(private)
    bases = ''.join('Z' if rng.randint(0, 1) else 'X' for _ in range(256))
    tube.until("> ")
    tube.sendline(2)
    tube.until("Choose your 256 basis for the KEP: ")
    tube.sendline(bases)
    data = tube.until("Flag Encrypted: ")
    ciphertext = bytes.fromhex(tube.until("\n")[:-1].strip())
    match = re.search(r"The Quantum key: ([0-9a-f]{64})", data)
    if not match:
        raise RuntimeError(f"quantum key missing from response: {data!r}")
    user_bits = ''.join(f'{x:08b}' for x in bytes.fromhex(match.group(1)))
    # The prepared state is |psi->; equal-basis measurements are opposite.
    server_bits = ''.join('1' if bit == '0' else '0' for bit in user_bits)
    raw = bytes(int(server_bits[i:i + 8], 2) for i in range(0, 256, 8))
    key = hashlib.sha256(raw).digest()
    decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    return padded[:-padded[-1]].decode()


def main():
    points = [(q, identify_curve_and_point(q)) for q in WANTED]
    tube = Tube()
    banner = tube.until("Public Key: ") + tube.until("\n")
    print(banner.strip())
    residues = []
    for q, point in points:
        result = oracle_point(tube, point)
        residue = bsgs(point, result, q)
        residues.append(residue)
        print(f"private mod {q} = {residue}")
    private, modulus = crt(residues, WANTED)
    assert modulus > BOUND and private < BOUND
    print(f"private_key = {private}")
    print(quantum_query(tube, private))


if __name__ == "__main__":
    main()
