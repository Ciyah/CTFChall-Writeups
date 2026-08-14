#!/usr/bin/env python3
import json
import socket

HOST, PORT = "154.57.164.82", 30129


def request(payload):
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        stream = sock.makefile("rwb")
        stream.write(json.dumps(payload).encode() + b"\n")
        stream.flush()
        return json.loads(stream.readline())


if __name__ == "__main__":
    response = request({
        "action": "sign",
        "track": ["half", "add", "sub", "binary_division_odd_modulus", "div"],
    })
    with open("sample.json", "w", encoding="ascii") as output:
        json.dump(response, output)
    print({key: value for key, value in response.items() if key != "trace"})
    print("trace length:", len(response["trace"]))
