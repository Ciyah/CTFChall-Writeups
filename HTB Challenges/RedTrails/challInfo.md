---
ctf: HTBLabs
title: RedTrails
category: forensics
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# RedTrails

## Challenge
Our SOC team detected a suspicious activity on one of our redis instance. Despite the fact it was password protected it seems that the attacker still obtained access to it. We need to put in place a remediation strategy as soon as possible, to do that it's necessary to gather more informations about the attack used. NOTE: flag is composed by three parts.

## Approach

1. Inspected the TCP conversations in `capture.pcap`. The attacker at
   `10.10.0.15` authenticated to Redis (`10.10.0.90:6379`) with password
   `1943567864`.
2. In TCP stream 0, the attacker dumped the `users_table` hash. Its
   `henry6159:email` field contained the second flag part:
   `_c0uld_0p3n_n3w`.
3. The attacker wrote cron entries via `CONFIG SET DIR`, `CONFIG SET
   DBFILENAME`, `SET`, and `SAVE`. This downloaded `VgLy8V0Zxo` over HTTP.
   Reversing and base64-decoding its embedded blob revealed a persistence
   script. Its SSH-key payload contained the first part:
   `HTB{r3d15_1n574nc35`.
4. In TCP stream 2, the attacker used Redis rogue-server replication
   (`SLAVEOF`) to transfer and load `x10SPFHN.so`, then invoked
   `system.exec` to download another payload.
5. Carved the 58,928-byte ELF module from the `FULLRESYNC` response in TCP
   stream 6. Disassembly of `DoCommand` showed that command output was
   encrypted with AES-256-CBC using the hard-coded values:
   - key: `h02B6aVgu09Kzu9QTvTOtgx9oER9WIoz`
   - IV: `YDP7ECjzuV7sagMN`
6. Hex-decoding and decrypting the 960-character response to the final
   `system.exec` command exposed an environment variable containing the
   third part: `_un3xp3c73d_7r41l5!}`.

## Tools

- tshark / Wireshark
- xxd, strings, base64
- objdump
- OpenSSL

## Lessons

- Redis traffic is plaintext unless transport encryption is configured;
  authentication alone does not hide passwords or commands in a capture.
- Writable Redis configuration and module loading can turn database access
  into file writes and remote command execution.
- Rogue Redis replication can deliver a malicious shared object directly to
  a target.

## Flag

`HTB{redacted}`
