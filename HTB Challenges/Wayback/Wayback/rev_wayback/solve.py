#!/usr/bin/env python3
"""Brute-force Wayback's timestamp-seeded password generator."""

import ctypes
from datetime import datetime, timedelta

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


ENCRYPTED = bytes.fromhex(
    "ad24426047b0ffb03b67977366483846"
    "2a6f00bdcaf0589dd1748e9ed5c56860"
    "1edc87d974894f9dd9b98cc35535145c"
    "494eb0af84c8f78d440a033c91c7de62"
    "d506d8cabdc2a10138b95139bbe60e89"
)
ALPHABET = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_+0123456789"

libc = ctypes.CDLL("libc.so.6")
libc.srand.argtypes = [ctypes.c_uint]
libc.rand.restype = ctypes.c_int


def password_for(timestamp: datetime) -> bytes:
    # V1 constructs the decimal timestamp arithmetically, then srand() keeps
    # only its low 32 bits.
    seed = int(timestamp.strftime("%Y%m%d%H%M%S")) & 0xFFFFFFFF
    libc.srand(seed)
    return bytes(ALPHABET[libc.rand() % len(ALPHABET)] for _ in range(20))


def decrypt(key: bytes) -> bytes | None:
    padded_key = key.ljust(32, b"\0")
    decryptor = Cipher(
        algorithms.AES(padded_key), modes.CBC(ENCRYPTED[:16])
    ).decryptor()
    plaintext_padded = decryptor.update(ENCRYPTED[16:]) + decryptor.finalize()
    try:
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(plaintext_padded) + unpadder.finalize()
    except ValueError:
        return None


def main() -> None:
    current = datetime(2013, 12, 10)
    end = datetime(2013, 12, 12)
    while current < end:
        password = password_for(current)
        plaintext = decrypt(password)
        if plaintext is not None and b"HTB{" in plaintext:
            print(f"timestamp: {current:%Y-%m-%d %H:%M:%S}")
            print(f"password:  {password.decode()}")
            print(f"plaintext: {plaintext.decode()}")
            return
        current += timedelta(seconds=1)
    raise SystemExit("No valid password found")


if __name__ == "__main__":
    main()
