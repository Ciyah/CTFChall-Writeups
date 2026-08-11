---
ctf: HTBLabs
title: mysterybox
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# mysterybox

## Challenge
They released this new mystery box thing to modify messages or something, but i'm sure my signing server will be fine. IP: 154.57.164.77:32156

## Approach

The service uses raw (unpadded) RSA signatures, so signatures are
multiplicative. First recover the hidden modulus using related messages. If
`S(m) = m^d mod n`, then, for example:

`S(2)^2 - S(4) = 0 mod n`

Taking the GCD of several such differences (`S(2)^2-S(4)`,
`S(2)^3-S(8)`, and `S(3)^2-S(9)`) yields `n`.

Let the forbidden admin message be `T`. Request signatures for the allowed
messages `2` and `2T`, then exploit multiplicativity:

`S(T) = S(2T) * S(2)^-1 mod n`

Submitting `T` with that forged signature passes verification and returns the
flag.

## Tools

- Python 3 (`socket`, `math.gcd`, modular inverse via `pow`)
- `solve.py`

## Lessons

Textbook RSA signatures are malleable. A secure signature scheme must use a
standardized randomized encoding such as RSA-PSS, and a signing oracle should
not expose algebraically related raw RSA operations.

## Flag

`HTB{redacted}`
