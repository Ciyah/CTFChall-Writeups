---
ctf: HTBLabs
title: JinjaCare
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# JinjaCare

## Challenge
Jinjacare is a web app for managing COVID-19 vaccination records, allowing users to view history and generate digital certificates. You're invited to identify security vulnerabilities in the system and retrieve the hidden flag from the application IP:154.57.164.74:31526 .

## Approach

1. Registered a normal user account and signed in.
2. Updated the full-name field at `POST /profile/personal` with `{{7*7}}`.
3. Downloaded `/generate_certificate` and extracted its text. The name appeared as
   `49`, confirming stored Jinja server-side template injection in the certificate
   renderer.
4. Changed the name to the following Jinja payload:

   ```jinja2
   {{cycler.__init__.__globals__.os.popen('cat /flag*').read()}}
   ```

5. Generated the certificate again; the command output was embedded as its name.

## Tools

- `curl` for account creation, login, profile updates, and PDF download
- `mutool draw -F txt` for PDF text extraction

## Lessons

- Escaping user data in the first HTML render is insufficient if that data is later
  interpolated into a template source string and rendered a second time.
- Use a fixed certificate template and pass profile data only as template variables;
  never concatenate stored user input into Jinja template source.

## Flag

`HTB{redacted}`
