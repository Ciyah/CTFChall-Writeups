#!/usr/bin/env python3
"""
Silent Frequencies — Curtin CTF 2026
Category: IoT · Points: 190

The file Chall.fc32 is a GNU Radio / SDR recording of a 2-FSK signal stored
as little-endian complex float32 (IQ) samples.

Signal structure
----------------
- 10 bursts, each 25,600 samples long
- 100,000 silence samples between bursts  (25,600 + 100,000 = 125,600 / frame)
- Each burst carries 256 symbols of 100 samples each
- Two tones: phase change ≈ −0.05 cycles/sample (bit=1) or +0.05 (bit=0)

Decoding
--------
1. Slice each frame at 125,600-sample boundaries and take the first 25,600.
2. Compute instantaneous phase change: angle(s[n+1] * conj(s[n])).
3. Sample mid-symbol (index 49 of each 100-sample symbol) to avoid transitions.
4. Threshold at 0: negative → bit 1, non-negative → bit 0.
5. Pack 256 bits MSB-first → 32 bytes.
6. Byte 0 is the preamble (0xAA = 10101010). Bytes 1–31 are ASCII flag.
"""

import sys
from pathlib import Path
import numpy as np

BURST_LEN    = 25_600
FRAME_LEN    = 125_600   # burst + silence
SYMBOL_LEN   = 100
SAMPLE_MID   = 49        # mid-symbol sample offset for phase measurement


def decode_burst(burst: np.ndarray) -> bytes:
    phase_change = np.angle(burst[1:] * burst[:-1].conj())
    bits = (phase_change[SAMPLE_MID::SYMBOL_LEN] < 0).astype(np.uint8)
    return np.packbits(bits, bitorder="big").tobytes()


def main() -> None:
    fc32_path = Path("Chall.fc32")
    if not fc32_path.exists():
        sys.exit("Chall.fc32 not found — run from the challenge directory.")

    samples = np.fromfile(fc32_path, dtype="<c8")
    frames: list[bytes] = []

    for start in range(0, len(samples), FRAME_LEN):
        burst = samples[start : start + BURST_LEN]
        if len(burst) < BURST_LEN:
            break
        frames.append(decode_burst(burst))

    if not frames:
        sys.exit("No bursts found.")

    unique = set(frames)
    if len(unique) != 1:
        print(f"[!] Warning: {len(unique)} distinct frames (expected 1)", file=sys.stderr)

    frame = frames[0]
    preamble, payload = frame[0], frame[1:]

    print(f"Bursts decoded : {len(frames)}")
    print(f"Preamble byte  : 0x{preamble:02X}  (expected 0xAA)")

    try:
        flag = payload.decode("ascii")
        print(f"Flag           : {flag}")
    except UnicodeDecodeError:
        print(f"Raw payload    : {payload!r}")


if __name__ == "__main__":
    main()
