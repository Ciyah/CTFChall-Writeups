---
ctf: HTBLabs
title: OpenSecret
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# OpenSecret

## Challenge
A simple help desk portal where users can submit support tickets. The application uses JWT tokens for session management, but something seems off about how they're implemented. Can you find the security flaw? IP: 154.57.164.82:31829

## Approach

1. Requested the application root page.
2. Inspected the inline JavaScript responsible for generating the JWT session cookie.
3. Found that the HS256 signing secret is sent to every client in the page source:

   ```javascript
   const SECRET_KEY = "HTB{redacted}";
   ```

Because HMAC JWT signing uses the same secret to create and verify signatures, exposing
this value lets any visitor forge arbitrary valid session tokens. In this challenge,
the exposed secret is also the flag.

## Tools

- `curl`

## Lessons

- Never place JWT signing secrets in browser-delivered JavaScript.
- JWTs should be issued and signed only by the server.
- Client-side code and JWT payloads must always be treated as public information.

## Flag

`HTB{redacted}`
