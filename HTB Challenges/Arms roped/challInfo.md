---
ctf: HTBLabs
title: Arms roped
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-13
---

# Arms roped

## Challenge
Get a shell! IP:154.57.164.72:31272

## Approach

`scanf("%m[^\n]%n", &tmp, &n)` allocates an attacker-sized string, but the
program then copies all `n` bytes into a 28-byte stack buffer. The following
`puts` supplies an unterminated stack disclosure before the canary is checked.

Successive inputs disclose:

- 33 bytes: the remaining three bytes of the stack canary
- 41 bytes: the PIE/GOT register and the caller frame pointer
- 72 bytes: the saved Thumb return address at `libc + 0x17525`

The final overflow starts with `quit` so execution leaves the input loop. It
restores the canary and returns to the `__libc_csu_init` pop/call gadgets. The
call gadget loads the disclosed `system` address from the known stack frame and
invokes `system("/bin/sh")`.

## Tools

- radare2 / readelf
- QEMU ARM user-mode emulation
- Python sockets

## Lessons

- An overflow inside a loop does not reach the corrupted return address until
  the loop's exit condition is satisfied.
- `%m` removes the destination-size bound; copying its result into a fixed
  local array reintroduces an unbounded stack copy.
- Unterminated `puts` echoes can disclose a canary and multiple ASLR bases a
  few bytes at a time.

## Flag
HTB{redacted}
