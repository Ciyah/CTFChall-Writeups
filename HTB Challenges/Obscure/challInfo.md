---
ctf: HTBLabs
title: Obscure
category: forensics
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Obscure

## Challenge
An attacker has found a vulnerability in our web server that allows arbitrary PHP file upload in our Apache server. Suchlike, the hacker has uploaded a what seems to be like an obfuscated shell (support.php). We monitor our network 24/7 and generate logs from tcpdump (we provided the log file for the period of two minutes before we terminated the HTTP service for investigation), however, we need your help in analyzing and identifying commands the attacker wrote to understand what was compromised.

## Approach

1. Removed the junk token `u)` from `support.php`. The reconstructed implant
   uses the key `80e32263`, searches request bodies between the markers
   `6f8af44abea0` and `351039f4a7b5`, then performs Base64 decode, repeating-key
   XOR, and zlib decompression before evaluating the plaintext.
2. Extracted the four POST bodies and their HTTP responses from the PCAP with
   `tshark`, then reversed that encoding in `solve.py`.
3. The recovered commands were:

   - `id`
   - `ls -lah /home/*`
   - `chdir('/home/developer')`
   - `base64 -w 0 pwdb.kdbx`

4. Decoded the last response a second time as Base64, producing a valid KeePass
   2.x database (`pwdb.kdbx`). `keepass2john` extracted its hash, and John found
   the database password `chainsaw` in `rockyou.txt`.
5. Opened the database and read the entry named `Flag`.

## Tools

- tshark
- Python (`solve.py`)
- keepass2john / John the Ripper
- PyKeePass

## Lessons

The shell is a Weevely-style backdoor. Both request and response bodies use the
same Base64/XOR/zlib protocol, while command output may add another encoding
layer (the attacker used Base64 to make the binary KeePass file safe to print).

## Flag

`HTB{redacted}`
