---
ctf: "Curtin CTF 2026"
title: "Pinpoint 2"
category: "osint"
difficulty: ""
tags: ["osint", "aviation", "antarctica", "airport-codes"]
flag_format: "CURTIN_CTF{redacted}"
date: "2026-11-21"
---

## Challenge

> Wonder how one gets there.....

Flag format is `CURTIN_CTF{redacted}`. This is a follow-up to Pinpoint 1, which identified **Davis Station, Antarctica** as the target location. Pinpoint 2 asks how one travels there — pointing to the airfield that serves the station.

## Approach

### Phase 1 — Analyze

The challenge hint "Wonder how one gets there....." and the flag format `CURTIN_CTF{redacted}` both point clearly to an airport or airfield. The IATA and ICAO codes are the two standard designator systems for airports. Combined with Pinpoint 1's answer of Davis Station, Antarctica, the task is to identify the airport/skiway serving Davis Station and find its codes.

### Phase 2 — Recon

1. Researched how aircraft reach Davis Station, Antarctica. The Australian Antarctic Program (antarctica.gov.au) explains that fixed-wing flights operate under two seasonal modes:
   - Early season: flights land on a sea-ice runway near the station.
   - Later season (once sea ice deteriorates): flights use **Davis Plateau Skiway**, nicknamed **"Woop Woop"**, located approximately 40 km east of the station.

2. Searched for "Davis Plateau Skiway airport codes" and found the airport listed on Flightradar24 as **QAD** (IATA) / **AT07** (ICAO).

3. Cross-referenced with the Australian Antarctic Program's station update from 25 February 2022, which included a photo of the shelter at the skiway bearing a sign reading **"Woop Woop Domestic Terminal"** — confirming the location.

   ![Woop Woop Domestic Terminal](https://www.antarctica.gov.au/site/assets/files/58733/hermann_8.1200x0.jpg)

### Phase 3 — Infiltrate

No exploitation required — pure OSINT lookup.

The flag format `CURTIN_CTF{redacted}` fills directly with the two codes found:
- IATA: `QAD`
- ICAO: `AT07`

Result: `CURTIN_CTF{redacted}`

## Tools

- [Australian Antarctic Program — Ski Landing Area Locations](https://www.antarctica.gov.au/antarctic-operations/travel-and-logistics/aviation/intracontinental-operations/ski-landing-area-locations/)
- [Flightradar24 — QAD airport listing](https://www.flightradar24.com/data/airports/qad/statistics)
- [AAP Davis Station Update, 25 Feb 2022](https://www.antarctica.gov.au/news/stations/davis/2022/this-week-at-davis-25-february-2022/)

## Lessons

- When a flag format specifies `{IATA_ICAO}`, the answer is always a standard airport designator pair. Search both codes together on Flightradar24 or OurAirports.
- Remote research stations (Antarctic, Arctic, etc.) often have non-obvious airfields (skiways, sea-ice runways) that still carry official IATA/ICAO codes.
- Chained OSINT challenges build on each other — Pinpoint 1's answer (Davis Station) is the direct input to Pinpoint 2.

## Flag

`CURTIN_CTF{redacted}`

