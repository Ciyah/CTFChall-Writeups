---
ctf: SunCTF
title: AttckDef
category: misc
difficulty: unknown
tags: []
flag_format: sunctf26{...}
date: 2026-09-05
---

# AttckDef

## Challenge
SUNCTF AD attack/defence.

Recover the final sunctf26{...} flag from the range and submit it here.

Launch the range from this challenge and keep the generated instance URL private to your team. Use that full URL as the base URL for solver scripts. Challenge support: @Kitkat in the event Discord. Rehack logo
https://sunctf.sunwaycybersecurityclub.org/plugins/team-runtime-auth/launch/4 

## Approach
1. Inspected `attckdef-handout/old_attack.pcap` with `tshark`. Traffic from
   Scap3G04T (`10.60.4.2`) showed repeated calls to
   `/api/notes/validate-token` with successively longer UUID prefixes, followed
   by a successful `/api/submit` request.
2. Confirmed the flaw in `source/app/routes_service.py:193-199`. An exact token
   returns the note content, a correct prefix (`on_file.startswith(submitted)`)
   sleeps for 10 seconds, and an incorrect prefix sleeps for only 3 seconds.
   Although both branches now return the same HTTP 200 body, their timing leaks
   every UUID character.
3. Updated `attckdef-handout/exploit.py` to accept the private instance base URL.
   It registers 16 accounts, tries all 16 hexadecimal characters concurrently
   at each UUID position, detects the candidate taking at least five seconds,
   and automatically solves the per-account math captchas.

   ```bash
   tshark -r attckdef-handout/old_attack.pcap -Y http \
     -T fields -e frame.number -e ip.src -e http.request.uri -e http.response.code -e http.file_data
   python attckdef-handout/exploit.py "$BASE"
   ```

4. Live values recovered from tick `14905520`:

   - Flag ID: `gameserver:NOTE-96476169-C513F7`
   - Share token: `cfc30869-4fc4-46bc-8024-6a142237e28b`
   - Planted flag: `SUN26CTPBCQGKGXGC5ZSV24HRCXR2`

   The solver submitted this exact body to `/api/submit`:

   ```json
   {"flag_id":"gameserver:NOTE-96476169-C513F7","flag":"SUN26CTPBCQGKGXGC5ZSV24HRCXR2"}
   ```

   The server replied with `status: accepted` and returned the final flag.

## Tools

- `tshark`
- Python 3 with `requests`
- Supplied service source

## Lessons

- Returning identical bodies and status codes does not hide a secret-dependent
  timing difference.
- Rate limits keyed only by account can be distributed across many cheaply
  registered accounts; simple captchas can also be solved automatically.
- UUIDs are not access-control secrets when an endpoint exposes a prefix oracle.

## Flag

`sunctf26{pr3f1x_l34k_1n_th3_fl4g_st0r3_xx}`
