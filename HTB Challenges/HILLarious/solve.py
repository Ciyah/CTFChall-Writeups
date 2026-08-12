#!/usr/bin/env python3
import pathlib
import struct
import sys

MASK = (1 << 64) - 1
FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3
SEED_XOR = 0xDEADBEEFCAFEBABE
LCG_A = 0x5851F42D4C957F2D
LCG_C0 = 0x6C576FAC43FD007C
LCG_C = 0x14057B7EF767814F


def derive(timestamp: int):
    h = FNV_OFFSET
    for byte in struct.pack("<Q", timestamp):
        h = ((h ^ byte) * FNV_PRIME) & MASK
    seed = h ^ SEED_XOR
    xor_key = struct.pack("<Q", seed)

    state = (seed * LCG_A + LCG_C0) & MASK
    a = (state & 0xff) | 1
    state = (state * LCG_A + LCG_C) & MASK
    b = state & 0xff
    state = (state * LCG_A + LCG_C) & MASK
    c = state & 0xff
    state = (state * LCG_A + LCG_C) & MASK
    d = (state & 0xff) | 1
    if (a * d - b * c) % 2 == 0:
        a = (a + 2) & 0xff
    return (a, b, c, d), xor_key


def decrypt(path: pathlib.Path) -> bytes:
    raw = path.read_bytes()
    if len(raw) < 20 or raw[:4] != b"SNAR":
        raise ValueError(f"{path}: invalid SNAR file")
    timestamp, original_size, version = struct.unpack_from("<QII", raw, 4)
    if version != 1:
        raise ValueError(f"{path}: unsupported version {version}")

    matrix, xor_key = derive(timestamp)
    a, b, c, d = matrix
    det_inv = pow((a * d - b * c) & 0xff, -1, 256)
    ciphertext = raw[20:]
    mixed = bytes(v ^ xor_key[i % 8] for i, v in enumerate(ciphertext))
    plaintext = bytearray()
    for i in range(0, len(mixed), 2):
        y0, y1 = mixed[i:i + 2]
        plaintext.append(det_inv * (d * y0 - b * y1) & 0xff)
        plaintext.append(det_inv * (a * y1 - c * y0) & 0xff)
    return bytes(plaintext[:original_size])


def main():
    paths = [pathlib.Path(arg) for arg in sys.argv[1:]]
    if not paths:
        paths = sorted(pathlib.Path("HILLarious").glob("*.enc"))
    for path in paths:
        plaintext = decrypt(path)
        output = path.with_suffix("")
        output.write_bytes(plaintext)
        print(f"{path} -> {output} ({len(plaintext)} bytes)")


if __name__ == "__main__":
    main()
