---
ctf: HTBLabs
title: Forks and Knives
category: pwn
difficulty: unknown
tags: [format-string, stack-overflow, fork-oracle, ret2libc, rop]
flag_format: HTB{...}
date: 2026-08-12
---

# Forks and Knives

## Challenge
Here at the Forks & Knives restaurant we recently hired a new IT guy to add some features to our ordering and reservation system. Apparently, he isn't very good. We want to hire you to test our system. Can you find any problems? IP:154.57.164.82:32327

## Approach

The server forks after `accept()`, so every child inherits the same stack
canary, stack layout, PIE base, and libc base. The order handler reads 0x100
bytes into a 0x110-byte buffer, then (when adding another item) reads another
0x100 bytes at `buffer + first_read_size`. This overflows the canary, saved
RBP, and return address.

1. Use the post-overflow menu as a crash oracle to recover the 8-byte canary
   and the child handler's saved RBP byte by byte.
2. Reservations are passed to `fprintf()` as the format string. Add `%N$p`
   reservations, then partially overwrite the order handler's return address
   with PIE offset `0x1426`, entering the reservation viewer after its inverted
   manager check. This leaks stack, PIE, and libc pointers.
3. Clear the shared file through the equivalent check bypass at `0x1847`, add
   `%2$s`, and bypass the viewer again. The leaked bytes `48 3d 00` identify
   the disclosed libc address as offset `0x11491b`, yielding libc base
   `0x7f0b2f4bc000` for this instance.
4. ROP through the supplied libc: call `dup2(4, 0..2)`, then
   `system("/bin/sh")`, and read the flag over the client socket. The command
   `cat flag*` returned two values: a thematic decoy followed by the real,
   instance-specific hash flag. The first value was accepted by HTB.

## Tools

- `objdump`, `readelf`, radare2
- Python sockets and a concurrent fork oracle

## Lessons

- Fork-per-connection services turn stack cookies and ASLR values into stable
  brute-force targets when a reliable response/crash distinction exists.
- A short format string can still disclose useful register arguments; `%2$s`
  helped fingerprint the exact libc offset.
- Partial return-address overwrites bypass PIE when the destination is in the
  same image and only the low address bytes need changing.
- Do not assume the most thematic-looking `HTB{...}` value is genuine. Avoid
  broad globs when extracting flags; enumerate filenames and validate outputs.

## Flag

`HTB{redacted}`

Decoy encountered: `HTB{redacted}`
