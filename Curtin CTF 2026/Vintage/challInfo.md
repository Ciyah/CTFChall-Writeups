---
ctf: "Curtin CTF 2026"
title: "Vintage"
category: "forensics"
difficulty: ""
tags: ["steganography", "jpeg", "png", "file-carving", "exiftool", "trailing-data"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

Some memories never fade, they just get older and more beautiful

Flag Format is CURTIN_CTF{redacted}

## Approach

1. **Phase 1 — Analyze:** Single file provided: `Vintage-Car.jpeg`. Theme ("memories", "vintage") suggests image forensics / hidden data.

2. **Phase 2 — Recon:** Checked for data appended after the JPEG end-of-image marker (`FF D9`):
   ```bash
   python3 -c "
   d=open('Vintage-Car.jpeg','rb').read()
   i=d.rfind(b'\xff\xd9')
   print('EOI at', i, 'of', len(d), '| trailing bytes:', len(d)-(i+2))
   print(d[i+2:i+2+16])
   "
   ```
   → 18,777 bytes after EOI, starting with `\x89PNG\r\n\x1a\n` — a full PNG file is appended to the JPEG.

3. **Phase 3 — Infiltrate:** Carved the hidden PNG:
   ```bash
   python3 -c "
   d=open('Vintage-Car.jpeg','rb').read()
   i=d.rfind(b'\xff\xd9')+2
   open('hidden.png','wb').write(d[i:])
   "
   file hidden.png      # PNG image data, 1280 x 720
   ```
   The PNG renders the flag string in plain text. Confirmed via exiftool:
   ```bash
   exiftool hidden.png | grep -i 'Text Layer'
   # Text Layer Text : K@7m#Q2v!p9L$xR
   ```

## Tools

- Python 3 (manual carve)
- `file`
- `exiftool`

## Lessons

- Always check for data **after the JPEG `FF D9` EOI** marker — trailing files are a classic two-files-in-one trick. `binwalk`, `foremost`, or a one-line Python carve all work.
- `exiftool` can surface Photoshop **text layer** content, which may hold flags even when rendered text is small or hard to read visually.

## Flag

`CURTIN_CTF{redacted}`
