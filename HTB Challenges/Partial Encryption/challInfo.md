---
ctf: HTBLabs
title: Partial Encryption
category: rev
difficulty: unknown
tags: [aes-ni, self-modifying-code, dynamic-analysis, windows-pe]
flag_format: HTB{...}
date: 2026-08-11
---

# Partial Encryption

## Challenge
Static-Analysis on this program didn't reveal much. There must be a better way to approach this...

## Approach

The executable is a 64-bit Windows PE. Normal string extraction does not expose
the flag because the interesting routines are stored encrypted in `.data` and
only copied into executable memory when needed.

The dispatcher at `0x140001050` makes this behavior clear:

1. It allocates memory with `VirtualAlloc`.
2. It processes the source in 16-byte blocks.
3. It calls the AES-NI routine at `0x140001000` for every block.
4. It changes the allocation to executable memory with `VirtualProtect`.
5. The caller executes the decrypted allocation and then releases it with
   `VirtualFree`.

The block index is broadcast to all 16 bytes and used to generate the two AES
operands. In intrinsics, one block is decrypted as:

```c
__m128i index = _mm_set1_epi8(i);
__m128i a = _mm_aeskeygenassist_si128(index, 0x00);
__m128i b = _mm_aeskeygenassist_si128(index, 0x10);
plain = _mm_aesdeclast_si128(_mm_xor_si128(cipher, b), a);
```

I reproduced this in `solve.c` and applied it to the encrypted blobs referenced
by the outer dispatcher:

| RVA | Size |
| --- | ---: |
| `0x4000` | `0x70` |
| `0x4070` | `0x40` |
| `0x40b0` | `0x30` |
| `0x40e0` | `0x30` |
| `0x4110` | `0x30` |
| `0x4140` | `0x1a0` |
| `0x42e0` | `0x1e0` |
| `0x44c0` | `0x270` |
| `0x4730` | `0x100` |

The block counter restarts at zero for each blob. Build and run the helper with:

```bash
gcc -O2 -maes -msse4.1 solve.c -o solve
./solve Partial\ Encryption/rev_partialencryption/partialencryption.exe decrypted.exe
dd if=decrypted.exe of=/tmp/decrypted_data.bin bs=1 skip=9728 count=2128 status=none
objdump -D -b binary -m i386:x86-64 -Mintel \
  --adjust-vma=0x140004000 /tmp/decrypted_data.bin
```

The recovered code checks `argv[1]` one position at a time. The checks are split
across four decrypted validator functions, presumably to frustrate static
analysis. In position order they require:

```text
0..3   HTB{
4..9   W3iRd_
10..17 RUnT1m3_
18..21 DEC}
```

The outer routine loops over 22 input positions and rejects the input if any
earlier NUL byte is found. Thus the complete flag has exactly 22 characters.

## Tools

- `file`, `strings`, and `objdump` for PE inspection and disassembly
- GCC AES intrinsics to reproduce the binary's AES-NI transformation
- `dd` to extract the decrypted `.data` region for raw disassembly

## Lessons

- When encrypted routines are copied to temporary executable allocations, the
  loader/decryptor is often far more useful than the encrypted bytes themselves.
- AES-NI instructions do not necessarily imply conventional AES encryption. Here
  `AESKEYGENASSIST` and `AESDECLAST` are composed as a custom reversible block
  transform.
- Each encrypted function is an independent blob, so its block index must be
  reset during offline decryption.

## Flag

`HTB{redacted}`
