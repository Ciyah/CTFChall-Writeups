---
ctf: HTBLabs
title: SpeedNet
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# SpeedNet

## Challenge
Speednet is an ISP platform. Join our bug bounty to find vulnerabilities and retrieve the hidden flag. Test using the email service at http://IP:PORT/emails/ with address test@email.htb IP: 154.57.164.82:31232

## Approach

1. Downloaded the Vite JavaScript bundle and recovered the `/graphql` endpoint and
   the application's queries and mutations.
2. Used GraphQL introspection to discover the undocumented `devForgotPassword`
   mutation.
3. Registered `test@email.htb`, then exploited the `userProfile(userId: Int!)`
   IDOR with `userId: 1` to identify the administrator as
   `admin@speednet.htb`.
4. Called `devForgotPassword` for the administrator. It returned the password
   reset token directly, allowing the admin password to be changed.
5. Logging in still required 2FA. GraphQL alias batching allowed 500
   `verifyTwoFactor` attempts in each HTTP request, bypassing request-based rate
   limiting. The four-digit OTP was recovered and yielded an administrator JWT.
6. Queried `invoiceHistory` with the administrator JWT. One invoice number held
   the flag.

## Tools

- `curl`
- GraphQL introspection
- Python standard library (GraphQL alias batching)

## Lessons

- Disable schema introspection in production when it is not required, but do not
  treat that as a substitute for authorization.
- Enforce object-level authorization on `userProfile`.
- Never deploy developer-only password reset operations or return reset secrets.
- Rate-limit sensitive resolver executions, not only HTTP requests; cap GraphQL
  query complexity and aliases.

## Flag

`HTB{redacted}`
