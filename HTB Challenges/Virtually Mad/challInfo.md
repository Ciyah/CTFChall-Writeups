---
ctf: HTBLabs
title: Virtually Mad
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Virtually Mad

## Challenge
Your friend loves to make pretty odd programs. This time you are given a special machine and you have to crack the correct code.

## Approach

The input is split into five 8-character hexadecimal VM instructions. The
dispatcher has an off-by-one-style layout: opcodes 1 through 4 map to MOV,
ADD, SUB, and CMP. Each arithmetic instruction uses a marker nibble of 1,
followed by a destination-register nibble, an addressing-mode nibble, and a
12-bit operand.

The five position-specific validation rules allow this program:

```text
02100100  ADD a, 0x100
02100100  ADD a, 0x100
03110001  SUB b, 1
01121100  MOV c, b
04130000  CMP d, 0
```

It leaves `a = 0x200`, `b = c = 0xffffffff`, `d = 0`, and the equality flag
set to `0x10000000`, satisfying every final check.

## Tools

- `objdump`
- `strings`
- Python 3

## Lessons

- Check the exact address used for a function-pointer lookup; the allocated
  dispatch table's first logical entry was not index zero.
- Position-specific instruction constraints can reduce a VM challenge to a
  short register-state construction problem.

## Flag

`HTB{redacted}`
