#!/usr/bin/env python3
from ast import literal_eval
from math import gcd
from pathlib import Path


def long_to_bytes(value: int) -> bytes:
    return value.to_bytes((value.bit_length() + 7) // 8, "big")


values = {}
for line in Path("RSAisEasy/output.txt").read_text().splitlines():
    name, value = line.split(": ", 1)
    values[name] = literal_eval(value)

n1 = values["n1"]
c1 = values["c1"]
c2 = values["c2"]
leak = values["(n1 * E) + n2"]
e = 0x10001

# leak = n1 * E + n2, while n1 = p*q and n2 = q*z.
# Therefore gcd(n1, leak) = gcd(n1, n2) = q.
q = gcd(n1, leak)
p = n1 // q
n2 = leak % n1
z = n2 // q

phi1 = (p - 1) * (q - 1)
phi2 = (q - 1) * (z - 1)
m1 = pow(c1, pow(e, -1, phi1), n1)
m2 = pow(c2, pow(e, -1, phi2), n2)

print(long_to_bytes(m1).decode() + long_to_bytes(m2).decode())
