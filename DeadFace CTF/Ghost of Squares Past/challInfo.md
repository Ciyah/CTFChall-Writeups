---
ctf: "DeadFace CTF"
title: "
Ghost of Squares Past"
category: "osint"
difficulty: ""
tags: []
flag_format: "deadface{...}"
date: "2026-10-18"
---

## Challenge

Created By: @RP-01?

Intelligence gathered from DEADFACE communications suggests that the group has been using Savannah, Georgia's historic squares to conceal a coded message. Investigators recovered five clues, a combination of riddles and photographs, each pointing to a specific location within the city's historic district.

DEADFACE appears to have arranged these locations into a compass pattern, with the first four representing North, East, South, and West, and the fifth marking the center.

Your mission is to identify all five locations and reconstruct the hidden message before DEADFACE can put it to use.

For the first four locations, determine the year each square was established. For the final location, identify the surname engraved on its monument.

Flag Format: Deadface{YEAR-YEAR-YEAR-YEAR-SURNAME}

Submit your findings in the order provided by the clues. The flag is the year each square was discovered and the name etched into the 5th point. All in order.

Point 1 - Riddle

    First of them all, where the city began, A banker's green heart in Oglethorpe's plan. A Quaker from Rhode Island sleeps under stone here Mark the year this first square was laid out, and draw near.

Point 2 - Location

Point 3 - Riddle

    Riddle Just a ways away a battle of a northern frontier Gave its name to this ground eighteen-twelve drawing near. Where a feather once drifted and a founder stands tall, Mark the year it was laid out, the newest of all.

Point 4 - Location

Point 5 - Riddle

    Four points now marked, good work, you did your best Their meeting point holds the key to this test. Carry their years in that order, and seek the lone name Carved in the stone where their center lays claim.

Submit the flag as: deadface{YYYY-YYYY-YYYY-YYYY-surname}. Example: deadface{1990-1982-1956-1985-smith}.

## Approach

1. Read the two riddles and inspected `Point 2.png` and `Point 4.png` as
   location photographs of Savannah's historic squares.
2. Point 1 is **Johnson Square**: it was Savannah's first square and contains
   the grave and monument of Rhode Island Quaker Nathanael Greene. The City of
   Savannah dates it to **1733**.
3. Point 2 is **Oglethorpe Square**, recognizable from the supplied photograph
   and confirmed by its position east of the eventual center. It was laid out
   in **1742**.
4. Point 3 is **Chippewa Square**: it is named for the War of 1812's Battle of
   Chippewa, is associated with the floating-feather/bench scenes in *Forrest
   Gump*, and contains the James Oglethorpe monument. It was laid out in
   **1815**.
5. Point 4 is **Telfair Square**, recognizable from the supplied photograph
   and confirmed by its position west of the eventual center. It dates to
   **1733** (when it was called St. John's Square).
6. Plotting the four squares produces the required compass pattern around
   **Wright Square**: Johnson is north, Oglethorpe east, Chippewa south, and
   Telfair west. Wright Square's central monument honors William Washington
   Gordon, and its north-facing panel contains the lone surname **Gordon**.
7. Putting the four years and surname in clue order gives the flag.

## Image Evidence

### Point 1 — Johnson Square (1733)

The Nathanael Greene Monument and burial site match the riddle's Rhode Island
Quaker.

![Nathanael Greene Monument in Johnson Square](https://www.savannahga.gov/PhotoGallery/10/nathaniel%20green%20mon.jpg)

*Source: City of Savannah photo gallery.*

### Point 2 — Oglethorpe Square (1742)

The supplied location photograph is the square immediately east of Wright
Square.

![Supplied photograph of Oglethorpe Square](<Point 2.png>)

### Point 3 — Chippewa Square (1815)

The James Oglethorpe Monument confirms the location described by the riddle.

![James Oglethorpe Monument in Chippewa Square](https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/General_James_E._Oglethorpe_Statue_in_Chippewa_Square_%284351005904%29.jpg/1024px-General_James_E._Oglethorpe_Statue_in_Chippewa_Square_%284351005904%29.jpg)

*Photo: Jennifer Morrow, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), via Wikimedia Commons.*

### Point 4 — St. John’s Square (1733)

The supplied location photograph is the square immediately west of Wright
Square.

![Supplied photograph of Telfair Square](<Point 4.png>)

### Point 5 — Wright Square / Gordon Monument

The Gordon Monument occupies the center of the four-point compass. Its
north-facing panel reads only `GORDON`.

![William Washington Gordon Monument in Wright Square](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/William_Gordon_monument_in_Wright_Square_%284350251131%29.jpg/960px-William_Gordon_monument_in_Wright_Square_%284350251131%29.jpg)

*Photo: Jennifer Morrow, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), via Wikimedia Commons.*

## Tools

- `file` and ImageMagick `identify` to inspect the supplied PNG files
- Visual comparison of the photographs with Savannah square imagery
- City of Savannah facilities and monument records to confirm dates and the
  Wright Square monument

## Lessons

The compass wording is also a built-in verification mechanism: all four
identified squares line up exactly around Wright Square, so the photo matches
and center are not merely based on similar-looking parks.

## Flag

`deadface{1733-1742-1815-1733-gordon}`

