from pathlib import Path


MULTIPLIER = 123
OFFSET = 18
MODULUS = 256


def decrypt(ciphertext: bytes) -> bytes:
    inverse = pow(MULTIPLIER, -1, MODULUS)
    return bytes(inverse * (byte - OFFSET) % MODULUS for byte in ciphertext)


if __name__ == "__main__":
    encoded = Path(__file__).with_name("msg.enc").read_text().strip()
    print(decrypt(bytes.fromhex(encoded)).decode())
