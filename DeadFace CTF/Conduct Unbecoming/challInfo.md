---
ctf: "DeadFace CTF"
title: "Conduct Unbecoming"
category: "forensics"
difficulty: ""
tags: []
flag_format: "deadface{...}"
date: "2026-10-17"
---

## Challenge

Created By: @G2Gh0st

DEADFACE recently breached Night Veil University and exfiltrated a number of internal documents. We were able to recover one of those documents for analysis. We need your help to identify the asset-id that was used to create the document so we can have our investigators analysis it for more clues on how DEADFACE gained access.

Submit the flag as deadface{flag-text}.

Download Image SHA256: 6e7809f4a7893b0a8348195d0009181376ef635d465a2ee4279e78115e44f1ba

## Approach

I started by verifying the supplied image and inspecting its metadata:

```bash
sha256sum "Conduct Unbecoming.jpg"
file "Conduct Unbecoming.jpg"
exiftool -a -u -g1 "Conduct Unbecoming.jpg"
identify -verbose "Conduct Unbecoming.jpg"
```

The SHA-256 hash matched the value in the challenge description. The image was a
normal JPEG with no appended archive or obvious flag in its EXIF/XMP metadata.
One anomaly was that the JPEG measured `2566x3314`, while its EXIF metadata
reported `2550x3300`. This suggested examining details that were not readily
visible in the rendered document.

The page looked monochrome, but its RGB channels were not identical. I separated
the channels and subtracted them from one another with ImageMagick:

```bash
magick "Conduct Unbecoming.jpg" -channel R -separate -auto-level /tmp/cu-r.png
magick "Conduct Unbecoming.jpg" -channel G -separate -auto-level /tmp/cu-g.png
magick "Conduct Unbecoming.jpg" -channel B -separate -auto-level /tmp/cu-b.png

magick "Conduct Unbecoming.jpg" -fx '(r-g+1)/2' -auto-level /tmp/cu-rg.png
magick "Conduct Unbecoming.jpg" -fx '(g-b+1)/2' -auto-level /tmp/cu-gb.png
magick "Conduct Unbecoming.jpg" -fx '(r-b+1)/2' -auto-level /tmp/cu-rb.png
```

The `G-B` and `R-B` difference images exposed a faint yellow dot matrix in the
bottom-right corner. The dots were spaced 12 pixels apart in an eight-column
grid. After treating a present dot as `1` and an absent dot as `0`, the first
row was `11111111`, which served as a marker. The remaining rows decoded as
8-bit ASCII:

```text
01001110  N
01010110  V
01010101  U
00101101  -
01010000  P
01010010  R
01001001  I
01001110  N
01010100  T
00101101  -
00110001  1
00110111  7
```

This produced the asset ID `NVU-PRINT-17`.

## Tools

- `sha256sum`
- `file`
- `exiftool`
- ImageMagick (`identify`, `magick`)

## Lessons

- A document that appears black and white can still conceal information in
  small differences between its RGB channels.
- Channel subtraction and contrast normalization can reveal yellow printer
  tracking dots that are nearly invisible against a white page.
- Metadata dimensions that disagree with the decoded image dimensions are a
  useful signal that the file deserves closer visual and structural analysis.

## Flag

```text
deadface{NVU-PRINT-17}
```
