---
ctf: HTBLabs
title: Broken Decryptor
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Broken Decryptor

## Challenge
The decrypt function is broken and I lost my flag. Can you help me fix it? IP: 154.57.164.66:32353

## Approach

`encrypt()` XORs AES-CTR output with bytes from `os.urandom()`, but replaces every
zero byte with `0xff`. Therefore, for a fixed plaintext position, repeated
ciphertexts can take only 255 distinct values: the value corresponding to an OTP
byte of zero is always missing.

Collect many encryptions of the flag and many encryptions of an all-zero message
of the same length. The missing values are respectively `keystream XOR flag` and
`keystream`; XORing them recovers the flag. Requests are pipelined to avoid one
network round trip per sample.

## Tools

- Python socket client (`solve.py`)

## Lessons

- Replacing forbidden random values introduces a detectable bias/hole.
- Reusing an AES-CTR key and IV reuses the keystream.

## Flag

`HTB{7bc51e5d8c323f3cf9a356eec1b151ea}`
