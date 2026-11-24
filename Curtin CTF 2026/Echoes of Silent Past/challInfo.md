---
ctf: "Curtin CTF 2026"
title: "Echoes of Silent Past"
category: "iot"
difficulty: ""
tags: ["esp32", "firmware", "flash-dump", "base32", "xor", "xtensa"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

> Every Silent Pulse carries a story waiting to be uncovered

Flag Format: `CURTIN_CTF{redacted}`

Provided file: `Archive45.zip` → `Archive45/vault_dump.bin`

---

## Approach

### Phase 1 — Analyze (files only)

**1. Identify the firmware image**

```
$ file Archive45/vault_dump.bin
Archive45/vault_dump.bin: data

$ wc -c Archive45/vault_dump.bin
4194304  (4 MiB — matches a standard ESP32 flash)
```

Bytes `0x00000000`–`0x00007FFF` are all `0xFF` (erased flash). The ESP32
partition table lives at `0x8000`:

```
$ xxd -s 0x8000 -l 192 Archive45/vault_dump.bin
00008000: aa50 0102 0090 0000 0050 0000 6e76 7300  .P.......P..nvs.
00008020: aa50 0100 00e0 0000 0020 0000 6f74 6164  .P....... ..otad
00008040: aa50 0010 0000 0100 0000 1400 6170 7030  .P..........app0
00008060: aa50 0011 0000 1500 0000 1400 6170 7031  .P..........app1
00008080: aa50 0182 0000 2900 0000 1600 7370 6966  .P....).....spif
000080a0: aa50 0103 0000 3f00 0000 0100 636f 7265  .P....?.....core
```

Partitions: `nvs` (0x9000), `otadata` (0xe000), **`app0` at 0x10000**,
`app1` (0x150000), `spiffs` (0x290000), `coredump` (0x3f0000).

**2. Locate pivot strings**

```
$ strings -a -t x Archive45/vault_dump.bin | grep -Ei 'vault|checksum|flag|sealed'
  10125 === ESP32 VAULT v2.0 ===
  10193 [+] Vault checksum: 0x%08X
  101af [+] Flag is sealed in the vault. You can't read it from here...
  10202 [!] Too many attempts. Vault re-keyed. Locked for 5s.
```

All four strings are inside the `app0` region (file offset `0x10000`+).
`Vault checksum: 0x%08X` at `0x10193` and `Flag is sealed in the vault` at
`0x101af` are the entry points for reverse-engineering the assembly routine.

**3. Identify the descriptor table and key**

The Xtensa disassembly of the routine following the checksum format-string
reference reads five 8-byte descriptors from a table at `0x18C9C`:

```
$ xxd -s 0x18C9C -l 48 Archive45/vault_dump.bin
00018c9c: e58c 403f 0818 0300  ← descriptor 0: va=0x3F408CE5 len=8 dst=24 mode=3
00018ca4: dd8c 403f 0800 0000  ← descriptor 1: va=0x3F408CDD len=8 dst=0  mode=0
00018cac: d88c 403f 0520 0400  ← descriptor 2: va=0x3F408CD8 len=5 dst=32 mode=4
00018cb4: d08c 403f 0808 0100  ← descriptor 3: va=0x3F408CD0 len=8 dst=8  mode=1
00018cbc: c88c 403f 0810 0200  ← descriptor 4: va=0x3F408CC8 len=8 dst=16 mode=2
```

Immediately after the descriptor table, the routine loads a 4-byte key:

```
$ xxd -s 0x18CC4 -l 8 Archive45/vault_dump.bin
00018cc4: 5a13 c72e 4c53 4b4e    →  key = 5A 13 C7 2E
```

---

### Phase 2 — Recon and analysis

**Virtual-address to file-offset mapping**

Each descriptor's `virtual_address` is a DROM address. The app binary is
loaded at flash offset `0x10000` and mapped to `0x3F400000`:

    file_offset = virtual_address − 0x3F3F0000

Verification with descriptor 1 (mode 0, dst 0): VA `0x3F408CDD`
→ file `0x18CDD`. `xxd -s 0x18CDD -l 8` returns live bytes, confirming the
mapping.

**Descriptor layout (struct, 8 bytes each)**

| Field | Type | Description |
|---|---|---|
| `virtual_address` | u32 LE | DROM address of this fragment |
| `length` | u8 | byte count of this fragment |
| `destination` | u8 | byte offset in the 37-byte output buffer |
| `mode` | u8 | decoding mode (0–4) |
| `_pad` | u8 | unused |

**Decoding modes (i = 0-based index within fragment)**

| Mode | Operation |
|---|---|
| 0 | XOR with repeating key `5A 13 C7 2E` |
| 1 | subtract `17 × (i+1)` mod 256 |
| 2 | XOR with `(7×i + 3) & 0xFF` |
| 3 | rotate right 3 bits, then XOR `0x6B` |
| 4 | reverse fragment first, then XOR each byte with `0x42` |

Destination offsets place fragments in this order: 0, 8, 16, 24, 32
(5 × 8-byte slots, last slot only 5 bytes → 37 bytes total).

The descriptors appear in the binary in destination order 24, 0, 32, 8, 16
(i.e. out of order), so sorting by `destination` before assembly is required.

---

### Phase 3 — Infiltrate

**Run the solver**

```
$ python3 solve.py

[*] XOR key: 5a13c72e
[*] Descriptor @ 0x18C9C: va=0x3F408CE5 off=0x18CE5 len=8 dst=24 mode=3
[*] Descriptor @ 0x18CA4: va=0x3F408CDD off=0x18CDD len=8 dst=0  mode=0
[*] Descriptor @ 0x18CAC: va=0x3F408CD8 off=0x18CD8 len=5 dst=32 mode=4
[*] Descriptor @ 0x18CB4: va=0x3F408CD0 off=0x18CD0 len=8 dst=8  mode=1
[*] Descriptor @ 0x18CBC: va=0x3F408CC8 off=0x18CC8 len=8 dst=16 mode=2
[*] Assembled buffer (37 bytes): b'GMSFALJTGJPTCNK7OYZVE6K7OAYHOM2SMZKWY'

[+] Flag: CURTIN_CTF{redacted}
```

**What the solver does**

1. Reads all five 8-byte descriptors from `0x18C9C–0x18CC3`.
2. Reads the 4-byte XOR key from `0x18CC4`.
3. For each descriptor, extracts the fragment from the computed file offset,
   applies the decoding for that mode, and writes it into the 37-byte buffer
   at `destination`.
4. The raw buffer is a Base32 string `GMSFALJTGJPTCNK7OYZVE6K7OAYHOM2SMZKWY`.
5. Pads to a multiple of 8 with `=` and Base32-decodes to get the flag body.

---

## Tools

- `file`, `xxd`, `strings` — initial triage
- `objdump -m xtensa` / Ghidra with Xtensa support — disassembly of `app0`
- `python3 solve.py` — offline extractor (no live target needed)

## Lessons

An ESP32 flash dump is a composite image: erased flash (`0xFF`), partition
table at `0x8000`, and one or more app images. The virtual-address-to-file
formula `file_offset = VA − 0x3F3F0000` holds for DROM-mapped regions.

A checksum format string is a reliable disassembly entry point: the routine
that prints it always touches the data being checksummed, which is exactly
where hidden buffers are assembled. Following that one reference led directly
to the descriptor table, the key, and the entire decode logic — no fuzzing
or dynamic execution required.

Multi-mode per-fragment encoding (XOR, subtract, rotate, reverse) looks
complex but is entirely static; each mode is independently invertible. The
only real work is reading the descriptor layout correctly.

## Flag

```
CURTIN_CTF{redacted}
```
