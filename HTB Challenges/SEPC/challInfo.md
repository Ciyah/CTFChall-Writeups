---
ctf: HTBLabs
title: SEPC
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-13
---

# SEPC

## Challenge
We've extracted an embedded operating system running on an intercepted deep-space satellitle launched by Arodor. If we can breach the secure enclave and extract their security mechanisms, we can crack their encrypted communications

## Approach

The initramfs contains a stripped userspace program, `checker`, and an unstripped
kernel module, `checker.ko`. The init script loads the module, creates
`/dev/checker`, and starts the userspace program.

The userspace program reads a line and sends it to the device one byte at a
time. The module's write handler stores the current byte. Its read handler uses
an index `i` and tests it against:

```c
input_byte == rodata[0x20 + i] ^ rodata[0x60 + i]
```

XORing the two 34-byte tables produces:

```text
HTB{grabbing_d4t4_fr0m_k3rn3l5p4c3
```

After byte index 33 matches, the driver returns status 2 (success). This is an
off-by-one design error: no closing brace is checked. For the flag format, append
the closing brace.

## Tools

- `cpio`, `readelf`, `objdump`, `strings`
- `solve.py`

## Lessons

Relocations in a kernel module make the data references explicit even when
decompilation is unavailable. Following the file-operation pointers from
`.rela.data` quickly identifies the open, read, and write handlers.

## Flag

`HTB{redacted}`
