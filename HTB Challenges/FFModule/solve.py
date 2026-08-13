#!/usr/bin/env python3
"""Extract the FFModule shellcode and recover its embedded key/flag."""

from pathlib import Path


EXE = Path("FFModule/rev_ffmodule/ffmodule.exe")
DATA_FILE_OFFSET = 0x15800
PAYLOAD_SIZE = 0x5A4
XOR_KEY = 0x72
KEY_OFFSET = 0x263
KEY_SIZE = 0x20


def rol8(value: int, count: int) -> int:
    return ((value << count) | (value >> (8 - count))) & 0xFF


def main() -> None:
    image = EXE.read_bytes()
    encrypted = image[DATA_FILE_OFFSET : DATA_FILE_OFFSET + PAYLOAD_SIZE]
    assert len(encrypted) == PAYLOAD_SIZE
    payload = bytes(byte ^ XOR_KEY for byte in encrypted)
    Path("payload.bin").write_bytes(payload)
    print(f"wrote {len(payload)} decrypted bytes to payload.bin")

    encoded_key = payload[KEY_OFFSET : KEY_OFFSET + KEY_SIZE]
    # Shellcode at payload+0x29d: add bl, 0xed; rol bl, 3; xor bl, 0x42
    flag = bytes(rol8((byte + 0xED) & 0xFF, 3) ^ 0x42 for byte in encoded_key)
    print(flag.decode())


if __name__ == "__main__":
    main()
