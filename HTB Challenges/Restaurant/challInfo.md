---
ctf: HTBLabs
title: Restaurant
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Restaurant

## Challenge
Welcome to our Restaurant. Here, you can eat and drink as much as you want! Just don't overdo it..IP: 154.57.164.82:31909

## Approach

The `fill()` function allocates a 32-byte stack buffer but calls
`read(0, buffer, 0x400)`. The saved return address is therefore reached after
40 bytes. The binary has NX, no PIE, and full RELRO, so the exploit uses a
two-stage return-to-libc chain:

1. Return through `pop rdi; ret`, pass `puts@got` to `puts@plt`, and return to
   `main()`.
2. Subtract the supplied libc's `puts` offset (`0x80aa0`) from the leak.
3. Overflow again and call `system("/bin/sh")`, using offsets `0x4f550` and
   `0x1b3e1a` from the supplied libc. An extra `ret` gadget aligns the stack.

The complete standard-library exploit is in `solve.py` and can be run with:

```sh
python3 solve.py
```

## Tools

- `readelf`, `objdump`, `nm`, `strings`
- Python 3 (`socket` and `struct`; no pwntools dependency)

## Lessons

- A fixed-address ROP chain remains possible with full RELRO when the binary
  is not PIE.
- Leaking an already-resolved GOT entry gives the libc base needed for a
  second-stage `system("/bin/sh")` chain.
- On amd64, inserting a plain `ret` before entering libc avoids stack-alignment
  crashes in `system()`.

## Flag

`HTB{redacted}`
