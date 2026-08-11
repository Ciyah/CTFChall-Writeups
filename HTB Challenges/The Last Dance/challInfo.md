---
ctf: HTBLabs
title: The Last Dance
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# The Last Dance

## Challenge
To be accepted into the upper class of the Berford Empire, you had to attend the annual Cha-Cha Ball at the High Court. Little did you know that among the many aristocrats invited, you would find a burned enemy spy. Your goal quickly became to capture him, which you succeeded in doing after putting something in his drink. Many hours passed in your agency's interrogation room, and you eventually learned important information about the enemy agency's secret communications. Can you use what you learned to decrypt the rest of the messages?

## Approach

ChaCha20 is a stream cipher, so encryption XORs plaintext with a keystream.
The program initializes a new cipher twice with the same key and nonce, making
both ciphertexts start with the same keystream. Since the first plaintext is
included in `source.py`, recover the flag directly with:

`encrypted_message XOR known_message XOR encrypted_flag`

## Tools

- Python 3

## Lessons

Never reuse a key/nonce pair with a stream cipher. Doing so allows known
plaintext from one ciphertext to expose other plaintexts encrypted with the
same keystream.

## Flag

`HTB{und3r57AnD1n9_57R3aM_C1PH3R5_15_51mPl3_a5_7Ha7}`
