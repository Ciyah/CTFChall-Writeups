---
ctf: HTBLabs
title: Coffee Invocation
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-13
---

# Coffee Invocation

## Challenge
Our new crazy conspiracy theorist intern, has blocked everyone from the coffee machine because he saw that aliens were trying to steal the out of the world secret recipe. Your mission is to unveil the secrets that lie behind his profound madness and teach him a javaluable lesson.

## Approach

The ELF embeds two Java 17 class files and launches a JVM through JNI. Native
code mutates the boxed primitive caches and replaces `Shutdown.halt0`, allowing
Java `System.exit` calls to act as state transitions instead of terminating.

`Verify1` checks the first 26 bytes. The mutated `Byte` cache adds `0x51`, while
the mutated `Short` cache negates the target byte. Inverting the comparison
produces `1_c4nt_c4ptur3_fl4g5_unt17`.

`Verify2` checks bytes 26 through 51 in pairs. The launcher swaps boxed Boolean
values, leaves each source pair unsorted, sorts the entire decoy string, and
selects a different pair after each intercepted exit. Invert the 13 corrupted
Character-cache permutations to recover `_1v3_h4d_a1l_my_0xCAFEBABE`.

## Tools

- `objdump`, `xxd`, and `radare2`
- CFR Java decompiler
- `solve.py`

## Lessons

JNI can alter normally immutable Java wrapper caches, so decompiled Java alone
does not describe the effective comparisons. Track the native cache mutations
and the exact substring passed to each embedded class.

## Flag

`HTB{redacted}`
