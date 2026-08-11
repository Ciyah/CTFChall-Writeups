#!/usr/bin/env python3
import json
import socket
import sys


HOST = sys.argv[1] if len(sys.argv) > 1 else "154.57.164.67"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 32369
BS = 16


class Client:
    def __init__(self, host, port):
        self.s = socket.create_connection((host, port))
        self.buf = b""
        self.until(b"> ")

    def until(self, marker):
        while marker not in self.buf:
            chunk = self.s.recv(4096)
            if not chunk:
                raise EOFError(self.buf.decode(errors="replace"))
            self.buf += chunk
        out, self.buf = self.buf.split(marker, 1)
        return out

    def line(self, value):
        self.s.sendall(str(value).encode() + b"\n")

    def login_password(self):
        self.line(1)
        self.until(b"Send your credentials: ")
        self.line(json.dumps({"token": "", "username": "D-Cryp7", "password": "Cryp70Gr47Hy!"}))
        out = self.until(b"> ")
        token = out.split(b"Token: ", 1)[1].splitlines()[0]
        return bytes.fromhex(token.decode())

    def encrypted_data(self):
        self.line(2)
        out = self.until(b"> ")
        value = out.split(b"Encrypted data: ", 1)[1].splitlines()[0]
        return bytes.fromhex(value.decode())

    def oracle(self, value):
        self.line(1)
        self.until(b"Send your credentials: ")
        self.line(json.dumps({"token": value.hex()}))
        out = self.until(b"> ")
        return b"Decryption error!" not in out

    def oracle_batch(self, values):
        wire = b"".join(
            b"1\n" + json.dumps({"token": value.hex()}).encode() + b"\n"
            for value in values
        )
        self.s.sendall(wire)
        answers = []
        for _ in values:
            self.until(b"Send your credentials: ")
            out = self.until(b"> ")
            answers.append(b"Decryption error!" not in out)
        return answers

    def withdraw(self, card, amount):
        self.line(3)
        self.until(b"Insert your card number: ")
        self.line(card)
        self.until(b"Quantity: ")
        self.line(amount)
        return self.until(b"> ").decode(errors="replace")


def intermediate(client, block):
    """Recover AES-decrypt(block) with a two-block padding-oracle query."""
    crafted = bytearray(BS)
    result = bytearray(BS)
    for pos in range(BS - 1, -1, -1):
        padding = BS - pos
        for j in range(pos + 1, BS):
            crafted[j] = result[j] ^ padding
        probes = []
        for guess in range(256):
            candidate = bytearray(crafted)
            candidate[pos] = guess
            probes.append(bytes(candidate) + block)
        hits = [guess for guess, valid in enumerate(client.oracle_batch(probes)) if valid]
        if pos == BS - 1 and len(hits) > 1:
            # Perturbing the preceding byte preserves a 01 pad but destroys longer pads.
            checks = []
            for guess in hits:
                candidate = bytearray(crafted)
                candidate[pos] = guess
                candidate[pos - 1] ^= 1
                checks.append(bytes(candidate) + block)
            hits = [guess for guess, valid in zip(hits, client.oracle_batch(checks)) if valid]
        if len(hits) != 1:
            raise RuntimeError(f"oracle failed at byte {pos}")
        result[pos] = hits[0] ^ padding
        print(f"\rdecrypting block byte {BS-pos:2d}/{BS}", end="", flush=True)
    print()
    return bytes(result)


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def main():
    c = Client(HOST, PORT)
    token_ct = c.login_password()
    data_ct = c.encrypted_data()

    # The first known JWT plaintext block reveals the fixed IV.
    known_first = b'eyJhbGciOiJIUzI1'
    iv = xor(intermediate(c, token_ct[:BS]), known_first)
    print("IV:", iv.hex())

    blocks = [data_ct[i:i + BS] for i in range(0, len(data_ct), BS)]
    previous = iv
    plaintext = b""
    for n, block in enumerate(blocks, 1):
        plaintext += xor(intermediate(c, block), previous)
        previous = block
        print(f"plaintext so far: {plaintext!r}")

    pad = plaintext[-1]
    if not 1 <= pad <= BS or plaintext[-pad:] != bytes([pad]) * pad:
        raise RuntimeError("bad recovered padding")
    payload = plaintext[:-pad].decode()
    print("recovered payload:", payload)

    # Card numbers are conventionally 16 digits; the remainder is the float balance.
    card, balance_text = payload[:16], payload[16:]
    balance = float(balance_text)
    if not card.isdigit() or balance < 0 or not balance.is_integer():
        raise RuntimeError(f"unexpected card/balance encoding: {payload!r}")
    response = c.withdraw(card, int(balance))
    print(response)


if __name__ == "__main__":
    main()
