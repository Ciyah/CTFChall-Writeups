#!/usr/bin/env python3
"""Static solver for HTB's Debugme Windows reversing challenge."""

from pathlib import Path


IMAGE_BASE = 0x400000
TEXT_RVA = 0x1000
TEXT_RAW = 0x400


def va_to_raw(va: int) -> int:
    """Map an address in this binary's .text section to its file offset."""
    return TEXT_RAW + (va - IMAGE_BASE - TEXT_RVA)


binary = Path(__file__).with_name("Debugme").joinpath("debugme.exe").read_bytes()

# The hidden pre-entry stub (in the raw padding after .text) XOR-decrypts this
# inclusive address range before handing execution back to the CRT entry point.
start_va, end_va, key = 0x401620, 0x401791, 0x5C
stage1 = bytes(b ^ key for b in binary[va_to_raw(start_va):va_to_raw(end_va) + 1])

# After its anti-debug checks, the unpacked routine builds the encrypted flag
# using only these EAX operations and PUSHes. Emulate that small instruction
# subset directly, avoiding any need to execute the Windows binary.
pc = 0x4016B4 - start_va
stop = 0x401772 - start_va
eax = 0
pushes: list[bytes] = []

while pc < stop:
    opcode = stage1[pc]
    if stage1[pc:pc + 2] == b"\x31\xc0":       # xor eax, eax
        eax = 0
        pc += 2
    elif opcode == 0xB8:                         # mov eax, imm32
        eax = int.from_bytes(stage1[pc + 1:pc + 5], "little")
        pc += 5
    elif opcode == 0x2D:                         # sub eax, imm32
        eax = (eax - int.from_bytes(stage1[pc + 1:pc + 5], "little")) & 0xFFFFFFFF
        pc += 5
    elif opcode == 0x05:                         # add eax, imm32
        eax = (eax + int.from_bytes(stage1[pc + 1:pc + 5], "little")) & 0xFFFFFFFF
        pc += 5
    elif opcode == 0x25:                         # and eax, imm32
        eax &= int.from_bytes(stage1[pc + 1:pc + 5], "little")
        pc += 5
    elif opcode == 0x50:                         # push eax
        pushes.append(eax.to_bytes(4, "little"))
        pc += 1
    elif opcode == 0xE9:                         # decorative jmp to next instruction
        pc += 5
    else:
        raise RuntimeError(f"unexpected opcode {opcode:#x} at {start_va + pc:#x}")

# PUSH reverses dword order on the x86 stack. The tail of the unpacked routine
# contains `mov ecx, 0x24; mov ebx, 0x4b`: ciphertext length and XOR key.
ciphertext = b"".join(reversed(pushes))
count = int.from_bytes(stage1[0x40177C - start_va:0x401780 - start_va], "little")
xor_key = int.from_bytes(stage1[0x401781 - start_va:0x401785 - start_va], "little")
assert count == len(ciphertext) == 0x24 and xor_key == 0x4B

plaintext = bytes(byte ^ xor_key for byte in ciphertext)
print(f"HTB{{{plaintext.decode()}}}")
