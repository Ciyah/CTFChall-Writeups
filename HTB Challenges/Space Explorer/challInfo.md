---
ctf: HTBLabs
title: Space Explorer
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Space Explorer

## Challenge
A lost space mission control system suffers from flawed authentication logic between its Sender and Receiver services. IP:154.57.164.82:30357 

## Approach

The public Go service blocks `getSecureCode`, but forwards requests whose parsed
action is `getcosmic` to the internal Flask service. The two JSON parsers treat
object keys differently:

- Go's `encoding/json` matches struct field names case-insensitively, so both
  `action` and `Action` populate `RequestData.Action`; the later value wins.
- Python accesses `data['action']` exactly and therefore ignores `Action`.

Send the secure action in the lowercase key for Flask, followed by a mixed-case
key containing the allowed action for Go:

```bash
curl -X POST 'http://154.57.164.82:30357/execute' \
  -H 'Content-Type: application/json' \
  --data '{"action":"getSecureCode","Action":"getcosmic"}'
```

Go sees the final value, `getcosmic`, and forwards the original body. Flask sees
the exact lowercase key, `getSecureCode`, and returns the flag.

## Tools

- Source review
- `curl`

## Lessons

Do not make authorization decisions at one service and then forward the original
un-normalized request to another parser. Parse once into a canonical schema,
reject duplicate or ambiguous keys, and forward the validated representation.

## Flag
`HTB{C0SM1C-BYP4SS}`
