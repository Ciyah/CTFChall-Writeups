#!/usr/bin/env python3
import itertools, json, math, re, socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from sympy.ntheory.modular import crt
from sympy.ntheory.residue_ntheory import sqrt_mod

HOST, PORT = "154.57.164.71", 32734
EXPS = [65537, 4001, 11093, 7727, 32189, 19373, 8192, 7867, 599741, 919, 3697, 227, 9613]

s = socket.create_connection((HOST, PORT))
f = s.makefile("rwb", buffering=0)

def until(marker):
    data = b""
    while marker not in data:
        chunk = f.read(1)
        if not chunk:
            raise EOFError(data)
        data += chunk
    return data

def send(obj):
    f.write(json.dumps(obj).encode() + b"\n")

until(b"Option (json format) :: ")
keys = []
for i, e in enumerate(EXPS):
    send({"option": "1"})
    until(b"(json format) :: ")
    send({"choice": i})
    out = until(b"Option (json format) :: ")
    match = re.search(rb'\{"N".*?\}', out)
    row = json.loads(match.group())
    keys.append((row["N"], e, row["encrypted_passcode"], row["phi"]))

for i, (n, e, c, phi) in enumerate(keys):
    for j, (n2, _, _, _) in enumerate(keys[:i]):
        p = math.gcd(n, n2)
        if p != 1:
            q = n // p
            ph = (p - 1) * (q - 1)
            if math.gcd(e, ph) == 1:
                m = pow(c, pow(e, -1, ph), n)
                print("shared factor", i, j, "passcode", m.to_bytes((m.bit_length()+7)//8, "big").hex())

# Key 6 leaks phi(N), and e=8192=2^13. Factor N, then undo the
# exponent as thirteen successive modular square-root operations.
n, e, c, phi = keys[6]
sum_pq = n - phi + 1
disc = math.isqrt(sum_pq * sum_pq - 4 * n)
p, q = (sum_pq + disc) // 2, (sum_pq - disc) // 2
assert p*q == n

def repeated_roots(value, prime, rounds=13):
    vals = {value % prime}
    for _ in range(rounds):
        vals = {int(r) for v in vals for r in sqrt_mod(v, prime, all_roots=True)}
    return vals

rp, rq = repeated_roots(c, p), repeated_roots(c, q)
print("root counts", len(rp), len(rq))
for a in rp:
    for b in rq:
        m = int(crt((p, q), (a, b))[0])
        raw = m.to_bytes((m.bit_length()+7)//8, "big")
        if 4 <= len(raw) <= 64 and all(32 <= x < 127 for x in raw):
            print("candidate", raw, raw.hex())

passcode = b"s3cr3t"

def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def blshift(a, b):
    return bytes((((x % 2**((8-y)%8)) << y) | (x >> ((8-y)%8))) & 0xff
                 for x, y in zip(a, b))

def pad(message):
    bitlen = 8 * len(message) & 0xffffffffffffffff
    message += b"\x80"
    while len(message) % 32 != 28:
        message += b"\0"
    return message + bitlen.to_bytes(4, "big")

def compress(seed, previous, block):
    enc = Cipher(algorithms.AES(block), modes.ECB()).encryptor()
    return bxor(enc.update(blshift(seed, previous)) + enc.finalize(), seed)

# Obtain the genuine keyed-hash state. A 10-byte message avoids rxor's loop;
# its zero bytes also make the faulty single-bit mask harmless.
oracle_msg = passcode + b"\0" * 4
send({"option": "2"})
until(b"(json format) :: ")
send({"hash": oracle_msg.hex()})
out = until(b"Option (json format) :: ")
H = bytes.fromhex(re.search(rb'\{"hash": "([0-9a-f]+)"\}', out).group(1).decode())
print("oracle state", H.hex())

# Make the answer finish the oracle message and inject its MD padding.
prefix_len = 48 + 16 + len(oracle_msg)
padded_oracle = pad(b"\0" * prefix_len)
glue = padded_oracle[prefix_len:]
answer = oracle_msg[len(passcode):] + glue

send({"option": "3"})
until(b"(json format) :: ")
send({"passcode": passcode.hex()})
until(b"(json format) :: ")
send({"answer": answer.hex()})
token_prompt = until(b"(json format) :: ")
token = bytes.fromhex(re.search(rb'token = ([0-9a-f]+)', token_prompt).group(1).decode())
print("target token", token.hex())

# Continue from H and brute-force the 5 random characters offline.
block_a = b"\0" * 12 + (40).to_bytes(4, "big")
state_a = compress(H, padded_oracle[-16:], block_a)
total_before_final_pad = len(padded_oracle) + 32
final_glue = pad(b"\0" * total_before_final_pad)[total_before_final_pad:]
final_blocks = [final_glue[i:i+16] for i in range(0, len(final_glue), 16)]
alphabet = sorted(set("+%2$?!_8*469"))
found = None
for chars in itertools.product(alphabet, repeat=5):
    candidate = ''.join(chars).encode()
    block_b = candidate + b"\x80" + b"\0" * 10
    state = compress(state_a, block_a, block_b)
    previous = block_b
    for block in final_blocks:
        state = compress(state, previous, block)
        previous = block
    if state == token:
        found = candidate
        break

assert found is not None
print("2FA random value", found)
send({"token": found.hex()})
result = b""
while True:
    chunk = f.read(4096)
    if not chunk:
        break
    result += chunk
print(result.decode(errors="replace"))
