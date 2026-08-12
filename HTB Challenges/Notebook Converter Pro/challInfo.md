---
ctf: HTBLabs
title: Notebook Converter Pro
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Notebook Converter Pro

## Challenge
Welcome to NotebookConverter Pro, a tool for converting Jupyter notebooks into different formats with ease. While it appears simple and efficient, there may be more happening behind the scenes than meets the eye. IP:154.57.164.78:32131

## Approach

1. Register a normal user and upload an HTML-conversion notebook containing a
   Markdown image reference to `/srv/app/data/app.db`.
2. `nbconvert==7.17.0` is vulnerable to CVE-2026-39378. Because the application
   explicitly sets `HTMLExporter.embed_images = True`, the database is returned
   inside the generated HTML as a base64 data URI.
3. Decode the SQLite database and recover the randomized plaintext admin
   password from the `users` table.
4. Log in as admin and enable **Save exported asset files**.
5. Upload a Markdown-conversion notebook whose attachment filename is
   `../../../../app/converter/convert_job.py`. CVE-2026-39377 lets the
   `FilesWriter` follow this traversal and overwrite the converter with a small
   Python payload.
6. Submit one more conversion. The replacement converter executes the SUID
   `/readflag`, saves its output in the job export directory, and reports that
   file as the conversion output. Download it through the normal job endpoint.

## Tools

- `curl`
- `sqlite3`
- `base64`

## Lessons

- Pinning a known-vulnerable conversion library is especially dangerous when
  processing attacker-controlled notebook metadata and Markdown.
- An arbitrary file read can become privilege escalation when secrets such as
  generated admin passwords are stored in a readable SQLite database.
- Exported asset filenames must be normalized and constrained beneath the
  intended output directory.

## Flag

`HTB{redacted}`
