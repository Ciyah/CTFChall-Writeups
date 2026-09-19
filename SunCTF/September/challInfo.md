---
ctf: SunCTF
title: September
category: misc
difficulty: unknown
tags: []
flag_format: sunctf26{...}
date: 2026-09-05
---

# September

## Challenge
Something seems off with my MIDI...

## Approach
1. `file September.mid` identified a format-1 MIDI containing 18 tracks at 384
   ticks per quarter note. `strings -a -n 4 September.mid` exposed the track
   names; the final track, `TUBA`, was suspicious.
2. Parsing the tracks showed that `TUBA` contains 46 copies of only MIDI note
   45, all at velocity 64. The data is in the timing: notes of about 192 ticks
   are Morse dots, notes of about 384 ticks are dashes, 384-tick rests separate
   letters, and the 1536-tick rest separates words. A few timings differ by a
   handful of ticks because of the song's tempo mapping, so the decoder uses
   thresholds between the two values.
3. Run the included decoder from this directory:

   ```sh
   python3 solve.py
   ```

   It prints the Morse tokens and decodes them as `SUNCTF26 BADEEYAA`.
4. Applying the flag format's lowercase prefix and braces produces the flag.

## Tools

- `file`, `strings`, `xxd`
- Python 3 standard library (custom Standard MIDI File event parser)

## Lessons

In a MIDI steganography challenge, inspect each track independently. A track
that repeatedly plays one pitch can encode information through note duration
and rests even when its note and velocity values reveal nothing.

## Flag

`sunctf26{badeeyaa}`
