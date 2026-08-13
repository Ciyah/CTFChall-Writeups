---
ctf: HTBLabs
title: FFModule
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-13
---

# FFModule

## Challenge
After more and more recent hits of the infamous Jupiter Banking Malware we finally managed to get a sample of one module. Supposedly it steals secrets from Firefox users?

## Approach

The PE loader XORs `0x5a4` bytes at the start of `.data` with `0x72`,
allocates memory in each `firefox.exe`, copies the decrypted payload there,
and launches it with `CreateRemoteThread`.

The shellcode walks the PEB and resolves APIs dynamically. It locates
`NSS3.dll`, resolves and hooks `PR_Write`, and checks outbound buffers for
the `POST` method. Matching data is transformed and sent through a socket to
`127.0.0.1:1337`.

At payload offset `0x263` is the 32-byte encoded key. The byte transform at
offset `0x29d` is:

```text
key_byte = ROL8((encoded_byte + 0xed) & 0xff, 3) ^ 0x42
```

Applying it to all 32 bytes reveals the flag.

## Tools

- radare2 / rabin2
- objdump
- Python

## Lessons

- Extract injected shellcode before spending time on the statically linked
  loader/CRT.
- PEB walking, CRC32 API hashing, and inline strings are common shellcode
  techniques.
- Data embedded between a `call` and its target can be addressed through the
  pushed return address.

## Flag

`HTB{redacted}`
