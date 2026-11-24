#!/usr/bin/env python3
"""
Echoes of Silent Past — Curtin CTF 2026
ESP32 flash dump vault extractor.

Usage:
    python3 solve.py [path/to/vault_dump.bin]

Defaults to Archive45/vault_dump.bin relative to the script directory.
"""
import base64
import struct
import sys
from pathlib import Path

DESCRIPTOR_START = 0x18C9C   # first of five 8-byte descriptors
DESCRIPTOR_END   = 0x18CC4   # one past the last descriptor
KEY_OFFSET       = 0x18CC4   # 4-byte repeating XOR key
VA_TO_FILE_DELTA = 0x3F3F0000  # subtract from virtual address to get file offset
ASSEMBLED_LEN    = 37          # total reconstructed buffer length

dump_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "Archive45" / "vault_dump.bin"
dump = dump_path.read_bytes()

key = dump[KEY_OFFSET:KEY_OFFSET + 4]
print(f"[*] XOR key: {key.hex()}")

assembled = bytearray(ASSEMBLED_LEN)

for base in range(DESCRIPTOR_START, DESCRIPTOR_END, 8):
    # Each descriptor: virtual_address (4 bytes LE), length (1 byte),
    #                  destination_offset (1 byte), mode (1 byte), pad (1 byte)
    address, length, destination, mode, _pad = struct.unpack_from("<IBBBB", dump, base)
    file_offset = address - VA_TO_FILE_DELTA
    fragment = bytearray(dump[file_offset:file_offset + length])

    print(f"[*] Descriptor @ 0x{base:05X}: va=0x{address:08X} off=0x{file_offset:05X} "
          f"len={length} dst={destination} mode={mode}")

    if mode == 4:
        fragment = bytearray(reversed(fragment))

    decoded = bytearray(length)
    for i, byte in enumerate(fragment):
        if mode == 0:
            decoded[i] = byte ^ key[i % len(key)]
        elif mode == 1:
            decoded[i] = (byte - 17 * (i + 1)) & 0xFF
        elif mode == 2:
            decoded[i] = byte ^ ((7 * i + 3) & 0xFF)
        elif mode == 3:
            rotated = ((byte >> 3) | (byte << 5)) & 0xFF
            decoded[i] = rotated ^ 0x6B
        elif mode == 4:
            decoded[i] = byte ^ 0x42
        else:
            raise ValueError(f"Unexpected decoding mode {mode}")

    assembled[destination:destination + length] = decoded

print(f"[*] Assembled buffer ({len(assembled)} bytes): {bytes(assembled)}")

padded = bytes(assembled) + b"=" * (-len(assembled) % 8)
body = base64.b32decode(padded).decode("ascii")
flag = f"CURTIN_CTF{{{body}}}"
print(f"\n[+] Flag: {flag}")
