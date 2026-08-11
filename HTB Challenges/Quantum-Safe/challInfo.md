---
ctf: HTBLabs
title: Quantum-Safe
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Quantum-Safe

## Challenge
I heard Shor's algorithm can do all sorts of nasty things to RSA, so I've decided to be super modern and protect my flag with cool new maffs

## Approach

The public-key matrix has determinant 6297, so it is invertible over the
rationals. Each ciphertext therefore satisfies

`[character, noise1, noise2] = (ciphertext - r) * pubkey^-1`.

The same offset `r` is reused for every character and has only 11^3 possible
values. `solve.py` tries all of them using exact integer arithmetic. A candidate
is retained only when every recovered component is integral, both noise values
are in `[0, 100]`, and every character is printable. The unique valid offset is
`(7, 3, 0)`.

## Tools

- Python 3

## Lessons

Multiplication by a known invertible matrix provides no secrecy. The small,
reused additive offset can be exhaustively searched, while the plaintext and
noise bounds give a strong test for the correct candidate.

## Flag

`HTB{r3duc1nG_tH3_l4tTicE_l1kE_n0b0dY's_pr0bl3M}`
