---
ctf: HTBLabs
title: Zigzag
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Zigzag

## Challenge
VAULTRIX runs the quiet backend for people who need something to vanish — blackmail files, insider ledgers, kill lists rebranded as enterprise notes. Tonight one of those notes goes to auction, and your handler wants it gone before the bidding closes. Their pitch deck brags — We rewrote our entire backend in Zig. No garbage collector. No hidden allocations. No glibc heap exploits from 2015. Memory safety isn't a feature — it's the foundation. — but you've got a leaked socket, a countdown, and a hunch that memory safe doesn't mean exploit safe. IP:154.57.164.73:32418

## Approach

`GET` and `PATCH` allow 48-byte operations even when a note's data is only
24 bytes. Data buffers and 24-byte note records share an allocator size class,
so the overrun reaches the record's pointer and length fields, stopping just
before its callback pointer. Corrupting note 0's pointer turns it into an
arbitrary read/write primitive. This is used to leak the PIE address of note
1's render callback, then replace that callback with the binary's hidden
`execve("/bin/sh", ...)` routine at PIE offset `0x6b820`. `RENDER 1` invokes
the corrupted callback and yields a shell.

## Tools

- `objdump`, `readelf`, `strings`
- Python standard library exploit (`solve.py`)

## Lessons

Bounds checks against a logical maximum do not establish that a requested
range fits the allocation. Function pointers next to user-controlled heap
data turn a small linear overflow into control-flow hijacking.

## Flag
HTB{redacted}
