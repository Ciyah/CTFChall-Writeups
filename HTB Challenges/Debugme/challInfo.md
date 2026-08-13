---
ctf: HTBLabs
title: Debugme
category: rev
difficulty: unknown
tags: [windows, pe, anti-debug, self-modifying-code, xor]
flag_format: HTB{...}
date: 2026-08-13
---

# Debugme

## Challenge

> A developer is experimenting with different ways to protect their software.
> They have sent in a Windows binary that is supposed to be super secure and
> really hard to debug. Debug it and see if you can find the flag.

Artifact: `Debugme/debugme.exe`

- SHA-256: `da9814d7773262d69631d8c0f6f17cb1a55e8ac4e56d0e18f0ea05fbd0f6da1d`
- Format: 32-bit x86 PE, MinGW, console application
- Image base: `0x400000`
- Entrypoint: `0x4010f9`

## Approach

### 1. Triage

Initial inspection shows an unstripped MinGW binary with an unusual `main`:

```console
$ file Debugme/debugme.exe
PE32 executable for MS Windows 4.00 (console), Intel i386, 14 sections

$ objdump -t Debugme/debugme.exe | rg mash.asm
mash.asm
```

The symbols identify the challenge-authored object as `mash.asm` and place
`main` at `0x401620`. Disassembling that address produces nonsense because the
routine is encrypted in the file.

### 2. Hidden pre-entry stub

The nominal entrypoint begins with a jump outside `.text`'s declared virtual
size:

```asm
004010f9  jmp 0x408904
```

Address `0x408904` corresponds to file offset `0x7d04`, inside the raw padding
at the end of `.text`. Section-aware disassembly can therefore miss it. The
stub implements three anti-debug checks:

1. Read `PEB.BeingDebugged` from `fs:[0x30] + 0x02` and require zero.
2. Read `PEB.NtGlobalFlag` from `fs:[0x30] + 0x68` and require zero.
3. Execute `RDTSC` twice around junk instructions and require a delta no
   greater than `0x3e8` ticks.

If any check fails, execution takes the failure path at `0x408992`. Otherwise,
the following loop decrypts `main` in place:

```asm
mov eax, 0x401620
decrypt:
    xor byte [eax], 0x5c
    inc eax
    cmp eax, 0x401791
    jle decrypt
```

The stub then jumps back to `0x4010ff`, immediately after the original entry
jump, allowing normal CRT initialization to continue.

### 3. Decrypted main

Applying XOR `0x5c` to the inclusive range `0x401620..0x401791` reveals the
real routine. It repeats the same PEB and timing checks and prints decoy
messages on failure. On success, instructions between `0x4016b4` and
`0x401771` construct nine DWORDs on the stack using `mov`, `add`, `sub`, `and`,
and `push` instructions.

Because x86 is little-endian and each `push` grows the stack downward, the
DWORD order must be reversed while preserving the byte order within each
DWORD. This reconstructs the 36-byte ciphertext:

```text
1f397b272722252c140a253f7a140f78293e0c0c2e19143f39222820311419142d3e256a
```

The tail of the routine supplies both parameters directly:

```asm
mov ecx, 0x24  ; length = 36
mov ebx, 0x4b  ; XOR key
```

XORing each ciphertext byte with `0x4b` produces:

```text
Tr0lling_Ant1_D3buGGeR_trickz_R_fun!
```

Wrapping that value in the required `HTB{...}` format yields the flag.

### 4. Reproduction

`solve.py` maps the encrypted virtual-address range to its raw file offsets,
applies the first XOR layer, emulates only the small EAX/PUSH instruction
subset used to build the ciphertext, and applies the final XOR:

```console
$ python3 solve.py
HTB{redacted}
```

This is a fully static solution; Wine and a Windows debugger are unnecessary.

## Tools

- `file`, `strings`, `objdump`, `radare2`
- Python 3 (`solve.py`)

## Lessons

- PE raw padding can contain executable code omitted by section-aware tools.
- Anti-debug checks do not protect ciphertext and keys from static extraction.
- When `main` is encrypted, inspect code executed before the CRT and emulate
  only the small instruction subset needed to recover the data.

## Flag

`HTB{redacted}`
