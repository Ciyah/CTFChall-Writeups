---
ctf: HTBLabs
title: RAuth
category: rev
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# RAuth

## Challenge
My implementation of authentication mechanisms in C turned out to be failures. But my implementation in Rust is unbreakable. Can you retrieve my password? IP:154.57.164.82:32023

## Approach

### 1. Initial inspection

The challenge provides one executable:

```text
RAuth/challenge/rauth
```

Identifying the file shows that it is a 64-bit PIE ELF executable with debug
information and symbols still present:

```bash
file RAuth/challenge/rauth
```

```text
ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped
```

Running it reveals a simple password prompt:

```bash
chmod +x RAuth/challenge/rauth
./RAuth/challenge/rauth
```

```text
Welcome to secure login portal!
Enter the password to access the system:
You entered a wrong password!
```

Because the executable is not stripped, its Rust `main` function is easy to
locate:

```bash
nm -C RAuth/challenge/rauth | grep main
```

```text
0000000000006460 t rauth::main
0000000000006bd0 T main
```

### 2. Authentication routine

Disassembling `rauth::main` exposes calls to the Salsa20 implementation:

```bash
objdump -d -Mintel --demangle \
  --start-address=0x6460 --stop-address=0x6bd0 \
  RAuth/challenge/rauth
```

The relevant symbols are:

```text
salsa20::core::Core<R>::new
<salsa20::salsa::Salsa<R> as cipher::stream::StreamCipher>::try_apply_keystream
```

The routine performs these operations:

1. Read the password and remove its trailing newline.
2. Initialize Salsa20 from a hard-coded 32-byte key and 8-byte nonce.
3. Copy the supplied password into a byte vector.
4. Apply the Salsa20 keystream to it.
5. Require a length of exactly 32 bytes.
6. Compare the result with a hard-coded 32-byte ciphertext.
7. If it matches, decrypt and print a second embedded ciphertext containing the
   flag.

Because Salsa20 is a symmetric stream cipher, decrypting the expected password
ciphertext with the embedded key and nonce directly recovers the required
password.

### 3. Extracting the constants

The constants reside in `.rodata` around virtual address `0x39ca0`:

```bash
objdump -s --start-address=0x39c90 --stop-address=0x39d10 \
  RAuth/challenge/rauth
```

The key is stored as ASCII:

```text
0x39ca0: 65663339 66346632 30653736 65333362  ef39f4f20e76e33b
0x39cb0: 64323566 34646233 33386538 31623130  d25f4db338e81b10
```

Therefore:

```text
Key: ef39f4f20e76e33bd25f4db338e81b10
```

The nonce is loaded as the little-endian immediate
`0x3361303732633464`, whose in-memory byte representation is:

```text
Nonce: d4c270a3
```

The expected encrypted password is the following 32 bytes:

```text
05055fb1a329a8d558d9f556a6cb31f3
24432a31c99dec72e33eb66f62ad1bf9
```

### 4. Recovering the password

Decrypting that ciphertext using Salsa20 with the extracted key and nonce gives:

```text
TheCrucialRustEngineering@2021;)
```

The plaintext is exactly 32 bytes long, matching the explicit length check in
the authentication routine.

For example, with PyCryptodome the decryption can be reproduced as follows:

```python
from Crypto.Cipher import Salsa20

key = b"ef39f4f20e76e33bd25f4db338e81b10"
nonce = b"d4c270a3"
ciphertext = bytes.fromhex(
    "05055fb1a329a8d558d9f556a6cb31f3"
    "24432a31c99dec72e33eb66f62ad1bf9"
)

cipher = Salsa20.new(key=key, nonce=nonce)
password = cipher.decrypt(ciphertext)
print(password.decode())
```

### 5. Validation

The recovered password authenticates successfully against the local binary:

```bash
printf '%s\n' 'TheCrucialRustEngineering@2021;)' | \
  ./RAuth/challenge/rauth
```

```text
Welcome to secure login portal!
Enter the password to access the system:
Successfully Authenticated
Flag: "HTB{redacted}"
```

The local flag is intentionally a placeholder. Submitting the same password to
the remote instance returns the real flag:

```bash
printf '%s\n' 'TheCrucialRustEngineering@2021;)' | \
  nc 154.57.164.82 32023
```

```text
Welcome to secure login portal!
Enter the password to access the system:
Successfully Authenticated
Flag: "HTB{redacted}"
```

## Tools

- `file` - identify the executable format and whether symbols were stripped
- `strings` - perform an initial search for useful strings and library names
- `nm -C` - locate demangled Rust symbols, including `rauth::main`
- `objdump` - inspect the authentication code and dump embedded constants
- Python - reproduce Salsa20 decryption
- `nc` - submit the recovered password to the remote service

## Lessons

- Rust's memory safety does not protect secrets embedded directly in a client
  executable.
- An unstripped binary with debug information makes function and dependency
  identification substantially easier.
- Stream-cipher encryption is reversible with the same key, nonce, and
  keystream. Comparing an encrypted user input against a bundled ciphertext
  therefore exposes the original password when all parameters are shipped in
  the binary.
- Immediate integer constants on x86-64 must be interpreted using little-endian
  byte order. The nonce immediate `0x3361303732633464` becomes the ASCII string
  `d4c270a3` in memory.
- Local challenge flags may be decoys or placeholders; the recovered credential
  should be validated against the supplied remote instance.

## Flag

```text
HTB{redacted}
```
