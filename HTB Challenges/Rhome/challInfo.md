---
ctf: HTBLabs
title: Rhome
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Rhome

## Challenge
I received this lovely letter but the sender put a seal on it. She said that can be opened only at our place, Rhome. IP: 154.57.164.82:32762

## Approach

The modulus is generated as `p = 2*q*r + 1`, where `q` is only 42 bits and
`r` is a 512-bit prime. Since `g = h^(2*r) mod p`, Fermat's theorem gives
`g^q = 1 mod p`, so every public key and the shared secret lie in the small
order-`q` subgroup.

1. Request `p`, `g`, `A`, and `B` from the service.
2. Factor `p - 1` and identify its 42-bit prime factor `q`.
3. Use baby-step/giant-step to solve `A = g^a mod p` for `a mod q`.
4. Compute the shared secret as `B^a mod p`.
5. Derive `SHA256(long_to_bytes(ss))[:16]` and decrypt the flag with AES-ECB.

The complete exploit is in `solve.py`.

## Tools

- Python 3
- SymPy (`factorint`)
- `cryptography` (AES-ECB and PKCS#7 unpadding)

## Lessons

Large DH moduli do not provide security when the generator is confined to a
small subgroup. Validate the generator's order and use a sufficiently large
prime-order subgroup.

## Flag

`HTB{redacted}`
