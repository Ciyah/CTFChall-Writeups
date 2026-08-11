#!/usr/bin/env python3
import hashlib
import math
import re
import socket

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from sympy import factorint


HOST = "154.57.164.82"
PORT = 32762


def long_to_bytes(value):
    return value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")


def recv_until(sock, marker=b"> "):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise EOFError("server closed the connection")
        data += chunk
    return data


def bsgs(g, y, p, order):
    """Return x such that g**x == y (mod p), for a group of known order."""
    m = math.isqrt(order) + 1
    table = {}
    value = 1
    for j in range(m):
        table.setdefault(value, j)
        value = value * g % p

    stride = pow(pow(g, m, p), -1, p)
    gamma = y
    for i in range(m + 1):
        if gamma in table:
            x = i * m + table[gamma]
            if x < order and pow(g, x, p) == y:
                return x
        gamma = gamma * stride % p
    raise ValueError("discrete logarithm not found")


def main():
    with socket.create_connection((HOST, PORT)) as sock:
        recv_until(sock)
        sock.sendall(b"1\n")
        params_text = recv_until(sock).decode()
        values = dict((k, int(v)) for k, v in re.findall(r"^(p|g|A|B) = (\d+)$", params_text, re.M))
        p, g, A, B = (values[k] for k in ("p", "g", "A", "B"))

        # p - 1 = 2*q*r. The unique small odd factor is the subgroup order q.
        factors = factorint(p - 1)
        candidates = [int(f) for f in factors if 2**41 <= f < 2**42]
        if len(candidates) != 1:
            raise ValueError(f"could not identify q from factors: {factors}")
        q = candidates[0]

        a_mod_q = bsgs(g, A, p, q)
        shared_secret = pow(B, a_mod_q, p)

        sock.sendall(b"3\n")
        flag_text = recv_until(sock).decode()
        ciphertext = bytes.fromhex(re.search(r"encrypted = ([0-9a-f]+)", flag_text).group(1))
        key = hashlib.sha256(long_to_bytes(shared_secret)).digest()[:16]
        padded = Cipher(algorithms.AES(key), modes.ECB()).decryptor().update(ciphertext)
        unpadder = PKCS7(128).unpadder()
        flag = unpadder.update(padded) + unpadder.finalize()
        print(flag.decode())


if __name__ == "__main__":
    main()
