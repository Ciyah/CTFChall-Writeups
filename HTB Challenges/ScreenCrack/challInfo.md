---
ctf: HTBLabs
title: ScreenCrack
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# ScreenCrack

## Challenge
New screenshot service just dropped! They talk alot but can they hack it? IP:154.57.164.78:31937

## Approach

1. `validateUrl()` blocks literal private IPv4 addresses but accepts a domain
   without checking the address it resolves to.
2. Send a `gopher://localtest.me:6379/` URL to `/api/get-html`. Since
   `localtest.me` resolves to `127.0.0.1`, cURL reaches the unauthenticated
   internal Redis service.
3. Use a RESP `RPUSH` to add a forged `App\Jobs\rmFile` payload to
   `laravel_database_queues:default`.
4. Inject `';cp /flag /www/public/flag.txt;#` as `FileQueue::$uuid`. The queue
   worker runs as root, and `FileQueue::deleteFile()` interpolates the value
   into `system()` without escaping it.
5. Read `/flag.txt` after the queue worker wakes (it is configured with a
   600-second sleep interval).

## Tools

- `solve.py`

## Lessons

- Validate the resolved IP immediately before connecting, not just the URL's
  hostname.
- Restrict cURL protocols and authenticate/bind internal Redis securely.
- Never interpolate object properties into shell commands; use native file
  APIs such as `unlink()`.

## Flag
HTB{redacted}
