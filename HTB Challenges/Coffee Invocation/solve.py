#!/usr/bin/env python3
from pathlib import Path


binary = Path("Coffee Invocation/rev_coffee_invocation/coffee_invocation").read_bytes()

# Verify1 compares values after the native launcher corrupts the Byte and
# Short caches.  The installed mappings reduce to source = -target - 0x51.
target1 = binary[0x6480:0x6480 + 26]
part1 = bytes((-value - 0x51) & 0xFF for value in target1)

# Verify2 processes the second half in pairs. Boolean.TRUE/FALSE are swapped,
# so the source pair is left alone while the entire target string is sorted.
# Each exit installs the next corrupted Character-cache permutation.
target2 = b"Cr1KD5mk0_uUzQYifaGVqlN2B3wvpgPtSx6Odo{8hjJLHy9IXb4RnWZ}TAFEsMce7"
part2 = bytearray()
for index in range(13):
    table_offset = 0x6700 + index * 0x120
    mapping = binary[table_offset:table_offset + 127]
    inverse = {mapped: original for original, mapped in enumerate(mapping)}
    sorted_target = sorted(mapping[value] for value in target2)
    pair = sorted_target[index * 2:index * 2 + 2]
    part2.extend(inverse[value] for value in pair)

password = part1 + part2
assert len(password) == 52
print(f"HTB{{{password.decode()}}}")
