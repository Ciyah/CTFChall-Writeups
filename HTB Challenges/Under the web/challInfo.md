---
ctf: HTBLabs
title: Under the web
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Under the web

## Challenge
Dive deep under the web’s surface, where L in LFI stands for LEAK. Will you conquer the depths and claim victory? IP:154.57.164.74:30256

## Approach

1. `view.php?image=` provides an unrestricted file read. Read
   `/proc/self/maps`, the target libc, and the custom extension to recover all
   ASLR bases and symbol offsets.
2. `getImgMetadata()` allocates every matching PNG text value with
   `_emalloc_56`, then copies it with an unbounded `strcpy`. Overflow a
   `Copyright` value by 56 bytes to replace the next Zend free-list pointer.
3. Point that free-list entry at `metadata_reader.so`'s writable `strcmp` GOT
   entry. Two following metadata allocations consume the poisoned slot and
   overwrite `strcmp` with libc `system`.
4. Supply one more PNG text record whose keyword is
   `ls -1 /app > uploads/leak.png`. The parser's next `strcmp(keyword,
   "Title")` executes that keyword as a shell command.
5. Read `uploads/leak.png` through the LFI to learn the randomized 64-hex flag
   filename, then read `/app/<filename>`.

The complete exploit is in `solve.py`.

## Tools

- `readelf`, `objdump`, `gdb`
- Python standard library (PNG construction and HTTP requests)

## Lessons

- PHP's Zend allocator has a dedicated 56-byte small bin; the free-list link is
  stored directly in a freed slot's first eight bytes.
- Metadata values of length 0 or 1 are ignored by the extension, so heap-groom
  records must be at least two bytes long.
- Hijacking `strcmp` provides an immediate, attacker-controlled argument from
  the next PNG keyword and is cleaner than waiting for `efree` or `strlen`.

## Flag
HTB{redacted}
