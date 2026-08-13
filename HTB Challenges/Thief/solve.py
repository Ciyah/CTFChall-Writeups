#!/usr/bin/env python3
"""Recover the file exfiltrated by windowsupdate.exe from challenge.pcap."""

import argparse
import subprocess
from pathlib import Path

from Crypto.Cipher import AES


KEY = b"The Bloodharbor!"
PREFIX = b"exfil-"


def extract_chunks(pcap: Path):
    command = [
        "tshark",
        "--disable-protocol",
        "hipercontracer",
        "-r",
        str(pcap),
        "-Y",
        "icmp.type==8 && ip.src==192.168.127.146",
        "-T",
        "fields",
        "-e",
        "icmp.ident",
        "-e",
        "icmp.seq",
        "-e",
        "data.data",
    ]
    output = subprocess.check_output(command, text=True)

    chunks = []
    for line in output.splitlines():
        ident_text, seq_text, payload_hex = line.split("\t")
        payload = bytes.fromhex(payload_hex)
        if not payload.startswith(PREFIX):
            continue

        iv = payload[len(PREFIX) : len(PREFIX) + AES.block_size]
        ciphertext = payload[len(PREFIX) + AES.block_size :]
        plaintext = AES.new(KEY, AES.MODE_CBC, iv).decrypt(ciphertext)
        chunks.append((int(ident_text), int(seq_text), plaintext))

    # The malware's binary-tree scrambler reverses odd-depth groups. The ICMP
    # identifier stores the depth and the sequence number stores group position.
    chunks.sort(key=lambda item: (item[0], item[1] if item[0] % 2 == 0 else -item[1]))
    return chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pcap",
        nargs="?",
        type=Path,
        default=Path("Thief/misc_thief/challenge.pcap"),
    )
    parser.add_argument("-o", "--output", type=Path, default=Path("recovered.png"))
    args = parser.parse_args()

    chunks = extract_chunks(args.pcap)
    recovered = b"".join(chunk[2] for chunk in chunks).rstrip(b"\x00")
    args.output.write_bytes(recovered)
    print(f"Recovered {len(chunks)} chunks ({len(recovered)} bytes) to {args.output}")


if __name__ == "__main__":
    main()
