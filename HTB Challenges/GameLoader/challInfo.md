---
ctf: HTBLabs
title: GameLoader
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# GameLoader

## Challenge
Despite having an updated antivirus, my computer was compromised after running a game. Investigate the game and uncover the two-part flag. IP:154.57.164.82:32599

## Approach

1. Identified `Platformer 2D.pck` as a Godot 4.1.1 PCK with an encrypted
   directory and encrypted file entries.
2. Located the `script_encryption_key` access in the matching executable near
   the encrypted-pack handling code. The global points to the following AES-256
   key in `.data`:

   `f2f44f0aaa282c6b66065b1ca437abae05e20a55a0f6b2fd85f5b90576f0c88f`

3. Decrypted the PCK directory and file entries using AES-256-CFB. The malicious
   logic is in `res://player/player.gd`. Its obfuscated arrays decode to:

   - Host: `g4m3l0ad3r-network.htb`
   - Download route: `p47l0ad_binary`
   - Value hashed and passed to the downloaded executable:
     `GD_M@lw4r3_PCB29543}`
4. Replayed the loader's `POST /enum`, then downloaded the second stage. The
   HTTP response header disclosed `X-Half-Flag: HTB{Und3t3ct3d_`.
5. Joined the response-header half with the decoded script half.

## Tools

- `file`, `strings`, `objdump`, `radare2`
- GDRE Tools
- Python `cryptography` (AES-256-CFB verification)
- `curl`

## Lessons

- Godot PCK encryption cannot conceal its key from the matching runtime; the
  executable must contain or reconstruct the decryption key.
- Inspect response headers as well as response bodies in staged-loader
  challenges.
- Avoid executing an unknown loader or downloaded PE; all required behavior can
  be recovered statically and by replaying only the HTTP requests.

## Flag

`HTB{redacted}`
