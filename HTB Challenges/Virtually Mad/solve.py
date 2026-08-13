#!/usr/bin/env python3
"""Construct and optionally verify the Virtually Mad VM program."""

from pathlib import Path
import subprocess


def instruction(opcode: int, destination: int, operand: int, *, register=False) -> int:
    """Encode: opcode | required marker | destination | mode | 12-bit operand."""
    mode = 1 if register else 0
    return (
        (opcode << 24)
        | (1 << 20)
        | (destination << 16)
        | (mode << 12)
        | (operand & 0xFFF)
    )


program = [
    instruction(2, 0, 0x100),             # ADD a, 0x100
    instruction(2, 0, 0x100),             # ADD a, 0x100
    instruction(3, 1, 1),                 # SUB b, 1
    instruction(1, 2, 1 << 8, register=True),  # MOV c, b
    instruction(4, 3, 0),                 # CMP d, 0 (sets equality flag)
]

code = "".join(f"{opcode:08x}" for opcode in program)
flag = f"HTB{{{code}}}"
print(flag)

binary = Path(__file__).parent / "Virtually Mad/rev-virtuallymad/virtually.mad"
if binary.exists():
    result = subprocess.run(
        [binary], input=code + "\n", text=True, capture_output=True, check=True
    )
    assert "This is the right answer!" in result.stdout
    print(result.stdout, end="")
