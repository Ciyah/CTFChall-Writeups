---
ctf: "DeadFace CTF"
title: "Car Crash"
category: "osint"
difficulty: ""
tags: []
flag_format: "deadface{...}"
date: "2026-10-17"
---

## Challenge

Created By: @RP-01?

DEADFACE has been researching companies connected to one of their latest targets. Among the files recovered was a photo of a traffic accident involving a commercial truck.

We believe the truck may identify a company DEADFACE has taken an interest in. Determine which company owns the truck and when that company was founded.

Submit the flag as: deadface{MM_DD_YYYY}. Example: deadface{01_20_2026}

Download PNG(~2.5MB)
SHA256: 1aa227a57e32fb93e3cf34518902ef00e1a57b86f0929e583a017f721a0e06f8

## Approach

1. Inspecting `Car Crash.png` shows a commercial box truck in the center of
   the accident scene. The small marking on the upper-right side of its box is
   `USDOT: 080806` (the leading zero is only padding).
2. Querying USDOT number `80806` in the FMCSA SAFER carrier database identifies
   the carrier as **J B HUNT TRANSPORT INC**, DBA **J B HUNT**.
3. J.B. Hunt's 2021 Form 10-K states: "We were incorporated in Arkansas on
   August 10, 1961." The company's August 10, 2021 press release also says it
   marked its 60th anniversary that day, independently corroborating the date.
4. Formatting `08/10/1961` according to the requested `MM_DD_YYYY` pattern
   produces the flag.

## Tools

- Image inspection / ExifTool
- FMCSA SAFER carrier lookup:
  https://safer.fmcsa.dot.gov/query.asp?query_param=USDOT&query_string=80806&query_type=queryCarrierSnapshot&searchtype=ANY
- J.B. Hunt 2021 Form 10-K (SEC):
  https://www.sec.gov/Archives/edgar/data/728535/000143774922004457/jbht20211231_10k.htm
- J.B. Hunt 60th-anniversary release:
  https://www.jbhunt.com/our-company/newsroom/2021/08/j-b--hunt-celebrates-60th-anniversary

## Lessons

USDOT numbers are searchable carrier identifiers. A visually padded number
such as `080806` should also be checked without its leading zero (`80806`).

## Flag

`deadface{08_10_1961}`

