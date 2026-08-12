---
ctf: HTBLabs
title: Bobby's Bistro
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Bobby's Bistro

## Challenge
Bobby and I had recently created a nice little webapp to hang out and chat with our buddies, but that devil ran off to some vacation for new year. He did leave a bot behind to keep an eye out though. Hope nothing happens IP:154.57.164.82:31093

## Approach

1. Register and log in as a normal user.
2. Exploit SQL injection in `POST /profile` via the interpolated `token` value:
   `' OR role='admin'--`
   This discloses the randomized admin username and UUID.
3. Generate an RSA key pair and upload an attacker-controlled JWKS using the
   attachment filename `../static/.well-known/jwks.json`. The upload directory
   is `/app/uploads`, so the traversal overwrites the JWKS used by JWT validation.
4. Sign an RS256 JWT containing the leaked admin UUID and access the admin
   announcement endpoint.
5. Exploit the Chameleon `PageTemplate` sink in announcement creation. Since the
   filter removes dots and quotes, construct `/flag.txt` with `chr()` calls and
   read its first line with `list(open(...))[0]`.
6. Fetch `/announcements`, where the rendered flag is included in the generated
   announcement.

## Tools

- Python `requests`, `PyJWT`, and `cryptography`
- `solve.py`

## Lessons

- Never interpolate input into SQL, even for authenticated-only features.
- Uploaded filenames must be normalized and confined to their intended folder.
- A writable JWT trust store turns file upload traversal into authentication bypass.
- Character blacklists do not make server-side template evaluation safe.

## Flag

`HTB{redacted}`
