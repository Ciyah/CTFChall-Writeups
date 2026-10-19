---
ctf: "DeadFace CTF"
title: "Keep Digging "
category: "forensics"
difficulty: ""
tags: []
flag_format: "deadaface{...}"
date: "2026-10-18"
---

## Challenge

 Created By: @syyntax

DEADFACE left this calling card on a victim's machine. We suspect there is hidden information in this image, but none of our common steganography tools seem to work. There must be some way to determine where the flag is hidden.

Submit the flag as deadface{flag-text}.

## Approach

1. `file`, `exiftool`, `strings`, and `binwalk` showed a 448x670 progressive
   JPEG with no useful metadata or appended file.
2. ImageMagick decoded the picture, but reported thousands of "extraneous
   bytes" before each progressive scan marker. The image also ended abruptly
   at the bottom. This indicated that the JPEG's declared height had been
   reduced while the compressed scan data for the missing rows was left in the
   file.
3. The SOF2 marker starts at offset `0xab`. Its height field is at offsets
   `0xb0:0xb2` and contains `0x029e` (670). Replacing it with `0x02f0` (752),
   the full 94 eight-pixel MCU rows, restores the concealed area:

   ```bash
   python3 - <<'PY'
   from pathlib import Path
   data = bytearray(Path('keep_digging.jpg').read_bytes())
   data[0xb0:0xb2] = (752).to_bytes(2, 'big')
   Path('keep_digging_restored.jpg').write_bytes(data)
   PY
   ```

4. Opening `keep_digging_restored.jpg` reveals an extra dark strip below the
   original image containing the flag.

## Tools

- `file`
- `exiftool`
- `binwalk`
- ImageMagick (`identify`/`convert`)
- `xxd`
- Python 3

## Lessons

JPEG dimensions live in the Start of Frame marker and are trusted by decoders.
Changing only the declared height can conceal complete encoded MCU rows without
using a conventional steganography container, so standard extraction tools find
nothing. Decoder warnings about data beyond the expected scan boundary are a
strong clue for this technique.

## Flag

`deadface{D1g_d0wN_D33p!}`

