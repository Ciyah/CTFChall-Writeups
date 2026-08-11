---
ctf: HTBLabs
title: Secure Notes
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Secure Notes

## Challenge
We built this note-taking app to be so simple, there can't possibly be any bugs. We even added a door to claim the flag. However, only those who knock from inside may enter IP:154.57.164.75:31602

## Approach

The application uses vulnerable `mongoose@7.2.4` and passes the complete JSON
body directly to `Note.findByIdAndUpdate()`. This permits CVE-2023-3696: a
field can be renamed to a path below `__proto__`, and hydrating the resulting
document pollutes `Object.prototype`.

Node's `net.Socket#remoteAddress` uses a cached `_peername.address` value. Two
malicious notes can therefore supply the two inherited properties needed to
make the socket appear local:

1. Create a note whose title is `seed`, then update it with
   `{"$rename":{"title":"__proto__._peername"}}`.
2. Create a note whose title is `127.0.0.1`, then update it with
   `{"$rename":{"title":"__proto__.address"}}`.
3. Request `/flag`. The inherited `_peername` string is boxed, its inherited
   `address` resolves to `127.0.0.1`, and the localhost check succeeds.

## Tools

- Source review
- `curl`

## Lessons

- Never pass an untrusted request body directly to a database update method.
- Prototype pollution can become an authorization bypass through runtime
  gadgets even when the polluted property is not used directly by app code.
- Upgrade Mongoose beyond the versions affected by CVE-2023-3696.

## Flag

`HTB{redacted}`
