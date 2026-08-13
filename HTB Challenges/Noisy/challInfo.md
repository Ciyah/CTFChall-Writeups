---
ctf: HTBLabs
title: Noisy
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-13
---

# Noisy

## Challenge
Encrypting data with discrete values is all very well and good, but there’ll always be a finite number of outputs, and I hate anything you can brute force. That’s why I use continuous values to store my flags! It’s just… quite hard to get them back.

## Approach

The waveform is a sum of sinusoids. An FFT recovers each sinusoid's frequency and
amplitude. Its amplitude is `i + 1`, so it directly reveals the character's flag
position. Its frequency is `0.1 * ord(c) * 4**k`, where `k` is the number of prior
uses of that character. Process the components in amplitude order and keep a
counter for already-decoded characters to recover each printable ASCII value.

## Tools

- NumPy FFT
- SciPy WAV reader

## Lessons

Continuous-valued output does not prevent recovery when the signal is made from
perfectly separated deterministic frequencies, especially when amplitude leaks
the original ordering.

## Flag

`HTB{redacted}`
