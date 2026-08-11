---
ctf: HTBLabs
title: Lucky Dice
category: misc
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Lucky Dice

## Challenge
How fast can you keep score? IP: 154.57.164.82:31793

## Approach

The service prints every player's dice for 100 rounds and allows only 0.3
seconds to identify the player with the greatest sum.  Parse each `Player N:`
line as it arrives, sum its dice, and answer as soon as `Who wins this round?`
is received.  Use `(score, player_number)` as the comparison key because ties
are won by the last (highest-numbered) player.

## Tools

- Python 3 socket client (`solve.py`)

## Lessons

- Process streamed data incrementally instead of waiting for the whole prompt.
- Reproduce tie-breaking behavior explicitly in the comparison key.

## Flag

`HTB{redacted}`
