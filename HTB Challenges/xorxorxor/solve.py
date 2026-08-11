#!/usr/bin/env python3

"""Recover a four-byte repeated-XOR key from the known HTB flag prefix."""

CIPHERTEXT = bytes.fromhex(
    "134af6e1297bc4a96f6a87fe046684e8047084ee046d84c5282dd7ef292dc9"
)
KNOWN_PREFIX = b"HTB{"


def xor_repeating(data: bytes, key: bytes) -> bytes:
    return bytes(byte ^ key[i % len(key)] for i, byte in enumerate(data))


def main() -> None:
    key = bytes(cipher ^ plain for cipher, plain in zip(CIPHERTEXT, KNOWN_PREFIX))
    plaintext = xor_repeating(CIPHERTEXT, key)

    print(f"key:  {key.hex()}")
    print(f"flag: {plaintext.decode()}")


if __name__ == "__main__":
    main()
