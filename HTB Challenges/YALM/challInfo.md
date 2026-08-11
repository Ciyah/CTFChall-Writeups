---
ctf: HTBLabs
title: YALM
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# YALM

## Challenge
I created an encryption server with RSA, but I forgot to show the modulus. Can you help me recover it yet another time? IP: 154.57.164.82:32481

## Approach

`test_encryption()` divides the supplied integer by `N` and rejects it when a
second chunk exists. Its response is therefore a comparison oracle: "Thanks"
means `m < N`, while "Too many" means `m >= N`. Query ordered comparison
points in batches to bracket and recover the exact 2048-bit modulus efficiently.

The secret uses exponent `e = 3` and a fixed known sentence. After appending
the known `HTB{` prefix, model the remaining flag suffix as a small integer `x`:

`f(x) = (known_prefix * 256^len(x) + x)^3 - c (mod N)`

Try plausible suffix lengths and apply univariate Coppersmith/LLL. Verify each
root by re-encrypting the reconstructed plaintext modulo `N`.

## Tools

- Python socket client with pipelined comparison queries
- `fpylll` and SymPy for lattice reduction and polynomial handling

## Lessons

- Suppressing RSA ciphertext output does not prevent leakage when control flow
  reveals whether attacker-controlled input crossed the modulus.
- Pipelining ordered thresholds turns a high-latency one-bit comparison oracle
  into a practical multi-bit interval search.
- Textbook low-exponent RSA is vulnerable when most of the plaintext is known.

## Flag
HTB{48ff4d3a065e5a7d400a49cb5a4d2947}
