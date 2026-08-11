---
ctf: HTBLabs
title: AliEnS
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# AliEnS

## Challenge
In a groundbreaking discovery, a research lab uncovered alien technology utilizing AES encryption with custom padding. They engineered a user-friendly interface to interact with this enigmatic advancement. Now, a challenge is presented: Can you crack it? IP: 154.57.164.72:32370

## Approach

The custom padding uses Python character counts, but the result is converted to
UTF-8 only afterward. A character such as `é` counts as one character during
padding and two bytes during encryption. Adding 0 through 15 such characters
therefore moves the flag to any desired byte offset modulo the AES block size.

Although the server generates a fresh AES key for every request, ECB equality
still works among blocks in the same ciphertext. For every unknown flag byte,
the request contains 95 aligned candidate blocks (one for every printable ASCII
character). The Unicode displacement makes a block in the appended secret end
at the unknown byte. Its preceding 15 bytes are already known, initially from
the fixed `CryptoHackTheBox` string and afterward from recovered flag bytes.
Matching the secret ciphertext block against the candidate ciphertext blocks
reveals the next character. Repeat until `}`.

## Tools

- Python 3 raw socket exploit: `solve.py`

## Lessons

- Padding text before UTF-8 encoding can create a character-count/byte-count
  mismatch and defeat intended block alignment.
- A new ECB key per response prevents comparisons across responses, but does
  not prevent a codebook comparison constructed wholly inside one request.

## Flag

`HTB{39b1e545cddb21a21c4aa7e58a89df01}`
