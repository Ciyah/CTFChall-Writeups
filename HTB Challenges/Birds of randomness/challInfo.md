---
ctf: HTBLabs
title: Birds of randomness
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Birds of randomness

## Challenge
You think you found your soulmate, but you lost the train ticket that your love gave you to meet again. The only thing that you remember is the coordinates of the departing station and your love disappearing into the steam of the train. IP: 154.57.164.82:30828

## Approach

The disclosed point is `d*G`, where `d = x*y*z` and each factor is a prime
smaller than roughly 30,000.  Factor the (smooth) declared order of `G` and
use Pohlig-Hellman, with baby-step/giant-step for each prime-order subgroup, to
recover `d` from the departing coordinates.

Factor `d` into its three primes.  Their assignment to the PRNG's `x`, `y`, and
`z` states is ambiguous, but there are at most `3! = 6` permutations--exactly
the number of guesses supplied by the service.  For every valid permutation,
advance the three multiplicative generators until all states are prime, form
the next product, and submit its elliptic-curve point.

## Tools

- Python (`ecdsa`, `sympy`)
- `solve.py`

## Lessons

An elliptic-curve group with a smooth order is vulnerable to Pohlig-Hellman.
Restricting a secret scalar to a highly structured product also leaks enough
state to predict subsequent PRNG output.

## Flag

`HTB{redacted}`
