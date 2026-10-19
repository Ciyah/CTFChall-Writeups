---
ctf: "DeadFace CTF"
title: "Headshot"
category: "forensics"
difficulty: ""
tags: []
flag_format: "deadface{...}"
date: "2026-10-18"
---

## Challenge

Created By: @syyntax

DEADFACE was able to compromise a fileshare that consisted of corporate headshots for Aurora Health employees. We believe they're tagging the photos with information that communicates to their group which employees to target in their future campaigns. Figure out which image DEADFACE tampered with - it will give us a heads up on who they plan to target. Submit the answer as deadface{flag_text}.

## Approach

The supplied archive was inspected first to identify its contents:

```bash
unzip -l headshot.zip
```

It contained three headshots and an original copy of the third image:

```text
headshot001.png
headshot002.png
headshot003.png
headshot003.png_original
```

The presence of both `headshot003.png` and `headshot003.png_original`
identified the third headshot as the likely tampered image. The files were
extracted and their types and metadata examined:

```bash
unzip headshot.zip -d extracted
file extracted/*
exiftool extracted/*
```

All four files were valid 512x512 indexed-color PNG images. However,
`exiftool` reported an extra field in the modified third image that was not
present in its original counterpart:

```text
Comment : deadface{b00m_h34Dsh0TTT}
```

The result was independently verified by searching the raw printable strings:

```bash
strings -a extracted/headshot003.png | grep -i deadface
```

This returned:

```text
deadface{b00m_h34Dsh0TTT}
```

The nearby raw string `tEXtComment` shows that the flag was stored in a PNG
`tEXt` metadata chunk under the `Comment` keyword. It was therefore a metadata
steganography challenge rather than a pixel-level encoding.

## Tools

- `unzip` / `zipinfo` — listed and extracted the archive
- `file` — identified the image formats and properties
- `exiftool` — displayed the embedded PNG metadata
- `strings` — independently confirmed the plaintext flag in the file

## Lessons

- Inspect archive filenames before beginning more expensive steganography
  analysis; an included original can immediately identify the altered file.
- Always examine image metadata and PNG chunks before testing pixel-level LSB
  techniques.
- Validate a recovered value with a second method when possible. Here,
  `exiftool` and `strings` produced the same flag.

## Flag

```text
deadface{b00m_h34Dsh0TTT}
```

