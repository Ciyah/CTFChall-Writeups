---
ctf: "Curtin CTF 2026"
title: "Fl4shdump"
category: "rev"
difficulty: ""
tags: []
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

We desoldered the 512 KiB SPI flash from a CURTIN-RTR router seized during an incident and dumped it. The factory provisioned a per-device admin token onto it. Recover it.

## Approach

### Phase 1 — Analyze

1. Received `flashdump.bin`, a 524,288-byte (512 KiB) SPI flash dump from a CURTIN-RTR router.
2. Scanned for magic bytes to identify regions:
   - `0x50000`: Gzip magic bytes `1f 8b 08` — a compressed payload.
   - `0x70000`: `FLSH` header — the NVRAM configuration block.
3. Decompressed the gzip stream at `0x50000`, which yielded a `newc` CPIO archive (root filesystem).
4. Extracted the CPIO archive and located two key files:
   - `etc/init.d/rcS` — startup script that calls `/usr/sbin/provision` if `/tmp/admin_token` is absent.
   - `usr/sbin/provision` — the provisioning script.
   - `etc/board.conf` — contains `board_id=CURTIN-RTR-AC1200-r2`.
   - `etc/provision.enc` — 48-byte AES-CBC ciphertext.
5. Parsed the NVRAM block at `0x70000` (NUL-separated key=value pairs) and extracted `hw_serial=CRT-K7Q2-M9XV-4HZ8-WD3N`.

### Phase 2 — Recon

6. Read `usr/sbin/provision` to understand the decryption scheme:
   - **AES key**: first 16 bytes (32 hex chars) of SHA-256 over the hardware serial (no trailing newline).
   - **IV**: full 16-byte (32 hex chars) MD5 digest of the board ID (no trailing newline).
   - **Ciphertext**: the 48 bytes in `etc/provision.enc`.
   - Algorithm: AES-128-CBC, decrypted plaintext written to `/tmp/admin_token`.

### Phase 3 — Infiltrate

7. Reproduced the decryption offline using the two inputs extracted in Phase 1:

```bash
serial='CRT-K7Q2-M9XV-4HZ8-WD3N'
board_id='CURTIN-RTR-AC1200-r2'

key=$(printf '%s' "$serial" | sha256sum | cut -c1-32)
iv=$(printf '%s' "$board_id" | md5sum | cut -c1-32)

openssl enc -d -aes-128-cbc -K "$key" -iv "$iv" -in etc/provision.enc
```

8. Output: `CURTIN_CTF{redacted}`

## Tools

- `binwalk` / manual hex scan — locate gzip and NVRAM regions in the flash dump
- `dd` + `zcat` — extract and decompress the gzip payload
- `cpio` — unpack the newc CPIO root filesystem archive
- `strings` / hex editor — parse NVRAM NUL-separated key=value entries
- `sha256sum`, `md5sum` — derive AES key and IV
- `openssl enc` — perform AES-128-CBC decryption

## Lessons

- SPI flash dumps commonly pack multiple regions at fixed offsets: a compressed rootfs (gzip/LZMA) and an NVRAM block. Scanning for magic bytes (`1f 8b` for gzip, `FLSH`/`TRX`/`CFE` for headers) is the fastest way to locate them.
- Provisioning scripts that derive crypto keys from device-unique identifiers (serial numbers, board IDs) stored on the same flash are trivially broken once the dump is obtained — all key material is present in one image.
- Use `printf '%s'` (not `echo`) when hashing strings in shell scripts to avoid an unintended trailing newline changing the hash.

## Flag

`CURTIN_CTF{redacted}`

