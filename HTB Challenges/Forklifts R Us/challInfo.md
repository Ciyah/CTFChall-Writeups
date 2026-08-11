---
ctf: HTBLabs
title: Forklifts R Us
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Forklifts R Us

## Challenge
Something's off with the forklift firmware. The diagnostic terminal runs a Forth interpreter — and it seems to accept more than just the standard commands.IP: 154.57.164.82:32087

## Approach

1. Connect to the service and select option `3` to enter the Forth
   diagnostic interpreter.
2. Run `words` to enumerate the available Forth words.
3. Notice that `system` is exposed. This word executes an operating-system
   command from a Forth string.
4. Confirm command execution and locate the flag with:

   ```forth
   s" ls" system .
   ```

   The directory contains `flag.txt`.
5. Read it with:

   ```forth
   s" cat flag.txt" system
   ```

## Tools

- `nc`
- Forth `words` and `system`

## Lessons

An embedded interpreter should expose only a strict allowlist of required
operations. Leaving a word such as `system` available turns interpreter access
directly into arbitrary command execution.

## Flag

`HTB{redacted}`
