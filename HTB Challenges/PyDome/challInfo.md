---
ctf: HTBLabs
title: PyDome
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# PyDome

## Challenge
Can you navigate the programming jungle and conquer the P7 dome? IP:154.57.164.76:31595

## Approach

1. Send 100 valid numeric story indices. A failed SHA-256 comparison prints
   the selected story text, allowing `story.txt` to be recovered in chunks.
2. Encode the SHA-256 digest of the empty string using story indices. Numeric
   selectors and single-character selectors both become indices, but only the
   latter advance the diagnostic PRNG loop.
3. Pad inputs with multi-character values. They are appended to `non_int_arr`,
   but `ord()` raises before they reach `int_arr`. This independently controls
   PRNG consumption without changing the reconstructed 64-byte digest.
4. Explore the deterministic five-attempt paths until the secret-length draw
   is zero. The expected digest is then SHA-256(`b""`). Since the reconstructed
   input ends at byte 64, `zip(forest, user_input[64:])` is empty and `all([])`
   passes the final check vacuously.

## Tools

- Python sockets
- `leak_story.py` to recover `story.txt`
- `sweep.py` to explore deterministic PRNG-consumption paths

## Lessons

- Error output can turn index validation into an arbitrary file-content leak.
- Seeded `random` is deterministic and unsuitable for secrets.
- Mutating a list before a conversion that may throw can create inconsistent
  parser state.
- `all()` over an empty iterable returns `True`.

## Flag
HTB{redacted}
