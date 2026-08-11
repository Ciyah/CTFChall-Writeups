---
ctf: HTBLabs
title: POPO
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# POPO

## Challenge
An unknown and shady startup is selling its new product, called POPO - Paillier Operation Performance Optimizer. Our colleague Bongio claimed to have identified a confidentiality problem, but has now disappeared under mysterious circumstances. Before she disappeared, she published the suspicious code. It is time to get clarity and rescue her. IP: 154.57.164.82:32263

## Approach

`anonymize()` reuses the same random value `r` for every request. On the first
call, send `m = 0`; because zero takes the secret-message branch, the returned
ciphertext is

`c0 = gm * r^n mod n^2`.

That call also enables the broken optimizer. On the next call, send `m = 1`.
The optimized branch uses the integer `1` directly instead of `g^1`, giving

`c1 = r^n mod n^2`.

Cancel the reused randomizer:

`gm = c0 * inverse(c1, n^2) mod n^2`.

Although the constructor later replaces `g`, it calculates `gm` beforehand
with the initial value `g = n + 1`. Therefore

`gm = (n + 1)^FLAG = 1 + FLAG*n mod n^2`,

so the plaintext is simply `(gm - 1) // n`. Converting that integer to bytes
reveals the flag.

## Tools

- `nc`
- Python modular arithmetic (`pow(c1, -1, n*n)`)

## Lessons

- Never reuse Paillier encryption randomness.
- Stateful optimization paths must preserve the exact semantics of the
  unoptimized cryptographic operation.
- Do not compute dependent values such as `gm` before finalizing the generator.

## Flag

`HTB{redacted}`
