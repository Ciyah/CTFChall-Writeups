---
ctf: HTBLabs
title: Simple Encryptor
category: rev
difficulty: easy
tags: [reverse-engineering, prng, xor, bit-rotation]
flag_format: HTB{...}
date: 2026-08-11
---

# Simple Encryptor

## Challenge
On our regular checkups of our secret flag storage server we found out that we were hit by ransomware! The original flag data is nowhere to be found, but luckily we not only have the encrypted file but also the encryption program itself.

## Approach

1. Inspected the supplied files with `file`, `strings`, and `xxd`. The encryptor is an unstripped 64-bit ELF executable, and `flag.enc` contains 32 bytes.
2. Disassembled the `main` function with `objdump`. The program obtains the current Unix timestamp with `time(NULL)`, truncates it to 32 bits, and passes it to `srand()`.
3. For every plaintext byte, the program:
   - XORs it with the low byte of the first `rand()` result.
   - Calls `rand()` again and rotates the byte left by `rand() & 7` bits.
4. Before writing the encrypted bytes, the program writes the four-byte PRNG seed at the beginning of `flag.enc`. The stored little-endian seed is `0x62b1355a` (`1655780698`). This makes the complete random sequence reproducible.
5. Reproduced glibc's `rand()` sequence with the stored seed. For each ciphertext byte, reversed the operations in the opposite order: rotate right by the second random value, then XOR with the low byte of the first random value.
6. Re-encrypted the recovered plaintext using the same seed and confirmed that the result matches the supplied `flag.enc` byte for byte.

## Tools

- `file` — identified the executable and encrypted data file types.
- `strings` — exposed imported functions such as `time`, `srand`, and the input/output filenames.
- `objdump` — disassembled `main` and revealed the encryption algorithm.
- `xxd` — displayed the raw seed and ciphertext bytes.
- Python (`ctypes`, `struct`, and `pathlib`) — called glibc's PRNG, decrypted the file, and verified the result by re-encryption.

## Lessons

- A pseudorandom stream is not secret when its seed is stored next to the ciphertext.
- PRNG compatibility matters: reproducing this challenge requires glibc's `rand()` behavior, not Python's unrelated `random` implementation.
- To invert a sequence of transformations, apply their inverses in reverse order. Here, rotate-right must happen before XOR.
- A known flag prefix such as `HTB{` is useful as a quick sanity check, while exact re-encryption provides stronger verification.

## Flag
HTB{redacted}
