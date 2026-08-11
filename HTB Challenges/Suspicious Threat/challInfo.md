---
ctf: HTBLabs
title: Suspicious Threat
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Suspicious Threat

## Challenge
Our SSH server is showing strange library linking errors, and critical folders seem to be missing despite their confirmed existence. Investigate the anomalies in the library loading process and filesystem. Look for hidden manipulations that could indicate a userland rootkit.

Creds: root:hackthebox
IP: 154.57.164.78:32060

## Approach

1. Connected to the target over SSH with the supplied credentials.
2. Inspected `/etc/ld.so.preload` and found the suspicious library
   `/lib/x86_64-linux-gnu/libc.hook.so.6`.
3. Confirmed through `/proc/$$/maps` that the library was injected into
   processes. Analysis of the library showed hooks for `readdir`, `readdir64`,
   and `fopen`, plus the filtering strings `pr3l04d_` and `ld.so.preload`.
4. Bypassed the hooked directory functions by invoking Linux `getdents64`
   (syscall 217 on x86-64) directly from Python via `ctypes`.
5. The raw directory scan revealed `/var/pr3l04d_/flag.txt`, which could then
   be read directly.

## Tools

- SSH
- `/proc` process maps
- Python 3 (`ctypes` and the `getdents64` syscall)

## Lessons

An `LD_PRELOAD` userland rootkit can hide files from normal tools by hooking
libc functions such as `readdir`. Calling the underlying kernel syscall
directly bypasses that userland interception and exposes the real directory
entries.

## Flag

`HTB{redacted}`
