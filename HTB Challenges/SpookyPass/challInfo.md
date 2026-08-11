---
ctf: HTBLabs
title: SpookyPass
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# SpookyPass

## Challenge
All the coolest ghosts in town are going to a Haunted Houseparty - can you prove you deserve to get in?

## Approach
Inspected the binary with `file` and extracted its printable strings. The
expected password was stored unobfuscated in the binary:

`s3cr3t_p455_f0r_gh05t5_4nd_gh0ul5`

Supplying this password to the program passed the `strcmp` check and caused
the program to assemble and print the flag from its global `parts` array.

## Tools

- `file`
- `strings`
- `objdump`

## Lessons

Always begin a reverse-engineering challenge with basic static analysis.
Checking printable strings can immediately expose hard-coded credentials and
other useful clues before more involved debugging or decompilation is needed.

## Flag

`HTB{redacted}`
