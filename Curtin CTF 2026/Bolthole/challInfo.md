---
ctf: "Curtin CTF 2026"
title: "Bolthole"
category: "Mobile / Android RE"
difficulty: ""
tags: ["android", "apk", "reverse-engineering", "jadx", "xor", "sha256"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
solved: true
---

## Challenge

One secret mobile application.

Flag Format: `CURTIN_CTF{redacted}`

---

## Approach

### Phase 1 — Analyze

1. **Unzip the APK** to inspect structure:
   ```bash
   unzip Archive61/Bolthole.apk -d apk_out
   ```
   Gives: `AndroidManifest.xml`, `classes.dex` … `classes4.dex`, `res/`, `resources.arsc`.

2. **String triage** on the dex files to identify custom logic:
   ```bash
   strings -a apk_out/classes*.dex | grep -aiE 'bolthole|flag|cipher|xor|base64|pin'
   ```
   Hits: package `com.bolthole.vault`, classes `FlagEntry`, `PinEvaluator`, `VaultCipher`, references to `checkFlag`, `getCipher`, `xor`, `decodeMap`, `Base64`.

3. **Decompile with jadx**:
   ```bash
   jadx Archive61/Bolthole.apk -d jadx_out
   find jadx_out -path '*com/bolthole*' -name '*.java'
   ```
   Three classes of interest:
   - `MainActivity.java` — UI; on correct PIN calls `VaultCipher.releasePayload()` but **never** renders the secret on screen — only writes it to Logcat.
   - `PinEvaluator.java` — per-digit checksum validation.
   - `VaultCipher.java` — SHA-256 key derivation + XOR decryption, reads ciphertext from `res/values/arrays.xml` under the name `config_telemetry_masks`.

### Phase 2 — Recon / Vulnerability

**PinEvaluator logic** (each digit is independent, 10 possibilities each):
```java
private static final int[] CHECKSUM = {184, 20, 129, 94, 50, 28};
// transform = (((d*17)+43) ^ ((i*29)+11)) & 255
// must equal CHECKSUM[i]
```

**VaultCipher logic**:
```java
byte[] key = SHA256(pin.getBytes(UTF_8));
dec[j] = (byte)((maskArray[j] ^ key[j % 32]) ^ ((j*13+7) & 255));
// result is Base64 → decode for the flag body
```

The ciphertext (`config_telemetry_masks`) is a 28-item integer array in `res/values/arrays.xml`, disguised as telemetry config.

### Phase 3 — Exploit

**Brute PIN** (10^6 search space collapses to 10×6 = 60 checks):
```python
CHECKSUM = [184, 20, 129, 94, 50, 28]
pin = ''.join(
    next(str(d) for d in range(10)
         if ((((d*17)+43) ^ ((i*29)+11)) & 255) == CHECKSUM[i])
    for i in range(6)
)
# pin == "819125"
```

**Decrypt**:
```python
import hashlib, base64
masks = [58,160,199,55,50,194,189,184,211,157,143,198,83,161,56,150,65,42,53,115,209,212,169,199,118,211,102,32]
key = hashlib.sha256(pin.encode()).digest()
dec = bytes((m ^ key[j%32] ^ (((j*13)+7)&255)) & 255 for j, m in enumerate(masks))
# dec == b"SDFkRGVuX3VuRGVSX2IzbkU0dGgk"
print(base64.b64decode(dec).decode())   # H1dDen_unDeR_b3nE4th$
```

Run the full offline solver:
```bash
python3 solve.py
# optionally: python3 solve.py jadx_out/resources/res/values/arrays.xml
```

Output:
```
[*] PIN  : 819125
[*] Token (Base64): SDFkRGVuX3VuRGVSX2IzbkU0dGgk
[+] FLAG : CURTIN_CTF{redacted}
```

(On a real device: enter `819125` → `adb logcat -s VaultSync` → Base64-decode the token.)

---

## Tools

- `jadx` — APK decompilation to readable Java
- `strings` — fast initial triage of dex bytecode
- `unzip` — APK structure inspection
- Python 3 (`hashlib`, `base64`, `re`) — offline PIN brute + decryption

---

## Lessons

- **Client-side secrets don't stay secret.** PIN checksum, XOR key derivation, and the ciphertext all ship inside the APK — anything the app can compute, a decompiler can replay.
- **"Logcat-only" output is not protection.** The payload is fully reconstructable without ever running the app.
- **Obfuscation as config.** Naming the ciphertext array `config_telemetry_masks` and the log tag `VaultSync` is misdirection; `jadx` + a 15-line script undoes it instantly.
- Fix: real server-side validation; never derive or hold the secret on the device.

---

## Flag

```
CURTIN_CTF{redacted}
```

