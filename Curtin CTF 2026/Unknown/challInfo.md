---
ctf: "Curtin CTF 2026"
title: "Unknown"
category: "forensics"
difficulty: "easy"
tags: ["file-format", "png", "byte-reversal", "magic-bytes"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

I found this unknown file somewhere, but I can’t open it.

Flag Format: CURTIN_CTF{redacted}

A ZIP archive (`Archive22.zip`) containing a single file `Chall.dat` was provided.

## Approach

### Phase 1 — Analyze

1. Extracted the file and checked its type:
   ```bash
   unzip -p Archive22.zip Chall.dat > Chall.dat
   file Chall.dat
   # Output: data  (no recognized format)
   ```

2. Inspected the first 12 bytes with `od` to look for magic bytes or partial signatures:
   ```bash
   od -An -tx1 -N12 Chall.dat
   # Output: 82 60 42 ae 44 4e 45 49 00 00 00 00
   ```

3. Identified the bytes `44 4e 45 49` as ASCII `DNEI`, which is `IEND` reversed. `IEND` is the closing chunk of every valid PNG file — finding it near the *start* of the file strongly indicated the entire file had been stored in **reverse byte order**.

### Phase 2 — Recon / Hypothesis Confirmation

The standard PNG file signature is `89 50 4e 47 0d 0a 1a 0a` (first 8 bytes). If the file is reversed, those bytes should appear at the *end* of `Chall.dat`. Reversing the full byte stream and running `file` on the result would confirm the hypothesis.

### Phase 3 — Infiltrate

4. Reversed the byte stream with a short Python script:
   ```python
   from pathlib import Path

   data = Path("Chall.dat").read_bytes()
   Path("recovered.png").write_bytes(data[::-1])
   ```

5. Verified the recovered file:
   ```bash
   file recovered.png
   # Output: recovered.png: PNG image data, ...
   ```
   The PNG signature `89 50 4e 47 0d 0a 1a 0a` was now at the start, confirming the reversal was correct.

6. Opened `recovered.png` — it was a sunset photograph with the text **`N1C3_SUNS3T_76%`** overlaid across the sky.

7. Wrapped the extracted text in the required flag format: `CURTIN_CTF{redacted}`.

## Tools

- `unzip` — extract the archive
- `file` — identify file type by magic bytes
- `od` — inspect raw hex bytes
- `python3` — one-liner to reverse byte order

## Lessons

- When `file` reports `data` and the file has no recognizable format, dump the first (and last) 16 bytes and look for well-known magic bytes that might be reversed, XOR’d, or otherwise transformed.
- PNG files always start with `89 50 4e 47` and end with `49 45 4e 44 ae 42 60 82` (`IEND` chunk + CRC). Seeing either chunk at the wrong end immediately points to byte-order reversal.
- A simple `data[::-1]` in Python is enough to reverse an entire file — no external tools needed.

## Flag

`CURTIN_CTF{redacted}`
