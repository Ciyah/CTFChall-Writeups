---
ctf: "Curtin CTF 2026"
title: "Nano"
category: "iot"
difficulty: "easy"
tags: ["image", "hex", "ascii", "steganography", "hardware"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

> Nano RP2040 is very powerful micro controller

`Archive12.zip` contained `Nano_RP2040.png`, a photo of an Arduino Nano RP2040 Connect board.

Flag Format: CURTIN_CTF{redacted}

## Approach

### Phase 1 — Analyze

1. Extracted and examined the provided file:
   ```bash
   unzip Archive12.zip
   file Nano_RP2040.png
   # Output: PNG image data
   ```

2. Opened `Nano_RP2040.png` — a close-up photograph of an Arduino Nano RP2040 Connect board.

3. Zoomed in and rotated the image to read labels along the board's top edge. Between the `GND` and `D12` pin labels, ten two-digit values were printed:
   ```
   53 33 63 72 35 74 35 25 40 21
   ```

### Phase 2 — Recon / Hypothesis Confirmation

The values are each in the range `20`–`7E` (printable ASCII range in hex), strongly suggesting they are ASCII character codes encoded in hexadecimal rather than actual pin labels or electrical values.

### Phase 3 — Infiltrate

4. Decoded the hex sequence as ASCII:
   ```python
   print(bytes.fromhex("533363723574352540 21".replace(" ", "")).decode("ascii"))
   # Output: S3cr5t5%@!
   ```

   Full one-liner used:
   ```python
   print(bytes.fromhex("53336372357435254021").decode("ascii"))
   ```

5. Wrapped the decoded string in the required flag format: `CURTIN_CTF{redacted}`.

## Tools

- Image viewer / photo editor — zoom and rotate `Nano_RP2040.png` to read board labels
- `python3` — hex-to-ASCII decoding

## Lessons

- IoT challenges often hide flags in photographs of hardware — read every label, silkscreen text, and pin marking carefully.
- Two-digit hex values in the printable ASCII range (20–7E) are a strong hint that the data encodes text, not raw numbers.
- A simple `bytes.fromhex(...).decode("ascii")` is sufficient once the hex string is extracted.

## Flag

`CURTIN_CTF{redacted}`

