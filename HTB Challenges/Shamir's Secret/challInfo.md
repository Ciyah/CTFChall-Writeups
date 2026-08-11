---
ctf: HTBLabs
title: Shamir's Secret
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Shamir's Secret

## Challenge
We tracked down the Shamir gang's network activity to one server. We're sure there's some valuable data on there, but it's protected with a custom encryption scheme. Fortunately we managed to extract the scheme's source code. Can you figure out how to break it? IP: 154.57.164.73:32374

## Approach

The server reuses the same 64-bit key mask for every encryption. Exactly 32
positions contain evaluations of the degree-31 polynomial; the other 32 are
random pairs.

Query encryptions of the known integer message `0`. For every genuine pair,
an even `x` implies an even `y`, since every non-constant polynomial term is
then even and the constant is zero. A fake pair violates this condition with
probability 1/4 per query. Repeated queries therefore eliminate all fake
positions while never eliminating a genuine one.

After requesting the encrypted flag once, retain its pairs at the recovered 32
positions. Recover the constant coefficient with Lagrange interpolation at
zero over `Z/(2^1024)`. Because this is not a field, factor powers of two from
each numerator and denominator, invert only odd denominator components, and
multiply every coefficient by a common power of two. The run lost only four
modulus bits and recovered 1020 bits, far more than needed for the flag.

## Tools

- Python 3 socket client
- 2-adic Lagrange interpolation
- `solve.py`

## Lessons

- Reusing a secret selector mask across chosen-plaintext encryptions leaks it
  through simple modular invariants.
- Polynomial interpolation modulo a prime power needs special handling because
  even denominators are not invertible.

## Flag

`HTB{c706f0db2e6e2c1489ea861257743f84}`
