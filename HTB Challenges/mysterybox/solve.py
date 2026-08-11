#!/usr/bin/env python3
import math
import re
import socket

HOST = "154.57.164.77"
PORT = 32156
TARGET_BYTES = b"Username: Admin, Access code: CryptoBestCategoryF3"
TARGET = int.from_bytes(TARGET_BYTES, "big")


class Conn:
    def __init__(self, host, port):
        self.s = socket.create_connection((host, port))
        self.buf = b""

    def until(self, marker):
        while marker not in self.buf:
            chunk = self.s.recv(4096)
            if not chunk:
                raise EOFError(self.buf.decode(errors="replace"))
            self.buf += chunk
        end = self.buf.index(marker) + len(marker)
        out, self.buf = self.buf[:end], self.buf[end:]
        return out

    def sendline(self, value):
        self.s.sendall(str(value).encode() + b"\n")

    def sign(self, message):
        self.until(b"Enter your option: ")
        self.sendline(1)
        self.until(b"Enter your message to be signed in hex: ")
        self.sendline(message.to_bytes((message.bit_length() + 7) // 8 or 1, "big").hex())
        line = self.until(b"\n")
        match = re.search(rb"Signature for \d+: (\d+)", line)
        if not match:
            raise RuntimeError(line.decode(errors="replace"))
        return int(match.group(1))

    def verify(self, message, signature):
        self.until(b"Enter your option: ")
        self.sendline(2)
        self.until(b"Enter your message in hex: ")
        self.sendline(message.to_bytes((message.bit_length() + 7) // 8, "big").hex())
        self.until(b"Enter your signature in hex: ")
        self.sendline(signature.to_bytes((signature.bit_length() + 7) // 8, "big").hex())
        return self.until(b"\n").decode().strip()


def main():
    c = Conn(HOST, PORT)

    # If S(m) = m^d mod n, then S(x)^k - S(x^k) is a multiple of n.
    relations = []
    for x, k in ((2, 2), (2, 3), (3, 2)):
        sx = c.sign(x)
        sxk = c.sign(x**k)
        relations.append(abs(pow(sx, k) - sxk))
    n = math.gcd(*relations)
    if n.bit_length() > 1030:
        raise RuntimeError(f"modulus recovery left an extra factor ({n.bit_length()} bits)")

    # S(T*r) / S(r) = S(T) mod n by RSA's multiplicative property.
    r = 2
    sr = c.sign(r)
    str_ = c.sign(TARGET * r)
    forged = str_ * pow(sr, -1, n) % n
    print(f"recovered n ({n.bit_length()} bits): {n}")
    print(f"forged signature: {forged}")
    print(c.verify(TARGET, forged))


if __name__ == "__main__":
    main()
