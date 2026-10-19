---
ctf: "DeadFace CTF"
title: "Exfiltration"
category: "forensics"
difficulty: ""
tags: []
flag_format: "deadface{...}"
date: "2026-10-18"
---

## Challenge

Created By: @G2Gh0st

DEADFACE frequently uses unconventional methods to exchange information and avoid detection. Analysts recovered a set of images from a compromised communications channel that appear unrelated at first glance. We suspect the collection contains a hidden message intended for other members of the group. Recover the message and identify what DEADFACE is trying to say.

Submit the answer as deadface{flagtext}.

## Approach

1. Extract the archive and inspect all JPEG metadata with `exiftool`.
2. Each image has a suspicious `ImageUniqueID` beginning with `IMG_`; the suffix is valid hexadecimal. The images' `DateTimeOriginal` values also form a unique chronological ordering.
3. Sort the records by `DateTimeOriginal`, concatenate the hexadecimal suffixes, and decode the resulting hex stream as bytes:

   ```bash
   mkdir -p extracted
   unzip -o exfiltration.zip -d extracted
   exiftool -json -DateTimeOriginal -ImageUniqueID extracted/*.jpg \
     | jq -r 'sort_by(.DateTimeOriginal) | map(.ImageUniqueID | sub("^IMG_"; "")) | join("")' \
     | xxd -r -p
   ```

4. This prints `deadface{timing-is-everything}`.

## Tools

- `unzip`
- `exiftool`
- `jq`
- `xxd`

## Lessons

When a steganography challenge provides a collection of otherwise unrelated images, compare metadata across the entire set. Here, the timestamps supplied the ordering key while another EXIF field supplied hex-encoded payload fragments.

## Flag

`deadface{timing-is-everything}`

