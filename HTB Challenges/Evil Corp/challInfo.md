---
ctf: HTBLabs
title: Evil Corp
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Evil Corp

## Challenge
We turned our assembly tester off because a big mistake from our new C developer. Do you think there are other mistakes he made? IP:154.57.164.67:31126

## Approach

1. Extract the hard-coded UTF-32 login strings from `.rodata`: `eliot` / `4007`.
2. Select **Contact Support**. Its `fgetws` reads up to 4096 wide characters
   into a 16000-byte stack buffer, putting the saved RIP at wide-character
   index 4002.
3. The same input is converted to 16-bit characters into a fixed mapping at
   `0x10000`. Input index 2048 therefore begins writing into the adjacent RWX
   mapping at `0x11000`.
4. Send UTF-8 characters whose low 16 bits form a NOP sled and `/bin/sh`
   shellcode, then overwrite the saved RIP with `0x11000`. An embedded NUL
   supplies the zero high dword of the return address.
5. Execute `cat flag*` in the resulting shell.

## Tools

- `objdump`, `readelf`, `xxd`, `gdb`
- Python socket exploit: `solve.py`

## Lessons

Wide-character APIs change both overflow offsets and payload encoding. Here,
the 4-byte `wchar_t` stack layout controls RIP while the program's custom
2-byte conversion builds arbitrary x86-64 instructions in an RWX page.

## Flag
HTB{redacted}
