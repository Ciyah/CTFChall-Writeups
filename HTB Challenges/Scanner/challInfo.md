---
ctf: HTBLabs
title: Scanner
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Scanner

## Challenge
In the spirit of optimisation, I wanted a fast memory searching algorithm, and thanks to this program I think I've finally found one. Not only is it fast, it's also completely secure. IP:154.57.164.82:32084

## Approach

1. Fill the 4096-byte main buffer with a unique boundary marker and use
   `scanner_naive1`'s fixed 4096-position loop as an out-of-bounds equality
   oracle. This leaks the current heap allocation and saved libc/PIE pointers.
2. Trigger the `%16s` off-by-one in `read_parameters`: a 16-byte scanner name
   makes `scanf` append its NUL terminator over the low byte of the saved RBP.
   An embedded NUL after `naive1` preserves the scanner-name comparison.
3. Before corrupting RBP, fill the main buffer with repeated fake local-variable
   records. Whichever 16-byte-aligned RBP value results, main reads a valid heap
   pointer, size, and scanner index and survives the poisoned return.
4. Choose **Update buffer** again. Its shifted destination now overlaps the
   active `fgets` saved return address. A return sled covers every possible
   low-byte shift and converges on `pop rdi; ret; "/bin/sh"; system` using the
   supplied libc.
5. Read `flag.txt` from the resulting shell.

## Tools

- `objdump`, `readelf`, `r2`
- Python socket/subprocess exploit

## Lessons

- A width equal to the destination size is unsafe for `%s`; room is also needed
  for the terminating NUL.
- A one-byte saved-frame-pointer corruption can become control-flow hijacking
  when a later caller-relative buffer overlaps an active callee frame.
- Repeated fake records and a return sled remove dependence on the unknown low
  byte of the randomized stack address.

## Flag
`HTB{redacted}`
