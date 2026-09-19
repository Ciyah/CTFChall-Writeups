---
ctf: SunCTF
title: AttckDef Revenge
category: misc
difficulty: unknown
tags: []
flag_format: sunctf26{...}
date: 2026-09-06
---

# AttckDef Revenge

## Challenge
SUNCTF AD attack/defence, version 2.

Recover the final sunctf26{...} flag from the range and submit it here.

Launch the range from this challenge and keep the generated instance URL private to your team. Use that full URL as the base URL for solver scripts. Challenge support: @Kitkat in the event Discord. https://sunctf.sunwaycybersecurityclub.org/plugins/team-runtime-auth/launch/5

## Approach
1. `README.md` establishes that a gameserver creates a flag note every 120
   seconds and that a successful `/api/submit` returns the league flag.  The
   PCAP shows Scap3G04T creating 320 notes in roughly nine seconds before it
   predicts five gameserver share tokens exactly.
2. The flaw is in `source/app/tick.py:16,35-36`: one process-global
   `random.Random()` (MT19937) generates every user and gameserver note token.
   The public account/note API returns attacker-owned tokens.  Each UUID leaks
   four consecutive 32-bit outputs, so 156 notes leak all 624 MT19937 state
   words.  This bypasses the patched token equality check and CAPTCHA entirely.
3. `solve.py` registers 32 accounts and creates five notes per account, clones
   the generator from the first 156 UUIDs, and verifies the next four observed
   UUIDs.  It then predicts the next token, waits for the next `/api/flag_ids`
   entry, and sends that token once to `/api/notes/validate-token`.
4. The returned `SUN26...` note content is submitted with its exact
   `gameserver:NOTE-...` flag ID to `/api/submit`, whose accepted response
   contains the final `sunctf26{...}` flag.  The successful live run predicted
   token `8ed84aa8-4a9d-894d-dc1d-10be8589a056`, which released
   `SUN26EJLYFM6EVJUWFIB52CQJMKIZ` from
   `gameserver:NOTE-26220652-1FFD66`.

## Tools

- `tshark` for reconstructing Scap3G04T's HTTP requests from `old_attack.pcap`
- Python standard library for the automated exploit

## Lessons

- Access tokens must use a CSPRNG such as `secrets`, not a shared MT19937.
- Strict equality and rate limiting do not protect tokens whose generator state
  is recoverable from other API responses.

## Flag

`sunctf26{mt19937_624_w0rds_0wn_th3_str34m}`
