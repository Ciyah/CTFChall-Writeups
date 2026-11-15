---
ctf: "IBOH2026 CTF"
title: "Radio Silence"
category: "misc"
difficulty: ""
tags: []
flag_format: "IBOH26{...}"
date: "2026-11-14"
---

## Challenge

Author: @eric

Outpost Zulu went dark 72 hours ago. No voice, no data, no beacon. Our listening post is still intercepting traffic from the relay network, but every station broadcasts only static and enemy disinformation.

Command believes the message is not in what the stations say, but in which channels each one keeps open. Once recovered, it will be read out in standard radio phonetics. Transcribe it.

    Service: ctf-lookup.cofastic.com:5052 (UDP and TCP)
    Zone: signals.cofastic.com

Submit the recovered message as the full flag, including the IBOH26{} wrapper.


## Approach

### 1. Interpret the hint

The challenge provides a DNS zone and a service accepting UDP and TCP on port 5052. The key hint is that the message is hidden in “which channels each one keeps open.” This suggests inspecting which DNS record types exist at each name, rather than reading their contents.

### 2. Query the zone's NSEC record

NSEC records reveal the next existing name in a DNS zone and the record types present at the name being queried. Start at the zone apex:

```bash
dig +short @ctf-lookup.cofastic.com -p 5052 signals.cofastic.com NSEC
```

Response:

```text
alpha-213.signals.cofastic.com. NS SOA TXT RRSIG NSEC DNSKEY TYPE65534
```

The first field points to the next name, `alpha-213.signals.cofastic.com`. The remaining fields describe the record types at the current name, `signals.cofastic.com`.

### 3. Walk the NSEC chain

Query the name returned by the previous response:

```bash
dig +short @ctf-lookup.cofastic.com -p 5052 alpha-213.signals.cofastic.com NSEC
```

```text
alpha-921.signals.cofastic.com. TXT RRSIG NSEC
```

Continue following the first field until the chain returns to `signals.cofastic.com`. This enumerates the zone without needing to guess station names. The collected responses are saved in `nsec_records.json`.

Many names have only TXT records plus RRSIG and NSEC. The interesting names are the numbered relays: `relay-000`, `relay-001`, and so on. Their record-type sets vary.

For example:

```bash
dig +short @ctf-lookup.cofastic.com -p 5052 relay-000.signals.cofastic.com NSEC
dig +short @ctf-lookup.cofastic.com -p 5052 relay-001.signals.cofastic.com NSEC
```

```text
relay-001.signals.cofastic.com. AAAA SRV RRSIG NSEC
relay-002.signals.cofastic.com. MX AAAA SRV RRSIG NSEC CAA
```

These lines describe the types at `relay-000` and `relay-001`, respectively. The next-domain field is only a pointer.

### 4. Decode record presence into ASCII

Sort the relay names by their numeric suffix. Each relay encodes one byte through the presence or absence of eight record types. Ignore RRSIG and NSEC, which are present throughout the relay chain.

The working bit assignment is:

| Record type | Bit | Value |
| --- | --- | --- |
| A | 7 | 128 |
| AAAA | 6 | 64 |
| MX | 5 | 32 |
| TXT | 4 | 16 |
| HINFO | 3 | 8 |
| SRV | 2 | 4 |
| LOC | 1 | 2 |
| CAA | 0 | 1 |

Set a bit to 1 when its record type is present and to 0 when it is absent. This is the challenge's encoding order; it is not the order in which `dig` prints record types.

For `relay-000`, only AAAA and SRV are present among these eight types:

```text
A AAAA MX TXT HINFO SRV LOC CAA
0    1  0   0     0   1   0   0

01000100 = 0x44 = D
```

For `relay-001`, AAAA, MX, SRV and CAA are present:

```text
01100101 = 0x65 = e
```

Applying the same mapping to every relay produces readable radio phonetics, confirming the bit assignment.

The decoding logic in `solve.py` is:

```python
CHANNELS = ['A', 'AAAA', 'MX', 'TXT', 'HINFO', 'SRV', 'LOC', 'CAA']

message = ''
for record in relays:
    types = set(record['line'].split()[1:])
    byte = sum(1 << (7 - i)
               for i, channel in enumerate(CHANNELS)
               if channel in types)
    message += chr(byte)
```

### 5. Transcribe the radio phonetics

The decoded message is:

```text
Delta Zero Seven Alfa Foxtrot One Four One
Dash Eight Eight Two Foxtrot
Dash Four Three Bravo Charlie
Dash Eight Charlie Charlie Foxtrot
Dash Zero Four Charlie Charlie Six Five One Echo Bravo One Five Charlie
```

Convert the phonetic words to letters, spoken numbers to digits, and `Dash` to `-`:

```text
d07af141-882f-43bc-8ccf-04cc651eb15c
```

Wrap the recovered UUID in `IBOH26{}` to obtain the flag.

### 6. Reproduce the solution

Decode the saved responses without network access:

```bash
python3 solve.py
```

Alternatively, enumerate the live service and decode its responses:

```bash
python3 solve.py --live
```

Both modes print the recovered phonetic message followed by the full flag.

## Tools

`dig`, Python 3, `solve.py`, `nsec_records.json`.

## Lessons

NSEC permits zone walking, and its record-type metadata can carry data independently of the records' distracting contents.

## Flag

`IBOH26{redacted}`
