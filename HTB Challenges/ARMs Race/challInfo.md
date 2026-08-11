---
ctf: HTBLabs
title: ARMs Race
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# ARMs Race

## Challenge
The famous hacker Script K. Iddie has finally been caught after many years of cybercrime. Before he was caught, he released a server sending mysterious data, and promised his 0-days to anyone who could solve his multi-level hacking challenge. Now everyone is in an ARMs race to get his exploits. Can you be the one to solve Iddie's puzzle? IP:154.57.164.83:31917

## Approach
The service sends 50 hex-encoded, little-endian ARM programs and asks for the
final value of register `r0` after each one executes. Decode each blob with
Capstone, emulate its small instruction subset with 32-bit wrapping arithmetic,
and submit `r0` as an unsigned decimal integer. The generated programs use
`mov`/`movw`/`movt`, arithmetic (`add`, `adc`, `sub`, `sbc`, `rsb`, `mul`) and
bitwise operations (`and`, `orr`, `eor`, `bic`). The fresh context has its carry
flag clear, which matters for `adc` and `sbc`.

The automated solution is in `solve.py`.

## Tools
Python, Capstone

## Lessons
ARM instructions are fixed-width and the byte stream is little-endian. Preserve
the low half of a register for `movt`, and mask every arithmetic result to 32
bits.

## Flag
Confirmed by completing all 50 levels:

```text
HTB{redacted}
```
