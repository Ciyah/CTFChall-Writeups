---
ctf: HTBLabs
title: DoxPit
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# DoxPit

## Challenge
The owner of famous underground forum doxpit has been allegedly kidnapped, now that turmoil ensues it is the right time to strike and take down this appalling operation. IP:154.57.164.82:30399

## Approach

1. Extract the Server Action ID from the public Next.js page.
2. Abuse CVE-2024-34351 in Next.js 14.1.0 by replacing the `Host` header on a
   Server Action that redirects to `/error`.
3. Use a callback server that returns `text/x-component` to `HEAD` and a 302
   redirect to `GET`, turning the issue into full-read SSRF against Flask on
   `127.0.0.1:3000`.
4. SSRF `/register` to create a user and recover its access token.
5. SSRF `/home?token=...&directory=...` and exploit the second Jinja render of
   `results.scanned_directory`. Use `{% print ... %}`, `attr()`, and an auxiliary
   `u=__globals__` parameter to bypass the blacklist.
6. Execute `cat /flag*` and read its output in the scan report.

## Tools

- `curl`
- Python callback server
- `localhost.run` reverse SSH tunnel

## Lessons

- Next.js 14.1.0 relative Server Action redirects trust the request host.
- The original CVE becomes readable when the callback's `HEAD` response claims
  to be an RSC stream and its `GET` response redirects to the internal target.
- Re-rendering partially substituted templates makes otherwise escaped data an
  SSTI sink.

## Flag

`HTB{redacted}`
