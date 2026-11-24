---
ctf: "Curtin CTF 2026"
title: "Captured whispers"
category: "iot"
difficulty: ""
tags: []
flag_format: "CTF{...}"
date: "2026-11-21"
---

## Challenge

Captured whispers, hidden stories, and echoes of untold secrets

Flag Format: CURTIN_CTF{redacted}


## Approach

### Phase 1 — Analyze

1. `Archive24.zip` contained `Chall.sal`, a Saleae Logic 2 capture recorded at **24 MHz**.
2. Inspected digital channel 1: short pulses ~5,000 samples wide, longer pulses at multiples of that width. At 24 MHz, 5,000 samples ≈ 208 µs → **4,800 bps** baud rate.
3. The signal idled low, indicating **inverted polarity** — consistent with a non-standard UART line or level-shifted signal.

### Phase 2 — Recon

4. Opened `Chall.sal` in Saleae Logic 2, added an **Async Serial** analyzer:

   | Setting   | Value           |
   |-----------|-----------------|
   | Input     | Digital ch. 1   |
   | Bit rate  | 4,800           |
   | Data bits | 7               |
   | Parity    | Even            |
   | Stop bits | 1               |
   | Bit order | LSB first       |
   | Signal    | Inverted        |

5. Decoded frames passed even-parity checks and produced readable ASCII. Near the end of the transcript a shell session appeared with the line:
   ```
   shell> cat /etc/motd
   zJLgHX&fTX'sHI+xzZ\xSV_d}tLKSi
   shell> logout
   ```

### Phase 3 — Infiltrate

6. Brute-forced single-byte XOR keys against the `/etc/motd` line. Key **`0x1E`** produced a valid Base64 string: `dTRyVF8xJF9mVW5fdDBfMHAzcjRUMw`.
7. Added `==` padding and Base64-decoded to get the flag body.

```python
import base64

motd = rb"zJLgHX&fTX'sHI+xzZ\xSV_d}tLKSi"
encoded = bytes(b ^ 0x1E for b in motd)
padded = encoded + b"=" * (-len(encoded) % 4)
body = base64.b64decode(padded, validate=True).decode("ascii")
print(f"CURTIN_CTF{redacted}}}")
```

Run: `python3 solve.py`

## Tools

- Saleae Logic 2 (UART / Async Serial decoder)
- Python 3 (`solve.py` — XOR brute-force + Base64 decode)

## Lessons

- When a digital capture idles low, try **inverted** polarity in the UART decoder before assuming the data is noise.
- Pulse-width estimation from sample count at known sample rate is a quick way to guess baud rate without a frequency analyzer.
- Short obfuscated strings in shell output (motd, env vars) are worth trying single-byte XOR; a valid Base64 output is a strong confirmation signal.

## Flag

`CURTIN_CTF{redacted}`

