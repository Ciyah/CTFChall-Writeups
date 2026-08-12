---
ctf: HTBLabs
title: HILLarious
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# HILLarious

## Challenge
During a typical workday, one of Blackink-corp's servers was attacked. The cause? An executable that encrypted all the files of their new secret project. Amidst stress and confusion, the security team managed to recover the software used and the files retrieved from the compromised server. Your mission: assist the team in regaining control and recovering the project data.

## Approach

1. Unpacked the recovered executable with UPX and disassembled it.
2. Identified the 20-byte `SNAR` header: magic, 64-bit timestamp, original
   size, and version.
3. Reimplemented its key derivation: FNV-1a over the little-endian timestamp,
   XOR with `0xdeadbeefcafebabe`, followed by the program's LCG.
4. Reversed the 2x2 matrix multiplication modulo 256 and then removed the
   repeating 8-byte XOR layer.
5. Decrypted all three `.enc` files with `solve.py`.

## Tools

- UPX
- objdump / readelf
- Python 3

## Lessons

An odd determinant makes a 2x2 matrix invertible modulo 256, but embedding all
key material in a predictable timestamp-derived scheme makes the cipher fully
reversible from the file header.

## Flag

`HTB{redacted}`
