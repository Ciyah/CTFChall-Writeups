---
ctf: HTBLabs
title: RSAisEasy
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# RSAisEasy

## Challenge
I think this is safe... Right?

## Approach

The two RSA moduli share the prime `q`:

`n1 = p*q` and `n2 = q*z`.

The supplied leak is `L = n1*E + n2`. Since adding a multiple of
`n1` does not change a GCD with `n1`, `gcd(n1, L) = gcd(n1, n2) = q`.
After recovering `q`, compute `p = n1/q`, recover `n2 = L mod n1`, and
compute `z = n2/q`. Both private exponents can then be calculated and
the two flag fragments decrypted.

## Tools

- Python 3 standard library (`math.gcd`, modular inverse via `pow`)

## Lessons

RSA moduli must never reuse a prime. A linear expression containing a
second modulus can still expose that shared factor through a GCD.

## Flag

`HTB{1_m1ght_h4v3_m3ss3d_uP_jU$t_4_l1ttle_b1t?}`
