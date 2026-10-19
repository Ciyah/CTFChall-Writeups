---
ctf: "DeadFace CTF"
title: "File Dump 02 "
category: "osint"
difficulty: ""
tags: []
flag_format: "deadface{...}"
date: "2026-10-18"
---

## Challenge

Created By: @RP-01?

Now we know who is responsible for impersonating Daniel. Can you dig through these documents and maybe find a where? We are pretty sure Daniel had a computer stolen so where could that have happened?

Submit the flag as deadface{store_name}. Example: deadface{texas_tires}.

## Approach

This challenge continues File Dump 01. I copied its supplied `File Dump Challenge`
directory here and reviewed the documents and images together.

The relevant artifacts are:

- `reciept_1.png`: a receipt for computer servicing. Its stained address line still
  exposes the number `17`.
- `snip.png`: a storefront window showing the same `17`, an `OPEN` sign, and the
  words `Apple Specialist`.
- `advertising_ad_1.png`: an advertisement for Golden Donuts.
- `businesscard_1.png`: an Alaska business card, which provides a second geographic
  hint toward Anchorage.

Searching for an Apple specialist associated with suite 17 and Golden Donuts leads
to **Alaska MacStore**. Its official address is `2217 E. Tudor Rd., Suite 17,
Anchorage, AK 99507`. A business listing also describes it as being in the strip
mall behind Golden Donuts. This accounts for the suite number, Apple storefront,
Golden Donuts advertisement, and Alaska clue simultaneously.

## Tools

- `unzip` and `sed` to extract readable text from the DOCX files
- ExifTool and ImageMagick to inspect metadata and enhance the stained receipt
- Web search to correlate the storefront and surrounding-business clues

## Lessons

Artifacts that look like unrelated clutter can be geographic corroboration. The
storefront crop alone has several plausible visual matches, but the number `17`,
Alaska business card, and Golden Donuts advertisement uniquely reinforce Alaska
MacStore.

## Flag

`deadface{alaska_macstore}`

