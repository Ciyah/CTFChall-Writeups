#!/usr/bin/env python3
"""
Vintage — Curtin CTF 2026
Carves the hidden PNG appended after the JPEG EOI (FF D9) marker.
"""
import sys

jpeg = "Archive11/Vintage-Car.jpeg"
out  = "hidden.png"

data = open(jpeg, "rb").read()
eoi  = data.rfind(b"\xff\xd9")

print(f"JPEG EOI at byte {eoi} of {len(data)}")
trailing = len(data) - (eoi + 2)
print(f"Trailing bytes: {trailing}")

if trailing < 8:
    print("No significant trailing data found.")
    sys.exit(1)

payload = data[eoi + 2:]
print(f"Magic bytes: {payload[:8]}")

if payload[:4] == b"\x89PNG":
    print("Hidden PNG detected — carving...")
    open(out, "wb").write(payload)
    print(f"Saved to {out}")
else:
    print("Trailing data does not look like a PNG.")
    sys.exit(1)
