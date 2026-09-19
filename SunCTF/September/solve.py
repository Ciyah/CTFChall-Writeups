#!/usr/bin/env python3
from pathlib import Path


MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6",
    "--...": "7", "---..": "8", "----.": "9",
}


def read_vlq(data, pos):
    value = 0
    while True:
        byte = data[pos]
        pos += 1
        value = (value << 7) | (byte & 0x7f)
        if byte < 0x80:
            return value, pos


def notes_and_name(track):
    pos = tick = 0
    running = None
    active = {}
    notes = []
    name = ""

    while pos < len(track):
        delta, pos = read_vlq(track, pos)
        tick += delta
        if track[pos] & 0x80:
            status = track[pos]
            pos += 1
        else:
            status = running

        if status == 0xff:
            kind = track[pos]
            pos += 1
            length, pos = read_vlq(track, pos)
            payload = track[pos:pos + length]
            pos += length
            if kind == 3:
                name = payload.decode("latin1")
            continue

        if status in (0xf0, 0xf7):
            length, pos = read_vlq(track, pos)
            pos += length
            running = None
            continue

        running = status
        event_type = status >> 4
        size = 1 if event_type in (0xc, 0xd) else 2
        payload = track[pos:pos + size]
        pos += size
        if event_type == 9 and payload[1] != 0:
            active[(status & 0xf, payload[0])] = tick
        elif event_type == 8 or (event_type == 9 and payload[1] == 0):
            key = (status & 0xf, payload[0])
            start = active.pop(key)
            notes.append((start, tick))

    return name, notes


data = Path("September.mid").read_bytes()
assert data[:4] == b"MThd"
track_count = int.from_bytes(data[10:12], "big")
pos = 8 + int.from_bytes(data[4:8], "big")
tuba_notes = None

for _ in range(track_count):
    assert data[pos:pos + 4] == b"MTrk"
    length = int.from_bytes(data[pos + 4:pos + 8], "big")
    track = data[pos + 8:pos + 8 + length]
    pos += 8 + length
    name, notes = notes_and_name(track)
    if name == "TUBA":
        tuba_notes = notes

assert tuba_notes is not None

# At 384 ticks/quarter note, 192-tick notes are dots and 384-tick notes
# are dashes. A 384-tick rest separates letters; the long rest separates words.
tokens = []
symbol = ""
for index, (start, end) in enumerate(tuba_notes):
    symbol += "." if end - start < 300 else "-"
    if index + 1 == len(tuba_notes):
        tokens.append(symbol)
        break
    rest = tuba_notes[index + 1][0] - end
    if rest > 900:
        tokens.extend((symbol, "/"))
        symbol = ""
    elif rest > 280:
        tokens.append(symbol)
        symbol = ""

decoded = "".join(" " if token == "/" else MORSE[token] for token in tokens)
prefix, flag_text = decoded.split()
print("Morse:", " ".join(tokens))
print("Decoded:", decoded)
print("Flag:", f"{prefix.lower()}{{{flag_text.lower()}}}")
