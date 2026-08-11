---
ctf: HTBLabs
title: Embryonic Plant
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Embryonic Plant

## Challenge
In a post-apocalyptic world, you are an aspiring botanist who has dedicated his life to the study of plants and their genetic manipulation, and is an expert on their embryonic stage. On your journey around the world, hoping to find a way to artificially create plants that can withstand Earth's cruel environment, you have come across a new species in a seemingly inhospitable area. You know it's time for you to unlock the secrets of nature. Will 5 plants be enough? IP: 154.57.164.67:32055

## Approach
For the affine recurrence `s[i+1] = p*s[i] + q (mod r)`, consecutive
differences satisfy `D[i+1] = p*D[i] (mod r)`. Therefore `r` divides both
`D1^2 - D0*D2` and `D2^2 - D1*D3`, so their gcd reveals `r`.

Recover `p = D1/D0 (mod r)` and `q = s1 - p*s0 (mod r)`. Since the challenge
chooses `p,q < r`, these residues are the actual primes, and `p*q*r == n`.
Compute the RSA private exponent from the recovered factorization, hash it for
the AES key, and decrypt the ECB ciphertext.

## Tools
`solve.py` (Python, cryptography, sympy)

## Lessons
Several outputs of an affine LCG allow elimination of its unknown multiplier
and increment; a gcd of the resulting integer relations can recover the hidden
modulus.

## Flag
`HTB{0c8fe20bab8b35c1c7067c314a2442e4}`
