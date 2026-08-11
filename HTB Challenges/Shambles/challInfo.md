---
ctf: HTBLabs
title: Shambles
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Shambles

## Challenge
Room... IP:154.57.164.67:32369

## Approach

The login endpoint decrypts user-controlled AES-CBC ciphertext before validating
the JWT. Its distinct padding and JWT validation messages form a padding oracle.
Use that oracle to recover `AES_DEC(C_i)` for each ciphertext block. The server
uses a fixed key and IV for both tokens and user data, and the first JWT plaintext
block is the known base64url header `eyJhbGciOiJIUzI1`, so the IV follows from
`IV = AES_DEC(C_0) XOR known_plaintext`. Decrypt the account-data ciphertext,
split its card number and balance, then withdraw the full balance.

## Tools

- Python socket client and CBC padding-oracle implementation: `solve.py`

## Lessons

- Do not expose different responses for padding failures and authentication
  failures; authenticate ciphertext before attempting decryption.
- Reusing a fixed CBC IV across different messages allowed the known JWT header
  to reveal the IV needed to decrypt the account data.

## Flag

`HTB{522c0a35508c32a19587479c081cf928}`
