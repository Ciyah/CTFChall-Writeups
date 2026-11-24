---
ctf: "Curtin CTF 2026"
title: "Digital Footprints"
category: "forensics"
difficulty: ""
tags: ["prefetch", "windows-forensics", "timestamp", "FILETIME", "IST"]
flag_format: "CURTIN_CTF{redacted}"
date: "2026-11-22"
---

## Challenge

During the investigation, we uncovered traces of past system activity that could help identify which programs were accessed and determine when something suspicious was last running on the system.

Flag Format: CURTIN_CTF{redacted}
View Hint: Hint

Its IST time


## Approach

### Phase 1 — Analyze (files first)

1. Extracted the archive and listed its contents:
   ```
   unzip -Z1 Archive58.zip | sort
   ```
   The archive is a Windows Prefetch directory (`Archive58/`) containing `.pf` files for dozens of system executables.

2. Scanned filenames for anything suspicious. Among standard system binaries (IPCONFIG.EXE, LOGONUI.EXE, SVCHOST.EXE, etc.) one stood out immediately:
   ```
   SOMETHING.EXE-0A0B02BB.pf
   ```
   The deliberately generic name `SOMETHING.EXE` signals this is the target. The hash suffix `0A0B02BB` is the Windows Prefetch hash of the executable's path.

### Phase 2 — Recon and analysis

3. Installed the libscca Prefetch reader on Kali:
   ```
   sudo apt install libscca-utils
   ```

4. Extracted and read the Prefetch record:
   ```bash
   pf='SOMETHING.EXE-0A0B02BB.pf'
   cp Archive58/"$pf" .
   sccainfo "$pf" | less
   ```

5. Key findings from `sccainfo`:
   - **Executable path**: `\DEVICE\HARDDISKVOLUME4\USERS\HELIOS\DESKTOP\SOMETHING.EXE`
     → Confirms it ran from the desktop of user **Helios**.
   - **Three recorded launch timestamps (UTC)**:
     | # | UTC time            | IST (UTC+5:30)      |
     |---|---------------------|---------------------|
     | 1 | 2026-10-26 17:31:51 | 2026-10-26 23:01:51 |
     | 2 | 2026-10-26 17:33:03 | 2026-10-26 23:03:03 |
     | 3 | 2026-10-26 17:36:40 | **2026-10-26 23:06:40** ← latest |

   - The hint says IST, so the flag uses the **latest** timestamp converted to India Standard Time (UTC+5:30).

### Phase 3 — Infiltrate / flag extraction

6. Located the raw Windows FILETIME for the latest run at offset `0x80` in the decompressed Prefetch data:
   ```
   0x01DD65708F80E872
   ```
   FILETIME counts 100-nanosecond ticks since 1601-01-01 00:00:00 UTC.

7. Converted independently of system timezone with Python to verify:
   ```python
   from datetime import datetime, timedelta, timezone
   from zoneinfo import ZoneInfo

   ticks = 0x01DD65708F80E872
   epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
   utc = epoch + timedelta(microseconds=ticks // 10)
   ist = utc.astimezone(ZoneInfo("Asia/Kolkata"))
   print(ist.strftime("CURTIN_CTF{redacted}"))
   # → CURTIN_CTF{redacted}
   ```

8. Submitted the flag.


## Tools

- `unzip` — list and extract the archive
- `libscca-utils` / `sccainfo` — parse Windows Prefetch (`.pf`) records
- `python3` with `zoneinfo` — convert raw FILETIME to IST


## Lessons

- Windows Prefetch records store up to 8 recent execution timestamps per executable as 64-bit FILETIMEs in the compressed `.pf` file. `sccainfo` from `libscca-utils` decodes them directly.
- The ZIP modification timestamp for a `.pf` file is unreliable for flag purposes (it lacks seconds and reflects archive creation, not execution time). Always read timestamps from inside the Prefetch record itself.
- When the flag asks for "last ran" + a specific timezone, take the **maximum** of all recorded timestamps and convert to that zone. India Standard Time = UTC+5:30.
- A suspiciously generic executable name (SOMETHING.EXE on a user's Desktop) is the first indicator to investigate in a Prefetch forensics challenge.


## Flag

`CURTIN_CTF{redacted}`
