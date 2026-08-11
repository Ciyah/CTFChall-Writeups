---
ctf: HTBLabs
title: Protein Cookies
category: crypto
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-10
---

# Protein Cookies

## Challenge
Another day of flexing your muscles in the mirror and still not being satisfied with your body image. Pumped full of adrenaline and creatine, the only thing missing for you is a good workout program. We heard that the best one out there is from the Swole Eagle gym, but they've closed down the registrations because the FDA is hunting them down for the one secret that natty bodybuilders hate. With an appetite for breaking rules, and an oven full of protein cookies ready to become the post-workout treat of the day, you'll have to get the right exercise going to not waste any of that precious muscle mass building potential. Infiltrate the portal of the gym membership and get the exercise program you know you deserve! 🍪 IP: 154.57.164.77:31813

## Approach

The application gives every visitor a cookie of the form:

```text
base64(message).base64(sha512(secret || message).hexdigest())
```

For a guest, the decoded message is
`username=guest&isLoggedIn=False`. Because this is a plain secret-prefix
SHA-512 MAC rather than HMAC, it is vulnerable to a hash length-extension
attack. The secret is 16 bytes long (`os.urandom(16)`), so extend the signed
message with `&isLoggedIn=True`, including the required SHA-512 glue padding,
and compute the continued digest from the known guest digest.

After base64-encoding the extended message and the new hexadecimal digest,
send them as the `login_info` cookie to `/program`. `parse_qs()` returns both
`isLoggedIn` values, and `v[-1]` selects the appended `True`. The endpoint then
returns `flag.pdf`.

## Tools

- `curl`
- `hlextend` (SHA-512 length extension)
- `mutool draw -F txt`

## Lessons

- Do not use `hash(secret || message)` as a MAC with Merkle-Damgard hashes.
  Use HMAC and compare tags with a constant-time comparison.
- Avoid allowing duplicate security-sensitive parameters to override earlier
  values during query-string parsing.

## Flag

`HTB{redacted}`
