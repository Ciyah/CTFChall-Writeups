---
ctf: HTBLabs
title: infosekurus query
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# infosekurus query

## Challenge
I warned my boss, Mr. Dam, that guarding his sensitive data with a custom authentication system wasn't secure at all. He laughed and bet me that if I could somehow bypass it, he would give everyone in the office a promotion. Upon hearing this, the entire office UNIted is rooting for me... IP: 154.57.164.71:32734

## Approach

1. Request RSA key index 6. Its exponent is `8192 = 2^13`, so it is not
   coprime with the even totient and the server leaks `phi(N)`.
2. Factor `N` from `N - phi(N) + 1 = p + q`. Take 13 successive modular
   square roots modulo `p` and `q`, combine them with CRT, and filter the
   resulting candidates for printable bytes. This recovers `s3cr3t`.
3. Query the custom hash using `s3cr3t` plus four null bytes. The precedence
   bug in `rxor` reduces its random mask to one bit, which the chosen input
   clears, revealing a genuine intermediate keyed-hash state.
4. Use Merkle-Damgard length extension: submit an answer containing the
   remaining oracle bytes and the oracle message's glue padding.
5. Continue the AES-based compression function locally and brute-force the
   five randomized characters from its 12-character alphabet. Submit the
   matching five-byte value to bypass 2FA.

## Tools

- Python 3
- SymPy (`sqrt_mod`, CRT)
- `cryptography` AES implementation

## Lessons

- Never expose RSA totients, including for invalid/non-coprime exponents.
- Prefix-MAC constructions based on Merkle-Damgard hashes permit length
  extension; use HMAC or a standard authenticated construction.
- Parentheses and operator precedence errors in cryptographic code can reduce
  randomness to a predictable value.

## Flag
HTB{56674ba45f935b8d36cb8269f1de5dcd}
