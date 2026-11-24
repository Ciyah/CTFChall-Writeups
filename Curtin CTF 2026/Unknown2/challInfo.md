---
ctf: "Curtin CTF 2026"
title: "Unknown2"
category: "forensics"
difficulty: ""
tags: [rar, password-cracking, sqlite, hex-encoding, john-the-ripper]
flag_format: "CURTIN_CTF{...}"
points: 240
hint: "Just Love"
date: "2026-11-21"
---

## Challenge

I found another unknown file somewhere, but I can’t open it.

Flag Format: CURTIN_CTF{redacted}

An extensionless file called `Unknown2` is provided.

## Approach

### Phase 1 — Analyze

1. Inspected the raw header of `Unknown2` with `xxd -g1 -l 16 Unknown2`.
   - First 8 bytes: `aa bb cc dd 1a 07 01 00`
   - RAR5 magic: `52 61 72 21 1a 07 01 00` (`Rar!` in ASCII)
   - The final four bytes matched RAR5; only the first four were corrupted.

### Phase 2 — Recon

2. Repaired the archive by overwriting the first four bytes with the correct RAR5 signature:
   ```
   cp -- Unknown2 Unknown2.rar
   printf ‘Rar!’ | dd of=Unknown2.rar bs=1 conv=notrunc status=none
   ```
3. Extracted the hash for cracking:
   ```
   rar2john Unknown2.rar > unknown2.hash
   ```
   John identified it as RAR5 / PBKDF2-SHA256 with 32,768 iterations.

4. Used the hint "Just Love" to narrow the password search — filtered rockyou.txt for entries containing "love" (case-insensitive):
   ```
   LC_ALL=C grep -aiF ‘love’ /usr/share/wordlists/rockyou.txt > love-candidates.txt
   ```
   Yielded 206,800 candidates.

### Phase 3 — Infiltrate

5. Cracked the password with John the Ripper:
   ```
   john --session=unknown2-love --wordlist=love-candidates.txt unknown2.hash
   john --show unknown2.hash
   ```
   After ~10 min 51 sec: **password = `.loveme.`** (including both periods).

6. Extracted the archive with `unrar` (7-Zip failed with "Unsupported Method"):
   ```
   unrar x -p’.loveme.’ Unknown2.rar Unknown2_unrar/
   ```

7. Identified the extracted file as a SQLite 3 database:
   ```
   file Unknown2_unrar/store.db
   sqlite3 -readonly Unknown2_unrar/store.db ‘.tables’
   ```
   Tables: `customers`, `products`, `orders`, `order_items`, `payments`, `reviews`.

8. Found the anomalous review by grouping identical title+text pairs and sorting by frequency:
   ```sql
   SELECT MIN(review_id) AS sample_id,
          COUNT(*) AS uses,
          review_title,
          review_text
   FROM reviews
   GROUP BY review_title, review_text
   ORDER BY uses, sample_id;
   ```
   Five common patterns appeared 7–26 times. `review_id 91` ("Review 56") appeared once and contained a 92-character hex-encoded body:
   `0x530x300x6d0x330x740x480x310x6e0x470x5f0x770x340x350x5f0x660x300x750x6e0x440x5f0x380x5e0x38`

9. Decoded the hex payload:
   ```
   sqlite3 -readonly Unknown2_unrar/store.db \
     ‘SELECT review_text FROM reviews WHERE review_id = 91;’ |
     sed ‘s/0x//g’ | xxd -r -p
   ```
   Output: `S0m3tH1nG_w45_f0unD_8^8`

## Tools

- `xxd` — raw hex inspection of file header
- `dd` / `printf` — in-place byte patching to repair the RAR5 signature
- `rar2john` — hash extraction from RAR archive
- `john` (John the Ripper) — password cracking with filtered wordlist
- `grep` — focused wordlist generation from rockyou.txt using the hint
- `unrar` — archive extraction with recovered password
- `file` — file type identification
- `sqlite3` — database schema inspection and SQL querying
- `sed` + `xxd -r -p` — hex decoding of the flag body

## Lessons

- Corrupted magic bytes are a common forensics trick; always check the header with `xxd` before concluding a file is unknown.
- When a hint gives a word/theme, grep rockyou.txt for that substring (case-insensitive) rather than guessing whole passwords — dramatically reduces search space.
- RAR5 archives should be extracted with `unrar`, not 7-Zip, to avoid "Unsupported Method" errors on certain compression modes.
- In a SQLite database with many similar rows, grouping by content and sorting by frequency immediately surfaces the outlier.
- Hex flag data embedded in a database field may omit the `0x` separator or use it inconsistently — `sed ‘s/0x//g’ | xxd -r -p` handles the prefixed variant cleanly.

## Flag

`CURTIN_CTF{redacted}`

