---
ctf: HTBLabs
title: Offlinea
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Offlinea

## Challenge
In a world without internet, information has a new price. One secret. One look. What are you willing to trade? IP: 154.57.164.82:31766

## Approach
1. Send duplicate `url` parameters. PHP validates the last value, while the
   internal Flask application uses the first, allowing SSRF to
   `http://127.0.0.1:5000` with `http://info.cern.ch/` as the valid decoy.
2. Plant `{logify.__globals__[app].config}` in the `/logs` URL. A second visit
   to `/logs` triggers unsafe Python `str.format()` processing and exposes the
   Flask `SECRET_KEY` in the generated PDF.
3. Sign an HS256 JWT containing `is_admin: true` and use SSRF to request the
   internal `/bartender?token=...` endpoint.
4. Extract the secrets JSON, including the flag, from the resulting PDF.

## Tools
- curl
- pypdf

## Lessons
- Duplicate HTTP parameters can produce exploitable parser differences between
  PHP (last value) and Flask/Werkzeug (first value).
- Calling `str.format()` on attacker-controlled data permits object traversal
  and sensitive configuration disclosure.

## Flag
HTB{redacted}
