---
ctf: HTBLabs
title: Neon Core
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Neon Core

## Challenge
Deep within the Neon Lab research facility, a classified blueprint has been encrypted using a mysterious cipher. Rumors whisper that the encryption scheme has a critical flaw, one that could allow someone skilled enough to unravel its secrets. IP:154.57.164.77:31007

## Approach
Treat the flattened matrix after the S-box as a 16-element vector over GF(257).
The remaining operation, `K * X * L + T`, is an unknown affine map `A*x+t`.
A baseline chosen plaintext and 16 single-position changes recover all columns of
`A`; invert it for each flag block, then apply the published cube-root exponent
171 to every coordinate.

## Tools
`solve.py` (pure Python; no Sage dependency)

## Lessons
Non-linearity before an otherwise secret linear layer does not protect a cipher
from chosen plaintexts when the non-linearity is public and independently
invertible per coordinate.

## Flag
HTB{redacted}
