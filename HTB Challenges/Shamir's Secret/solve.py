#!/usr/bin/env python3
import ast
import math
import socket


HOST = "154.57.164.73"
PORT = 32374
N = 1 << 1024


def recv_until(sock, marker):
    data = bytearray()
    while marker not in data:
        chunk = sock.recv(65536)
        if not chunk:
            raise EOFError("server closed the connection")
        data.extend(chunk)
    return bytes(data)


def get_encryption(sock, option, message=None):
    sock.sendall(f"{option}\n".encode())
    if message is not None:
        recv_until(sock, b"Input message as hex: ")
        sock.sendall(message.hex().encode() + b"\n")
    response = recv_until(sock, b"> ")
    pairs = []
    for line in response.splitlines():
        line = line.strip()
        if line.startswith(b"("):
            pairs.append(ast.literal_eval(line.decode()))
    if len(pairs) != 64:
        raise ValueError(f"expected 64 pairs, received {len(pairs)}")
    return pairs


def v2(value):
    if value == 0:
        return 1024
    return (abs(value) & -abs(value)).bit_length() - 1


def recover_constant(points):
    # L_i(0) = product(-x_j) / product(x_i-x_j).  Work modulo 2^1024,
    # clearing only the largest power-of-two denominator. Odd denominators
    # are units and can be inverted directly.
    terms = []
    max_den_power = 0
    for i, (xi, _) in enumerate(points):
        numerator = 1
        denominator = 1
        for j, (xj, _) in enumerate(points):
            if i != j:
                numerator *= -xj
                denominator *= xi - xj
        shift = v2(numerator) - v2(denominator)
        max_den_power = max(max_den_power, -shift)
        terms.append((numerator, denominator, shift))

    modulus = N
    total = 0
    for (_, y), (num, den, _) in zip(points, terms):
        num_twos, den_twos = v2(num), v2(den)
        odd_num = num >> num_twos
        odd_den = den >> den_twos
        power = max_den_power + num_twos - den_twos
        coefficient = (odd_num % modulus) * pow(odd_den % modulus, -1, modulus)
        coefficient = (coefficient << power) % modulus
        total = (total + coefficient * y) % modulus

    if total % (1 << max_den_power):
        raise ValueError("interpolation result is not divisible as expected")
    reduced_modulus = 1 << (1024 - max_den_power)
    message = (total >> max_den_power) % reduced_modulus
    return message, max_den_power


def main():
    with socket.create_connection((HOST, PORT), timeout=20) as sock:
        recv_until(sock, b"> ")
        flag_encryption = get_encryption(sock, 1)

        candidates = set(range(64))
        rounds = 0
        while len(candidates) > 32 and rounds < 180:
            sample = get_encryption(sock, 2, b"\x00")
            candidates = {
                i for i in candidates
                if not (sample[i][0] % 2 == 0 and sample[i][1] % 2 == 1)
            }
            rounds += 1
            if rounds % 20 == 0:
                print(f"round {rounds}: {len(candidates)} mask candidates", flush=True)

    if len(candidates) != 32:
        raise RuntimeError(f"mask recovery left {len(candidates)} candidates")
    print(f"recovered genuine positions: {sorted(candidates)}")
    points = [flag_encryption[i] for i in sorted(candidates)]
    value, lost_bits = recover_constant(points)
    raw = value.to_bytes((value.bit_length() + 7) // 8, "big")
    print(f"lost {lost_bits} high-modulus bits; recovered {1024-lost_bits} low bits")
    print(raw)
    start = raw.find(b"HTB{")
    end = raw.find(b"}", start)
    if start >= 0 and end >= 0:
        print(raw[start:end + 1].decode())


if __name__ == "__main__":
    main()
