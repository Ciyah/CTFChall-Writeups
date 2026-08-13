---
ctf: HTBLabs
title: Thief
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-13
---

# Thief

## Challenge
There is a surprisingly high number of requests on our network - we hope that our data hasn't been compromised.

## Approach

1. Follow TCP stream 0 to recover the attacker's PowerShell session. The
   attacker downloads `windowsupdate.exe` over HTTP, then runs it against
   `1dub.png`.
2. Export the HTTP object and unpack it as a PyInstaller application. Its
   Python code encrypts each 256-byte file chunk with AES-CBC using the key
   `The Bloodharbor!`; each ICMP payload is `exfil- || IV || ciphertext`.
3. The ICMP identifier is the depth in the malware's binary-tree scrambler,
   while the sequence number is the position at that depth. Sort depths in
   ascending order, sequence numbers ascending for even depths and descending
   for odd depths.
4. Decrypt and concatenate all 48 echo-request payloads. Disable Wireshark's
   `hipercontracer` dissector so it does not consume five payloads that happen
   to match that protocol's magic value. The result is the original PNG.

## Tools

- tshark
- PyInstaller archive viewer / uncompyle6
- PyCryptodome

## Lessons

- Protocol heuristics can hide raw payload bytes from `data.data`; disabling a
  falsely matched dissector restores them.
- ICMP identifier and sequence fields can carry ordering metadata in addition
  to the exfiltrated bytes.

## Flag

`HTB{redacted}`
