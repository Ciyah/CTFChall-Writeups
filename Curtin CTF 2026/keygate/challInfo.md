---
ctf: "Curtin CTF 2026"
title: "keygate"
category: "rev"
difficulty: ""
tags: []
flag_format: "CTF{...}"
date: "2026-11-21"
---

## Challenge

KeyGate Pro wants a serial before it will let you in, and the vendor went out of business. Generate a valid serial.

## Approach

### Phase 1 — Analyze

1. `file keygate.exe` confirmed a 64-bit PE console binary (stripped to external PDB).
2. `strings keygate.exe` surfaced three key strings at file offsets:
   - `0x7416` → `Serial: `
   - `0x7422` → `Invalid serial.`
   - `0x7432` → `Serial accepted!`
3. `objdump -h keygate.exe` showed the `.rdata` section starts at file offset `0x7400`
   (VA `0x140009000`), confirming the strings live in read-only data.

### Phase 2 — Recon

4. Traced references to `Serial accepted!` (VA `0x140009032`) back through the `.text`
   section to the validation routine.
5. The validation logic:
   - Checks input is exactly **31 bytes** (`0x1f`).
   - Iterates the input bytes in **reverse** order.
   - For each byte, applies `rol al, 3` (rotate-left by 3 bits).
   - Compares the result against successive bytes from a 31-byte table in `.rdata`.
6. The comparison table starts at VA `0x140009050` → file offset `0x7450`.
   Extracted bytes (hex):
   ```
   eb 99 a3 a1 a3 81 93 fa 73 99 43 a3 fa 99 9b 93
   99 b3 99 93 db 32 a2 1a fa 72 4a a2 92 aa 1a
   ```

### Phase 3 — Infiltrate

7. To invert `rol al, 3`, apply `ror al, 3` (i.e., `(byte >> 3) | ((byte & 7) << 5)`)
   to each table byte, then reverse the result to restore input order.
8. Recovery script:

   ```python
   from pathlib import Path

   data = Path("keygate.exe").read_bytes()
   table = data[0x7450:0x7450 + 31]

   serial = bytes((byte >> 3) | ((byte & 7) << 5) for byte in table)[::-1]

   # Replay the executable's validation loop to verify.
   assert bytes(((byte << 3) | (byte >> 5)) & 0xff
                for byte in reversed(serial)) == table

   print(serial.decode("ascii"))
   ```

9. Output: `CURTIN_CTF{redacted}` (31 bytes, assertion passes).

## Tools

- `file`, `strings` — initial static triage
- `objdump -h` — section layout / file-offset mapping
- Python 3 — table extraction and ROR3 inversion

## Lessons

- `rol al, 3` with a fixed byte table is a trivial keygen: invert the rotation
  (`ror al, 3`) over each table entry and reverse the byte order to recover the
  plaintext serial directly — no brute-force required.
- The `.rdata` section's file-offset formula (`VA − section_VA + section_file_off`)
  is the fastest way to locate embedded constants without a full disassembler.

## Flag

`CURTIN_CTF{redacted}`

