---
ctf: "Curtin CTF 2026"
title: "Silent Frequencies"
category: "iot"
difficulty: ""
tags: ["SDR", "FSK", "IQ", "signal-processing", "radio"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

Tune into the unknown and uncover the secrets hidden in the signals

Flag Format: CURTIN_CTF{redacted}

## Approach

### Phase 1 — Analyze

1. `Archive60.zip` contained a single file `Chall.fc32` — a GNU Radio / SDR
   IQ recording stored as **little-endian complex float32** samples (the
   standard `.fc32` format). Each sample is a pair of 32-bit floats: in-phase
   (I) and quadrature (Q).

2. Loaded the file with `numpy.fromfile("Chall.fc32", dtype="<c8")` and
   plotted magnitude `|I + jQ|` over time. This revealed **10 identical
   bursts**, each **25,600 samples** long, separated by ~**100,000 samples**
   of near-zero noise → frame stride = 125,600 samples.

3. Computed the instantaneous phase change between adjacent samples:
   `angle(s[n+1] * conj(s[n]))`. Values clustered around **±0.05 rad/sample**
   — two distinct tones, confirming **binary FSK (2-FSK)** modulation.

### Phase 2 — Recon / Signal Analysis

4. Phase changes fell on **100-sample boundaries** (every 100th sample the
   tone switched or held steady). Each burst therefore carried
   `25,600 / 100 = 256 symbols = 256 bits = 32 bytes` of data.

5. Sampling the phase change at mid-symbol (sample index 49 within each
   100-sample window) avoids transition artefacts. Threshold at 0:
   - **negative phase change** (lower tone) → bit **1**
   - **non-negative phase change** (higher tone) → bit **0**

6. Packing the 256 bits **MSB-first** (`numpy.packbits`, `bitorder="big"`)
   produced a 32-byte frame whose first byte was `0xAA` (`10101010₂`) — a
   classic alternating-bit **preamble**. The remaining 31 bytes were
   printable ASCII.

### Phase 3 — Infiltrate / Decode

7. All 10 bursts produced the **identical** 32-byte frame, confirming correct
   demodulation.

8. Stripped the preamble byte and decoded bytes 1–31 as ASCII:

```bash
# Extract the IQ file
unzip -p Archive60.zip Chall.fc32 > Chall.fc32

# Run the solver
python3 solve.py
```

Output:
```
Bursts decoded : 10
Preamble byte  : 0xAA  (expected 0xAA)
Flag           : CURTIN_CTF{redacted}
```

## Tools

- Python 3 / NumPy (`numpy.fromfile`, `numpy.angle`, `numpy.packbits`)
- GNU Radio / SDR concepts (IQ samples, `.fc32` format, FSK demodulation)
- `solve.py` (included in this folder)

## Lessons

A `.fc32` file is a raw IQ recording: little-endian complex float32, two
floats per sample (I then Q). The instantaneous phase change
`angle(s[n+1] * conj(s[n]))` is the standard discriminator for FSK — it
maps directly to the transmitted tone without needing to know the carrier
frequency. Mid-symbol sampling and MSB-first packing are the two most common
gotchas when the bits look scrambled after thresholding.

## Flag

`CURTIN_CTF{redacted}`

