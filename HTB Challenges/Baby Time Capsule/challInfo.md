---
ctf: HTBLabs
title: Baby Time Capsule
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Baby Time Capsule


## Challenge
Very Easy Crypto Challenge
154.57.164.75:30142
## Approach
The server encrypts the same plaintext under a fresh RSA modulus each time, but
always uses the small public exponent `e = 5` and no padding. Request five
capsules, combine the five ciphertexts with the Chinese Remainder Theorem, and
recover the unreduced integer `m^5`. Since the product of the five 1024-bit
moduli is larger than `m^5`, taking the exact integer fifth root reveals the
flag. This is Hastad's broadcast attack.

## Tools
`solve.py` (Python standard library only)

## Lessons
Never use textbook RSA. Randomized padding such as RSA-OAEP prevents the same
message from producing values vulnerable to this broadcast attack.

## Flag
`HTB{redacted}`
