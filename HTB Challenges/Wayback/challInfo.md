---
ctf: HTBLabs
title: Wayback
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Wayback

## Challenge
A man named Michael Tanz bought 30 bitcoin in 2013 and stored it in his hardware wallet. He set the password for his hardware wallet through a password generator named V1. He remembers that his password is 20 characters long, and consisted of only alphanumeric characters and symbols. Michael however is not exactly sure of the date he generated the password - he knows it was between the 10th and the 11th of December 2013. Can you crack the password and help him recover his bitcoin ?

## Approach

Reverse engineering `generate_password()` shows that its alphabet is:

```
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_+0123456789
```

It seeds glibc `rand()` with a decimal local timestamp of the form
`YYYYMMDDHHMMSS`. Because `srand()` accepts a 32-bit unsigned integer, the
timestamp is truncated modulo `2^32`. Each password character is selected as
`alphabet[rand() % 72]`.

Brute forcing every second on 10 and 11 December 2013 gives the timestamp
`2013-12-11 13:01:25` and password `eWXtk*Oe%j5cof7Od08G`. Using that password
as the AES key (right-padded with NUL bytes to 32 bytes) decrypts the supplied
ciphertext.

## Tools

- `objdump`, `nm`, and `strings` for static analysis
- Python `ctypes` to reproduce glibc `srand()` / `rand()`
- `cryptography` for AES-256-CBC decryption

## Lessons

Time-based PRNG seeds are predictable, and truncating a timestamp to 32 bits
does not add entropy. Reproducing the exact libc PRNG and alphabet order is
essential.

## Flag

`HTB{redacted}`
