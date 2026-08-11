from sage.all import *
from Crypto.Util.Padding import pad, unpad
from secret import FLAG
import random

F = GF(257)

def random_matrix():
    return Matrix(F, [[ZZ(random.randint(0,15)) for _ in range(4)] for _ in range(4)])

K = random_matrix()
L = random_matrix()
T = random_matrix()

def S(x):
    return x**3

def S_inv(x):
    return x**171

def bytes_to_matrix(b):
    if len(b) != 16:
        raise ValueError("Block must be 16 bytes")
    rows = []
    for i in range(4):
        row = [F(b[4*i+j]) for j in range(4)]
        rows.append(row)
    return Matrix(F, rows)

def matrix_to_bytes(M):
    b = bytearray()
    for i in range(M.nrows()):
        for j in range(M.ncols()):
            b.append(int(M[i,j] % 256))
    return bytes(b)

def encrypt_block(plaintext_block):
    M = bytes_to_matrix(plaintext_block)
    M_sub = M.apply_map(S)
    C = K * M_sub * L + T
    return C

def encrypt_message(message):
    if isinstance(message, str):
        message = message.encode()
    padded = pad(message, 16)
    ciphertext = ""
    for i in range(0, len(padded), 16):
        block = padded[i:i+16]
        C = encrypt_block(block)
        hex_str = ''.join([format(int(C[i,j]), "02x") for i in range(4) for j in range(4)])
        ciphertext += hex_str
    return ciphertext

def encrypt_blueprint():
    return encrypt_message(FLAG)

def main():
    ct_flag = encrypt_blueprint()
    while True:
        print("\nNeonLab - Neon Core Encryption Service")
        print("1. Encrypt a message (raw text)")
        print("2. Get encrypted configuration (blueprint ciphertext)")
        opt = input("> ").strip()
        if opt == "1":
            msg = input("Enter message (raw text): ").strip()
            ct = encrypt_message(msg)
            print("Ciphertext (hex):", ct)
        elif opt == "2":
            print("Encrypted configuration (ciphertext, hex):", ct_flag)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
