---
ctf: HTBLabs
title: TrueSecret
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# TrueSecret

## Challenge
Our cybercrime unit has been investigating a well-known APT group for several months. The group has been responsible for several high-profile attacks on corporate organizations. However, what is interesting about that case, is that they have developed a custom command & control server of their own. Fortunately, our unit was able to raid the home of the leader of the APT group and take a memory capture of his computer while it was still powered on. Analyze the capture to try to find the source code of the server.

## Approach

1. Identify the image as 32-bit Windows 7 SP1 memory (PAE).
2. Find the active `TrueCrypt.exe` and `7zFM.exe` processes.
3. Locate and recover `backup_development.zip`; it contains `development.tc`.
4. Recover the cached TrueCrypt passphrase from RAM:
   `X2Hk2XbEJqWYsh8VdbSYg6WpG9g7`.
5. Mount `development.tc` and inspect `malware_agent/AgentServer.cs`.
6. The server encrypts Base64 session records with DES-CBC using key
   `AKaPdSgV` and IV `QeThWmYq`.
7. Decrypt the final session record with `solve.py` to recover the flag.

## Tools

- Volatility 2 (`Win7SP1x86_23418`)
- VeraCrypt/TrueCrypt-compatible mounting
- Python `cryptography`

## Lessons

- Mounted-volume passphrases and encryption material can remain in RAM.
- Volatility 2 can support older Windows images that Volatility 3 cannot stack.
- Hardcoded DES keys make recovered encrypted C2 logs straightforward to decrypt.

## Flag
`HTB{redacted}`
