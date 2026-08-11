---
ctf: HTBLabs
title: Twisted Entanglement
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Twisted Entanglement

## Challenge
In our company, we use Elliptic Curve Cryptography to encrypt our internal communications. Fearing the consequences that the rise of quantum computing will bring, we decided to implement a new key exchange scheme. While researching Quantum Cryptography, we came across a strange concept called entanglement and decided to incorporate it into our server. IP: 154.57.164.67:30759

## Approach

The ECC endpoint never validates that an attacker-supplied point belongs to
secp256k1.  Its addition formulas do not use `b`, so points from other curves
`y^2 = x^3 + b'` can be submitted.  These j=0 curves have small-order
subgroups.  Querying five such points reveals the private scalar modulo
`3319`, `22639`, `20412485227`, `199`, and `18979`; baby-step/giant-step and
CRT recover the bounded private key as `3262827136301000405966`.

Seeding Python's PRNG with that value reveals the server's measurement basis
for every qubit.  Supplying those same 256 bases makes the two measurements of
the prepared Bell state deterministically opposite.  Complementing the
returned user bits, hashing them, and decrypting the AES-ECB ciphertext yields
the flag.  The complete exploit is in `solve.py`.

## Tools

- Python 3
- `cryptography` (AES)

## Lessons

- Always validate that externally supplied ECC points are on the intended
  curve and in the correct subgroup.
- A deterministic PRNG must not select secret quantum measurement bases.

## Flag
HTB{redacted}
