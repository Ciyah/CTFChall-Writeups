---
ctf: "Curtin CTF 2026"
title: "Stagehand"
category: "web"
difficulty: ""
tags: []
flag_format: "CTF{...}"
date: "2026-11-21"
---

## Challenge

The Understudy Players are in dress rehearsal and the backstage desk prints a pass for everyone. The stage manager swears nobody can forge a pass, they are signed. Somebody left something lying around the desk, though. Can you find it?
curtinmy-stagehand.chals.io 

## Approach

**Phase 1 — Analyze**

1. Examined the challenge description: signed PHP cookie ("pass"), hint about something "left lying around".
2. Retrieved source backup `index.php~` via fuzzing common editor-backup filenames (`index.php~` returned HTTP 200). Saved as `src.php`.
3. Source revealed 4 classes: `CrewPrefs` (cookie data), `ShowReport` (`__destruct` echoes `$line`), `Poster` (`__toString` calls `$content->caption()`), `CueSheet` (`__call` does `glob()+file_get_contents` under `/var/www/`).
4. Cookie format: `base64(abbreviate(serialize(CrewPrefs))) . "." . HMAC-SHA256(blob, $SECRET)`.
5. `abbreviate()` runs AFTER `serialize()`, replacing `dress rehearsal` → `DR` (13 bytes shorter) without updating PHP's `s:<len>:` length prefixes.

**Phase 2 — Recon / Vulnerability Identification**

6. The desync bug: placing `dress rehearsaldress rehearsal` (30 chars) in `name` causes `serialize()` to write `s:30:"..."`. `abbreviate()` shrinks the value to `DRDR` (4 chars) but leaves the length as 30. When `unserialize()` reads, it over-reads 26 bytes beyond the 4-char content, consuming the stream bytes that follow — including the `";s:7:"tagline";s:<TL>:"` structure.
7. For a 3-digit tagline length (`TL`), over-read is 26, padding prefix is `20+3=23` → we land 3 bytes into the tagline value. Placing `AAA` + `";s:1:"x";` + gadget in tagline causes `unserialize` to treat the gadget as a fresh property of `CrewPrefs`.
8. POP chain: `ShowReport` (`__destruct` → string cast `$line`) → `Poster` (`__toString` → calls `$content->caption()`) → `CueSheet` (`__call('caption',...)` → `glob($pattern)` + `file_get_contents`).
9. The server signs the desynced (already-malicious) blob itself in `seal()`, so we never need the secret: POST the crafted name/tagline, receive a legitimately-signed malicious cookie, replay it.

**Phase 3 — Infiltrate**

10. Generated payload with `forge_solver.php` targeting `/var/www/flag*` (flag was NOT in `/var/www/html/`).
11. Ran `pwn.sh '/var/www/flag*'`:
    - POST with crafted name/tagline → server signs and returns malicious cookie in `crew.txt`.
    - GET with that cookie → `ShowReport::__destruct()` fires, echoes flag in HTML comment.

```bash
cd /home/ciyah/Desktop/Curtin\ CTF\ 2026/Stagehand
php forge_solver.php '/var/www/flag*' | sed 's/^POSTBODY=//' > /tmp/body.txt
curl -s -X POST https://curtinmy-stagehand.chals.io/ --data "$(cat /tmp/body.txt)" -c crew.txt >/dev/null
curl -s https://curtinmy-stagehand.chals.io/ -b crew.txt | grep -i 'show report'
# <!-- show report: [CURTIN_CTF{redacted}] -->
```

## Tools

- `curl` — recon, source backup retrieval, exploit delivery
- `forge_solver.php` — computes aligned name/tagline values for the desync attack
- `pwn.sh` — wrapper: POST to get signed cookie, GET to trigger gadget
- `php` (local) — serialize/abbreviate length math

## Lessons

- **Sign the final wire form, not an intermediate.** Transforming a payload after signing (even abbreviation) lets an attacker craft inputs whose post-transform bytes differ from the pre-sign form — the server signs the attacker's object for them.
- **Never `unserialize()` user-influenced data**, even when HMAC-verified, because the HMAC can be computed over a maliciously shaped blob the server produced itself.
- **Editor backups in the webroot** (`index.php~`) expose source, gadget classes, and the signing logic needed to plan the attack.
- Flag lives at `/var/www/flag*`, not `/var/www/html/flag*` — always scan both.

## Flag

`CURTIN_CTF{redacted}`

