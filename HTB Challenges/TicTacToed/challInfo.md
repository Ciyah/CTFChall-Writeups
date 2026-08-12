---
ctf: HTBLabs
title: TicTacToed
category: pwn
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# TicTacToed

## Challenge
A lawfirm recently busted an underground network of a part-time cybermafia group. Upon investigation they found nothing but a single tic-tac-toe game on their computer. The forensics team suspect it to be more than just a game. Can you expose them ? IP: 154.57.164.65:30105

## Approach

1. Reverse the Rust binary and recover the hidden move-history regex:
   `X:00O:04X:11O:13X:22O:31X:33O:40X:44`.
2. XOR the three encrypted access-code fragments with `0x5a`, yielding
   `D3f1n3tlya71c74c703gam3`.
3. In the embedded C2 binary, use `H` to leak the PIE address of
   `generateUserID`.
4. Use `E` + `Y` to free the global Agent while leaving its pointer dangling.
5. Select `F`: its `malloc(8)` reuses the Agent chunk and its raw `read(8)`
   replaces the callback with `getSecret` at `leak - 0x1a0`.
6. The subsequent indirect callback reads and prints `flag.txt`.

## Tools

- `nm`, `objdump`, `readelf`, `strings`
- Python socket exploit: `solve.py`

## Lessons

- A hidden game-state regex can serve as a second-stage unlock condition.
- Mixing a dangling function-pointer object with a same-size allocation gives
  a direct use-after-free callback overwrite.
- A function-pointer leak is enough to defeat PIE when the target callback is
  at a known relative offset.

## Flag
HTB{redacted}
