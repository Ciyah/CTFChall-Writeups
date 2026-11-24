---
ctf: "Curtin CTF 2026"
title: "Lost"
category: "forensics"
difficulty: ""
tags: ["pcap", "network-forensics", "ipv4-fragmentation", "image-reconstruction"]
flag_format: "CURTIN_CTF{...}"
date: "2026-11-21"
---

## Challenge

Something’s lost along the way

## Approach

### Phase 1 — Analyze

1. The challenge ZIP (`Archive36.zip`) contained a single file: `Capt.pcapng`.
2. Opened the pcap with tshark to survey traffic types. Found:
   - 48 UDP datagrams destined for `192.168.1.13:4444` sent from `192.168.1.5`
   - 195 IPv4 fragment packets — many UDP datagrams were fragmented at the IP layer

### Phase 2 — Recon

3. Sampled the raw UDP payloads and found each began with the ASCII magic marker `TILE` followed by a fixed 12-byte header:
   ```
   Offset  Size  Field
   0       4     Magic: b’TILE’
   4       2     Row (big-endian uint16)
   6       2     Column (big-endian uint16)
   8       2     Total row count (big-endian uint16)
   10      2     Total column count (big-endian uint16)
   12      4     PNG data length (big-endian uint32)
   16      ...   PNG image data
   ```
4. The grid was 6 rows × 8 columns = 48 tiles, each 240 × 180 px → full image 1920 × 1080.
5. Because many UDP datagrams exceeded the MTU, they were split into multiple IPv4 fragments identified by the same (src_ip, dst_ip, ip_id) triple. Without reassembly, only the fragments carrying the first 1480 bytes of each datagram would surface, explaining why previous partial extraction yielded only 21 tiles.

### Phase 3 — Infiltrate

6. Wrote a Python script using **scapy** to:
   a. Load the pcap with `rdpcap`.
   b. Group all packets carrying IP fragment data by `(ip.src, ip.dst, ip.id)`.
   c. Sort each group by `ip.frag * 8` (fragment byte offset) and concatenate payloads.
   d. Strip the 8-byte UDP header from the first fragment of each reassembled datagram.
   e. Verify the `TILE` magic, parse the header, and extract the embedded PNG bytes.
   f. Save each tile as `tile_<row>_<col>.png` and paste it onto a 1920 × 1080 PIL canvas at `(col * 240, row * 180)`.
7. All 48 tiles reassembled successfully into `reassembled_full.png`.
8. Opening the image revealed the flag rendered diagonally across a teal background.

```python
# Key fragment-reassembly loop (scapy):
from collections import defaultdict
from scapy.all import rdpcap, IP, UDP
import struct

fragments = defaultdict(list)
for pkt in rdpcap("Capt.pcapng"):
    if IP not in pkt:
        continue
    ip = pkt[IP]
    if ip.flags & 0x1 or ip.frag > 0:          # MF set or non-zero offset
        key = (ip.src, ip.dst, ip.id)
        fragments[key].append((ip.frag * 8, bytes(ip.payload)))

for key, frags in fragments.items():
    frags.sort()
    blob = b""
    for offset, data in frags:
        blob += data[max(0, len(blob) - offset):]  # handle overlaps
    src_port, dst_port = struct.unpack_from(">HH", blob)
    if dst_port == 4444 and blob[8:12] == b’TILE’:
        row, col, rows, cols = struct.unpack_from(">HHHH", blob, 12)
        png_len = struct.unpack_from(">I", blob, 20)[0]
        png_data = blob[24:24 + png_len]
        # paste onto canvas at (col*240, row*180)
```

## Tools

- tshark (traffic survey, fragment/UDP counting)
- scapy (IPv4 fragment reassembly, raw payload extraction)
- Pillow / PIL (tile parsing and image reconstruction)

## Lessons

- **IPv4 fragmentation hides data from naive pcap parsers.** Tools that show only the first fragment of a fragmented UDP datagram will silently truncate any payload larger than ~1480 bytes. Always check for `ip.flags.mf==1` or `ip.frag_offset>0` and reassemble before parsing application data.
- **Custom binary protocols in UDP are common CTF patterns.** When you see repeated UDP traffic to a fixed port with consistent payload structure, dump one payload with `tshark -x` or scapy and look for a magic header — it almost always signals a hand-rolled framing protocol.
- **Scapy’s `ip.frag` field is in 8-byte units**, so the byte offset is `ip.frag * 8`.

## Flag

`CURTIN_CTF{redacted}`

