---
ctf: HTBLabs
title: Micro Storage
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Micro Storage

## Challenge
Some group of people seem to have made a network service that lets you store files temporarily. But little did they know about the mistake they made coding their script... Try to get familiar with their service and discover the vulnerability behind it. Your goal is to leak the contents of /𝗳𝗹𝗮𝗴.𝘁𝘅𝘁. IP:154.57.164.75:30888

## Approach
The file-name filter blocks direct path traversal such as `../../flag.txt`, but the
archive function is vulnerable to GNU tar wildcard option injection. Uploaded files
whose names begin with `--` are expanded by the shell and interpreted as tar options.

1. Upload a normal file named `x` containing:
   `cp /flag.txt leaked`
2. Upload a file named `--checkpoint=1` (content is irrelevant).
3. Upload a file named `--checkpoint-action=exec=sh x` (content is irrelevant).
4. Choose **Compress and download all your files**.

The effective tar invocation processes the two crafted options and runs `sh x`, which
copies `/flag.txt` to `leaked`. Compressing again includes `leaked` in the returned
base64-encoded tar archive. Decode/extract the archive, or decode the `leaked` member,
to recover the flag.

## Tools

- `nc`
- `base64`
- GNU tar wildcard/checkpoint option injection

## Lessons

Never pass attacker-controlled filenames to shell-expanded archive commands. Use an
argument-safe API or terminate option parsing with `--` and avoid shell glob expansion.

## Flag
HTB{redacted}
