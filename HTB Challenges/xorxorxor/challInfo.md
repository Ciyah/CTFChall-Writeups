---
ctf: HTBLabs
title: xorxorxor
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# xorxorxor

## Challenge
Who needs AES when you have XOR?

## Approach

The supplied encryption used a four-byte key repeatedly:

`ciphertext[i] = plaintext[i] XOR key[i % 4]`

Since an HTB flag starts with the known four-byte prefix `HTB{`, XORing that
prefix with the first four ciphertext bytes recovers the entire key. Applying
the recovered key repeatedly to the full ciphertext decrypts the flag.

## Tools

- Python 3 (`solve.py`)

## Lessons

- XOR is its own inverse: `C XOR P = K` and `C XOR K = P`.
- Repeating a short XOR key leaks it when one full key-length of plaintext is
  known.

## Flag

`HTB{rep34t3d_x0r_n0t_s0_s3cur3}`
