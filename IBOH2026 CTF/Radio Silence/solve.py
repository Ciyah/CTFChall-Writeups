#!/usr/bin/env python3
"""Decode saved NSEC records; use --live to walk the challenge DNS zone."""
import json
import subprocess
import sys
from pathlib import Path

SERVER = 'ctf-lookup.cofastic.com'
ZONE = 'signals.cofastic.com.'
CHANNELS = ['A', 'AAAA', 'MX', 'TXT', 'HINFO', 'SRV', 'LOC', 'CAA']

def walk():
    name = ZONE
    seen = set()
    rows = []
    while name not in seen:
        seen.add(name)
        output = subprocess.check_output([
            'dig', '+short', '@' + SERVER, '-p', '5052', name, 'NSEC'
        ], text=True).strip()
        if not output or len(output.splitlines()) != 1:
            raise RuntimeError(f'Unexpected NSEC response for {name}: {output}')
        rows.append({'name': name, 'line': output})
        name = output.split()[0]
    return rows

if '--live' in sys.argv:
    records = walk()
else:
    records = json.loads(Path(__file__).with_name('nsec_records.json').read_text())

relays = sorted((r for r in records if r['name'].startswith('relay-')),
                key=lambda r: r['name'])
message = ''
for record in relays:
    types = set(record['line'].split()[1:])
    byte = sum(1 << (7 - i) for i, channel in enumerate(CHANNELS) if channel in types)
    message += chr(byte)
print(message)

phonetics = {
    'alfa': 'a', 'alpha': 'a', 'bravo': 'b', 'charlie': 'c',
    'delta': 'd', 'echo': 'e', 'foxtrot': 'f',
    'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
    'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
    'dash': '-',
}
payload = ''.join(phonetics[word.lower()] for word in message.split())
print('IBOH26{' + payload + '}')
