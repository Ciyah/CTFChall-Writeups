---
ctf: HTBLabs
title: Sattrack
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-12
---

# Sattrack

## Challenge
Welcome to the Sattrack Bug Bounty Program! Help us find security flaws in our satellite monitoring platform for authorized partners. Use partner@rockyou.xyz:partn3r123 to log in. Submit non-security issues via /report for admin support. IPs:154.57.164.67:31361, 154.57.164.67:31989 

## Approach

1. Identified `31989` as the Flask/nginx satellite application and `31361` as the Express admin-report bot.
2. Logged in with the supplied partner account and mapped the authenticated routes, including `/partner/share` and the protected `/admin/*` area.
3. Confirmed a client-side prototype-pollution source on `/login`: the recursive merge accepts `__proto__`, and the polluted `JS_FILES` property is consumed by a dynamic script loader. This is the vulnerability hinted at by the flag.
4. While validating the authentication boundary, found that the default credentials `admin@sattrack.com:admin123` authenticate as an administrator.
5. Requested `/admin/users` with the resulting admin JWT and recovered the flag from the user listing.

## Tools

- `curl`
- `ffuf`
- `rg`
- `john`

## Lessons

- Recursive client-side merges must reject `__proto__`, `constructor`, and `prototype` keys.
- Never consume inherited configuration properties when dynamically creating script elements; use own-property checks and a strict allowlist.
- Default administrative credentials can collapse an otherwise multi-stage browser exploit.

## Flag

`HTB{redacted}`
