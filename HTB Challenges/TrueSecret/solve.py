#!/usr/bin/env python3
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher, modes


KEY = b"AKaPdSgV"
IV = b"QeThWmYq"
CIPHERTEXT = (
    "+iTzBxkIgVWgWm/oyP/Uf6+qW+A+kMTQkouTEammirkz2efek8yfrP5l+mtFS+bW"
    "A7TCjJDK2nLAdTKssL7CrHnVW8fMvc6mJR4Ismbs/d/fMDXQeiGXCA=="
)


decryptor = Cipher(TripleDES(KEY * 3), modes.CBC(IV), backend=default_backend()).decryptor()
plaintext = decryptor.update(base64.b64decode(CIPHERTEXT)) + decryptor.finalize()
plaintext = plaintext[: -plaintext[-1]]  # PKCS#7 padding
print(plaintext.decode())
