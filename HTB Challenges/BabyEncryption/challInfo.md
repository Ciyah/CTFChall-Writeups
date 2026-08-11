---
ctf: HTBLabs
title: BabyEncryption
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# BabyEncryption

## Challenge
You are after an organised crime group which is responsible for the illegal weapon market in your country. As a secret agent, you have infiltrated the group enough to be included in meetings with clients. During the last negotiation, you found one of the confidential messages for the customer. It contains crucial information about the delivery. Do you think you can decrypt it?

## Approach

The encryption applies the affine transformation
`c = (123m + 18) mod 256` independently to each byte. Since
`gcd(123, 256) = 1`, 123 has a modular inverse, so each byte is recovered with
`m = 123^-1(c - 18) mod 256`. The implementation is in `solve.py`.

## Tools

- Python 3

## Lessons

Affine transformations modulo 256 are reversible whenever the multiplier is
coprime to 256.

## Flag

`HTB{l00k_47_y0u_r3v3rs1ng_3qu4710n5_c0ngr475}`
