---
ctf: HTBLabs
title: NeoVault
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# NeoVault

## Challenge
Neovault is a trusted banking app for fund transfers and downloading transaction history. You're invited to explore the app, find potential vulnerabilities, and uncover the hidden flag within IP:154.57.164.75:31804 .

## Approach

1. Registered a normal account through `POST /api/v2/auth/register` and logged in.
2. Inspected the Next.js client bundles and found both current v2 endpoints and
   deprecated v1 endpoints.
3. The deprecated `POST /api/v1/transactions/download-transactions` endpoint
   requires an `_id` supplied in the JSON body instead of deriving it from the
   authenticated session.
4. The endpoint passes `_id` to MongoDB without enforcing that it is a scalar
   ObjectId. Sending a `$ne` operator selects a different user's record:

   ```http
   POST /api/v1/transactions/download-transactions
   Content-Type: application/json
   Cookie: token=<authenticated JWT>

   {"_id":{"$ne":"<our user id>"}}
   ```

5. Extracting text from the returned PDF reveals the `neo_system` statement.
   Its transactions include a transfer for `user_with_flag` whose description
   contains the flag.

## Tools

- `curl`
- `mutool draw -F txt`

## Lessons

- Deprecated APIs remain exploitable when they are still routed and reachable.
- Object-level authorization must bind requested records to the authenticated
  identity rather than trusting a body parameter.
- Validate identifiers as scalar ObjectIds before using them in database queries;
  otherwise MongoDB query operators can turn an IDOR into broader record selection.

## Flag

`HTB{redacted}`
