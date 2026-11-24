---
ctf: "Curtin CTF 2026"
title: "Radio Silence"
category: "osint"
difficulty: ""
tags: []
flag_format: "CTF{...}"
date: "2026-11-21"
---

## Challenge

Found this at the bottom of a drawer while cleaning, next to a box of dead smart bulbs. I can’t even remember what it was called, the company’s website is long gone, and now I kind of wonder what happened to them. Someone must have kept records somewhere. What I really want to know is the exact hardware revision printed on its circuit board.

Flag format is CURTIN_CTF{redacted}


## Approach

### Phase 1 — Analyze (files first)

1. Examined `radio_silence.png`: a Bluetooth keyfob photographed open on a blue mat with dual rulers — the characteristic setup of an FCC lab photo (Intertek / UL / similar). The PCB has a QR code sticker and a CR2032 coin-cell holder. No other files were provided initially.

2. The challenge text says the company's website is "long gone" and asks for the "exact hardware revision **printed on its circuit board**" — pointing directly to the PCB silkscreen, which is typically captured in the FCC Internal Photos exhibit.

### Phase 2 — Recon and analysis

3. **Decoded the QR code** on the PCB (visible in `radio_silence.png`). It decoded to the string `DC2C26BE400B` — a MAC address in compact hex form: `DC:2C:26:BE:40:0B`.

4. **OUI lookup** for `DC:2C:26`: registered to **Iton Technology Co., Ltd.** (Shenzhen) — a manufacturer of BLE modules. This confirmed the device is Bluetooth LE and uses an Iton module.

5. **Device identification via FCC database**: searched for a Bluetooth keyfob filed by a smart-bulb startup. The FCC ID `2ABLO4001` matched: grantee "BeON Home, Inc.", equipment description "Keyfob", grant date 2016-07-11, tested at Intertek Shenzhen. The product code `4001` in the FCC ID matches the `4001` in the board name. BeON Home made smart security LED bulbs paired with a Bluetooth keyfob — a now-defunct company whose website went dark, matching the challenge narrative exactly.

6. The two FCC Internal Photos (`2ABLO4001-Internal-Photos-1D68D137.jpg`, `2ABLO4001-Internal-Photos-89BC4245.jpg`) are included in the challenge folder. The bare-PCB shot (`89BC4245`) shows the silkscreen text clearly along the right edge of the board.

### Phase 3 — Infiltrate (flag extraction)

7. Read the silkscreen from the bare-PCB FCC Internal Photo (`2ABLO4001-Internal-Photos-89BC4245.jpg`): the right edge reads **`BEONBT4001_Ver1.0_20160409`** — board name `BEONBT4001`, version `Ver1.0`, date code `20160409` (April 9, 2016, ~3 months before the FCC grant).

8. Wrapped in the flag format:

```
CURTIN_CTF{redacted}
```

## Tools

- QR code decoder (any; the QR is visible in the challenge photo)
- IEEE OUI lookup — `https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries` or `https://maclookup.app/`
- FCC ID database — `https://fccid.io/2ABLO4001` or `https://fcc.report/FCC-ID/2ABLO4001`
- Direct image inspection of the FCC Internal Photos exhibits (provided in the challenge folder)

## Lessons

- **FCC filings outlive companies.** When a device's manufacturer has gone dark, the FCC database preserves photos, test reports, and PCB silkscreens indefinitely. For any wireless device, search by FCC ID.
- **QR codes on PCBs are almost always MAC addresses or serial numbers.** Decoding the QR first gave the OUI, which immediately narrowed to the BLE module vendor and confirmed the device type.
- **OUI → vendor → product pivot**: knowing the BLE module OUI (Iton Technology) confirmed the hardware class, and the challenge narrative (smart bulbs, defunct website) pointed to BeON Home specifically.
- **FCC Internal Photos = PCB photos**. If the flag asks for a silkscreen value and the company is gone, the FCC exhibit is the canonical source.
- The challenge title "Radio Silence" is thematic: the company went radio-silent (defunct), and the records that survived were the RF regulatory filings.

## Flag

```
CURTIN_CTF{redacted}
```

