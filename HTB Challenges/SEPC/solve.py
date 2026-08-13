#!/usr/bin/env python3
import struct
import gzip
from pathlib import Path


INITRAMFS = Path(__file__).parent / "SEPC" / "rev_sepc" / "initramfs.cpio.gz"


def cpio_member(archive: bytes, wanted: str) -> bytes:
    """Return a member from a newc-format cpio archive."""
    offset = 0
    while archive[offset : offset + 6] in (b"070701", b"070702"):
        header = archive[offset : offset + 110]
        size = int(header[54:62], 16)
        name_size = int(header[94:102], 16)
        offset += 110
        name = archive[offset : offset + name_size - 1].decode()
        offset = (offset + name_size + 3) & ~3
        data = archive[offset : offset + size]
        if name == wanted:
            return data
        if name == "TRAILER!!!":
            break
        offset = (offset + size + 3) & ~3
    raise ValueError(f"cpio member {wanted!r} not found")


def section(blob: bytes, wanted: bytes) -> bytes:
    """Return a section from a little-endian ELF64 file."""
    shoff = struct.unpack_from("<Q", blob, 0x28)[0]
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", blob, 0x3A)
    headers = [
        struct.unpack_from("<IIQQQQIIQQ", blob, shoff + i * shentsize)
        for i in range(shnum)
    ]
    strings_header = headers[shstrndx]
    strings = blob[strings_header[4] : strings_header[4] + strings_header[5]]

    for header in headers:
        name_offset = header[0]
        name = strings[name_offset : strings.find(b"\0", name_offset)]
        if name == wanted:
            return blob[header[4] : header[4] + header[5]]
    raise ValueError(f"section {wanted!r} not found")


blob = cpio_member(gzip.decompress(INITRAMFS.read_bytes()), "checker.ko")
rodata = section(blob, b".rodata")

# checker.ko's read handler checks input[i] against these tables' XOR.
# It returns success after indices 0..33, so the closing brace is not checked.
password = bytes(a ^ b for a, b in zip(rodata[0x20:0x42], rodata[0x60:0x82]))
print(f"Password accepted by driver: {password.decode()}")
print(f"Flag: {password.decode()}}}")
