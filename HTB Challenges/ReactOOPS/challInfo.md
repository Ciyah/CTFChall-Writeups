---
ctf: HTBLabs
title: ReactOOPS
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# ReactOOPS

## Challenge
NexusAI's polished assistant interface promises adaptive learning and seamless interaction. But beneath its reactive front end, subtle glitches hint that user input may be shaping the system in unexpected ways. Explore the platform, trace the echoes in its reactive layer, and uncover the hidden flaw buried behind the UI. IP: 154.57.164.67:32233

## Approach

The application uses the Next.js App Router and pins Next.js 16.0.6 with
React 19. This is vulnerable to React2Shell (CVE-2025-55182), an
unauthenticated RCE in React Server Components/Flight deserialization.

Send a multipart POST request with a `Next-Action` header. The crafted Flight
object uses a self-reference (`$@0`) to recover `Chunk.prototype.then`, forges
the chunk's `_response`, resolves `_formData.get` to the JavaScript `Function`
constructor, and triggers it via the `$B` blob handler. Command output is
thrown as a `NEXT_REDIRECT` error digest, which is returned in the HTTP body.

Run:

```sh
python3 solve.py
```

## Tools

- Python standard library (`urllib`, `json`, and `re`)
- `solve.py`, the reusable exploit script

## Lessons

- A purely static-looking App Router page still exposes the vulnerable React
  Server Components request path.
- Dependency versions and package metadata can identify the intended bug even
  when the application source contains no custom server actions.
- Unsafe Flight path traversal can expose inherited methods and ultimately the
  `Function` constructor during deserialization.

## Flag

`HTB{redacted}`
