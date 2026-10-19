---
ctf: "DeadFace CTF"
title: "File Dump 01"
category: "forensics"
difficulty: ""
tags: []
flag_format: "deadface{...}"
date: "2026-10-18"
---

## Challenge

Created By: @RP-01?

We have intercepted a DEADFACE hacker's laptop and determined he had stolen a man named Daniel's entire identity. For this first challenge, let's identify which DEADFACE member is responsible!

Submit the answer as deadface{deadface alias}

## Approach

The supplied ZIP was extracted and its contents were classified with `file`. It
contained a mixture of PNG/JPEG images, PDFs, DOCX files, and XLSX files. Rather
than relying only on the visible document contents, the Office metadata was
examined with ExifTool.

Several files connected to the stolen identity listed the same suspicious
creator:

- `notes.docx`: creator `ghostwriter404`, last modified by `GHOST404-PC`
- `reminders.docx`: creator `ghostwriter404`
- `resume.docx`: creator `ghostwriter404`
- `invoice.xlsx`: creator `ghostwriter404`

The body of `notes.docx` also directly implicates its author in the identity
theft:

> Remember to keep the Hameser accounts consistent across sites.
>
> Use the FL address for anything that mails a code. Reroute the rest.

The important attribution artifact is the workstation name `GHOST404-PC`.
`ghost404` is not the exact DEADFACE handle: the official DEADFACE actor roster
spells the member's alias **`gh0st404`**, with a zero in `gh0st`. Therefore the
workstation evidence maps to DEADFACE operative `gh0st404`.

Official actor roster: <https://ctf.deadface.io/deadface>

### Commands

```bash
unzip -n File_Dump_Challenge.zip

find "File Dump Challenge" -maxdepth 1 -type f -print0 | xargs -0 file

exiftool -FileName -Title -Creator -Description -LastModifiedBy \
  "File Dump Challenge/notes.docx" \
  "File Dump Challenge/reminders.docx" \
  "File Dump Challenge/resume.docx" \
  "File Dump Challenge/invoice.xlsx"

unzip -p "File Dump Challenge/notes.docx" word/document.xml \
  | sed 's/<\/w:p>/\n/g; s/<[^>]*>//g' \
  | sed '/^[[:space:]]*$/d'
```

The decisive output was:

```text
File Name                       : notes.docx
Creator                         : ghostwriter404
Last Modified By                : GHOST404-PC
```

## Tools

- `unzip` — extracted the challenge archive and read the DOCX XML
- `file` — identified the supplied file formats
- `exiftool` — recovered Office creator and workstation metadata
- Official DEADFACE actor roster — confirmed the exact spelling of the alias

## Lessons

- DOCX and XLSX files are ZIP containers whose metadata can survive even when
  the visible content looks ordinary.
- Attribution values must be mapped to the exact canonical handle. In this
  case, `GHOST404-PC` points to `gh0st404`, not `ghost404`.

## Flag

```text
deadface{gh0st404}
```

