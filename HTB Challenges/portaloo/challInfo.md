---
ctf: HTBLabs
title: portaloo
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# portaloo

## Challenge
Portals... A gateway to other dimensions, where chaos meets creativity and the void greets you. IP:154.57.164.67:30733

## Approach

1. Allocate portal 0, free it, overwrite 16 bytes of freed tcache metadata, and
   free it again. Clearing the tcache key bypasses the double-free check.
2. Peek at the freed portal. Its safe-linked self-reference is
   `chunk ^ (chunk >> 12)`; invert this to recover the exact heap chunk address.
3. The program made the heap page RWX with `mprotect`, so write a 12-byte
   `execve(rsp, NULL, NULL)` shellcode into the freed chunk.
4. In `step_into_the_portal`, send 73 bytes to the 72-byte first buffer. This
   overwrites the canary's leading NUL, allowing `printf("%s")` to disclose the
   remaining 7 canary bytes and 6 useful bytes of saved RBP.
5. Use the second overflow: 72-byte padding, restored canary, saved RBP, the
   executable heap address, then `/bin/sh\0`. On return, the heap shellcode uses
   RSP as the filename pointer and spawns a shell.

The complete remote exploit is in `solve.py`.

## Tools

- Python 3 socket client
- glibc tcache safe-linking/double-free
- amd64 shellcode

## Lessons

- A dangling pointer enables both tcache metadata corruption and a heap leak.
- Safe-linked pointers of the form `x ^ (x >> 12)` can be inverted iteratively.
- A one-byte overwrite of a canary's leading NUL can turn a `%s` print into a
  canary leak.

## Flag

`HTB{redacted}`
