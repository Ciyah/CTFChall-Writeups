#!/usr/bin/env python3
import socket
import string


HOST = "154.57.164.72"
PORT = 32370
PROMPT = b"Message for encryption: "
ALPHABET = string.printable[:95]  # ASCII 0x20 through 0x7e, reordered
FIXED = "CryptoHackTheBox"


def recv_until(sock, marker):
    data = bytearray()
    while not data.endswith(marker):
        chunk = sock.recv(8192)
        if not chunk:
            raise EOFError("server closed the connection")
        data.extend(chunk)
    return bytes(data)


def main():
    recovered = ""
    with socket.create_connection((HOST, PORT), timeout=15) as sock:
        recv_until(sock, PROMPT)

        while not recovered.endswith("}"):
            previous = (FIXED + recovered)[-15:]
            candidates = [previous + char for char in ALPHABET]

            # Each 'é' is one character but two UTF-8 bytes, adding one byte
            # of displacement without changing the server's character padding.
            shift = (15 - len(recovered)) % 16
            message = "".join(candidates) + "é" * shift
            sock.sendall(message.encode() + b"\n")

            response = recv_until(sock, PROMPT)
            ciphertext = bytes.fromhex(response[:-len(PROMPT)].strip().decode())
            blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]

            # aaes.pad(message) is character-aligned to 16 bytes before UTF-8
            # expansion, so its encoded size is char-aligned size + shift.
            chars = len(message)
            encoded_padded_message_len = chars + (-chars % 16) + 16 + shift
            target = (encoded_padded_message_len + len(recovered)) // 16

            try:
                match = blocks[:len(candidates)].index(blocks[target])
            except ValueError:
                raise RuntimeError(
                    f"no printable match after {recovered!r}; target block {target}"
                )

            recovered += ALPHABET[match]
            print(recovered, flush=True)


if __name__ == "__main__":
    main()
