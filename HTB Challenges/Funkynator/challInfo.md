---
ctf: HTBLabs
title: Funkynator
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Funkynator

## Challenge
After 3 weeks of doing menial work as an intern, they finally allowed me to create front-facing programs! Could you rate my work? IP:154.57.164.66:31344

## Approach

The message editor accepts an unchecked unsigned offset for a one-byte write,
giving an arbitrary relative heap write. The exploit uses it to:

1. Extend a saved chunk into a freed unsorted-bin chunk and leak libc.
2. Extend another chunk into a freed tcache chunk and leak the safe-linking key.
3. Poison a two-entry tcache list so an allocation lands at `environ - 0x48`.
4. Print through `environ` to leak the stack address.
5. Write a `ret; pop rdi; "/bin/sh"; system` chain over the message editor's
   saved return address.

## Tools

- `rabin2`, `objdump`, `readelf`
- pwntools
- `solve.py`

## Lessons

- With safe-linking, a singly freed tcache chunk whose decoded `fd` is null
  exposes the heap-page key directly.
- A poisoned tcache list needs another entry behind its head; otherwise the bin
  becomes empty after the first allocation and the poisoned target is ignored.
- `environ` remains a useful bridge from a libc leak to a stack leak.

## Flag

`HTB{redacted}`
