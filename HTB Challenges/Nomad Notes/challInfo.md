---
ctf: HTBLabs
title: Nomad Notes
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-13
---

# Nomad Notes

## Challenge
A digital-to-physical postcard service helping you bridge the gap between pixels and paper. From the neon lights of Tokyo to the romantic canals of Venice, some secrets are harder to seal than an envelope. Can you find the message hidden between the lines? IP:154.57.164.77:31781

## Approach

1. `/postcard` HTML-escapes `secret`, but passes it directly as the replacement
   argument to JavaScript's `String.replace`. The replacement token `$\`` expands
   to the template prefix, including the quote before `{{ secret }}`, which breaks
   out of the nonced inline script and yields CSP-authorized JavaScript execution.
2. Have the public `/report` bot visit that crafted postcard.
3. From the bot's localhost origin, `fetch('/report')` with an
   `X-Carta-Auth-Key` header reaches the protected branch. The header value is HTML
   injected into `/destinations?name=...`; construct its `<`/`>` characters at
   runtime so postcard escaping cannot corrupt it.
4. Inject a meta referrer policy of `unsafe-url` and a meta refresh to an external
   collector. The resulting `Referer` discloses the entire protected destinations
   URL, including its `flag` query parameter.

## Tools

- Python 3 (`solve.py`)
- Chromium and curl for validation

## Lessons

- User data used as a `String.replace` replacement needs a callback replacer or
  escaped `$` replacement sequences, even if it was already HTML-escaped.
- Secrets in URLs can leak through referrers; use a restrictive referrer policy and
  do not put sensitive values in query strings.

## Flag
HTB{redacted}
