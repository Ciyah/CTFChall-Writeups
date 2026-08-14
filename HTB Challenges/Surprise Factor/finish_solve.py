#!/usr/bin/env python3
import itertools
import json
import socket
import sys

sys.path.insert(0, "Surprise Factor/crypto_surprise_factor")
from ec import G, N, scalar_mul, to_affine

HOST, PORT = "154.57.164.82", 30129

FACTORS = [
    3,
    349,
    1545773,
    6672923,
    1392212131,
    2909631091,
    4518664483,
    9622480222084166579,
    82889966717512745654064507380623,
    77341036545436718519905601418108235101550616001554018653,
]


def send(payload):
    with socket.create_connection((HOST, PORT), timeout=15) as sock:
        f = sock.makefile("rwb")
        f.write(json.dumps(payload).encode() + b"\n")
        f.flush()
        return json.loads(f.readline())


with open("sample.json", encoding="ascii") as f:
    sample = json.load(f)
h, r, s = (int(sample[name], 0) for name in ("hash", "r", "s"))
qx = int(sample["public_key"]["x"], 0)
qy = int(sample["public_key"]["y"], 0)

product = 1
for factor in FACTORS:
    product *= factor

for mask in range(1 << len(FACTORS)):
    k = 1
    for i, factor in enumerate(FACTORS):
        if mask >> i & 1:
            k *= factor
    if not (1 <= k < N) or not (1 <= product // k < N):
        continue
    point = to_affine(scalar_mul(k, G))
    if point is None or point[0] % N != r:
        continue
    d = ((s * k - h) * pow(r, -1, N)) % N
    if to_affine(scalar_mul(d, G)) != (qx, qy):
        continue
    print("nonce =", hex(k))
    print("private key =", hex(d))
    print(send({"action": "submit", "d": hex(d)}))
    break
else:
    raise SystemExit("no nonce/private-key candidate matched")
