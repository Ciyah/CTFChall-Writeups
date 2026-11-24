#!/usr/bin/env python3
"""
Bolthole — Curtin CTF 2026 (Mobile / Android RE)

Offline solve: recover PIN from PinEvaluator checksums, then decrypt
the ciphertext in config_telemetry_masks via VaultCipher logic.

Usage:
    python3 solve.py
    # Pass optional path to arrays.xml if jadx output exists:
    python3 solve.py jadx_out/resources/res/values/arrays.xml
"""

import re
import sys
import hashlib
import base64

# ---------------------------------------------------------------------------
# Step 1 — Brute PIN from PinEvaluator checksums
# ---------------------------------------------------------------------------
CHECKSUM = [184, 20, 129, 94, 50, 28]

pin = ''.join(
    next(str(d) for d in range(10)
         if ((((d * 17) + 43) ^ ((i * 29) + 11)) & 255) == CHECKSUM[i])
    for i in range(6)
)
print(f"[*] PIN  : {pin}")

# ---------------------------------------------------------------------------
# Step 2 — Parse config_telemetry_masks from arrays.xml
# ---------------------------------------------------------------------------
# Hardcoded fallback (extracted from Bolthole.apk via jadx)
MASKS_HARDCODED = [
    58, 160, 155, 11, 34, 141, 20, 40, 91, 145,
    36, 129, 224, 209, 153, 1, 65, 174, 8, 115,
    140, 201, 152, 165, 226, 0, 75, 28
]

arrays_xml = sys.argv[1] if len(sys.argv) > 1 else None

if arrays_xml:
    try:
        xml = open(arrays_xml).read()
        blk = re.search(
            r'<array name="config_telemetry_masks">(.*?)</array>', xml, re.S
        ).group(1)
        masks = [int(x) for x in re.findall(r'<item>(\d+)</item>', blk)]
        print(f"[*] Loaded {len(masks)} mask values from {arrays_xml}")
    except Exception as e:
        print(f"[!] Could not parse {arrays_xml}: {e} — using hardcoded masks")
        masks = MASKS_HARDCODED
else:
    print("[*] Using hardcoded mask values (run jadx first for live extraction)")
    masks = MASKS_HARDCODED

# ---------------------------------------------------------------------------
# Step 3 — Decrypt via VaultCipher logic:
#   dec[j] = masks[j] ^ SHA256(pin)[j % 32] ^ ((j*13 + 7) & 0xFF)
# ---------------------------------------------------------------------------
key = hashlib.sha256(pin.encode()).digest()
dec = bytes(
    (m ^ (key[j % 32] & 0xFF) ^ (((j * 13) + 7) & 0xFF)) & 0xFF
    for j, m in enumerate(masks)
)
print(f"[*] Token (Base64): {dec.decode()}")

flag_body = base64.b64decode(dec).decode()
flag = f"CURTIN_CTF{{{flag_body}}}"
print(f"[+] FLAG : {flag}")
