#!/usr/bin/env python3
"""Solve Baby Time Capsule with Hastad's broadcast attack."""

import argparse
import json
import math
import socket


def recv_until(sock: socket.socket, marker: bytes) -> bytes:
    data = bytearray()
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("server closed the connection")
        data.extend(chunk)
    return bytes(data)


def crt(residues: list[int], moduli: list[int]) -> int:
    modulus = math.prod(moduli)
    result = 0
    for residue, n in zip(residues, moduli):
        partial = modulus // n
        result = (result + residue * partial * pow(partial, -1, n)) % modulus
    return result


def integer_nth_root(value: int, degree: int) -> tuple[int, bool]:
    low, high = 0, 1
    while high**degree <= value:
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**degree <= value:
            low = middle
        else:
            high = middle
    return low, low**degree == value


def solve(host: str, port: int) -> bytes:
    ciphertexts: list[int] = []
    moduli: list[int] = []

    with socket.create_connection((host, port), timeout=10) as sock:
        for _ in range(5):
            recv_until(sock, b"(Y/n) ")
            sock.sendall(b"Y\n")
            response = recv_until(sock, b"\n").splitlines()[0]
            capsule = json.loads(response)
            ciphertexts.append(int(capsule["time_capsule"], 16))
            moduli.append(int(capsule["pubkey"][0], 16))

    # CRT returns m^5 without modular wraparound because the combined modulus
    # is roughly 5120 bits, much larger than a normal flag raised to the fifth.
    fifth_power = crt(ciphertexts, moduli)
    message, exact = integer_nth_root(fifth_power, 5)
    if not exact:
        raise ValueError("fifth root was not exact; collect more coprime samples")
    return message.to_bytes((message.bit_length() + 7) // 8, "big")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", nargs="?", default="154.57.164.75")
    parser.add_argument("port", nargs="?", type=int, default=30142)
    args = parser.parse_args()
    print(solve(args.host, args.port).decode())
