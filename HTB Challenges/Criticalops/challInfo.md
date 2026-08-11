---
ctf: HTBLabs
title: Criticalops
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Criticalops

## Challenge
Criticalops is a web app used to monitor critical infrastructure in the XYZ region. Users submit tickets to report unusual behavior. Please uncover potential vulnerabilities, and retrieve the hidden flag within the system IP: 154.57.164.82:30420.

## Approach

1. Accessed the HTTPS service and inspected its public Next.js JavaScript bundles.
2. Found the JWT signing implementation in the login page bundle. The client signs
   HS256 tokens using the hard-coded secret `SecretKey-CriticalOps-2025`.
3. Registered and logged in as a normal user to obtain a valid user ID.
4. Forged a JWT containing that user ID and `"role":"admin"`, signed with the
   exposed secret.
5. Sent the forged token as `Authorization: Bearer <token>` to `/api/tickets`.
   The admin-only response disclosed the flag in a seeded ticket.

## Tools

- curl
- Python standard library (`hmac`, `hashlib`, `base64`) for JWT generation

## Lessons

- Never place authentication secrets or token-signing logic in client-side code.
- Authorization must be enforced server-side using server-issued identity claims.
- Sensitive credentials and flags should not be stored in broadly readable tickets.

## Flag

`HTB{redacted}`
