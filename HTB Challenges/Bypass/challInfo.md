---
ctf: HTBLabs
title: Bypass
category: rev
difficulty: easy
tags: [.NET, decompilation, authentication-bypass, AES]
flag_format: HTB{...}
date: 2026-08-11
---

# Bypass

## Challenge
The Client is in full control. Bypass the authentication and read the key to get the Flag.

## Approach

`Bypass.exe` is a 32-bit .NET Framework executable:

```text
$ file Bypass.exe
Bypass.exe: PE32 executable for MS Windows 4.00 (console), Intel i386 Mono/.Net assembly
```

Because it is managed code, it can be opened in a .NET decompiler such as ILSpy or
dnSpy. The names are obfuscated, but the program is small enough that the important
control flow is still obvious.

### 1. Identify the impossible login

The authentication method asks for a username and password, discards both values,
and returns `false` unconditionally:

```csharp
public static bool _1()
{
    Console.Write("Enter a username: ");
    string username = Console.ReadLine();
    Console.Write("Enter a password: ");
    string password = Console.ReadLine();
    return false;
}
```

Its caller only proceeds to the key check when that method returns `true`:

```csharp
if (_1())
{
    _2();
    return;
}
```

There are therefore no valid credentials to discover. The intended client-side
bypass is to change `return false` to `return true` in dnSpy, save the patched
assembly, and run it. The same result can be achieved in a debugger by changing the
method's return value at runtime.

### 2. Recover the secret key

The key-checking method compares the supplied value with a string loaded into
`_5._3`:

```csharp
string expectedKey = _5._3;
string suppliedKey = Console.ReadLine();

if (expectedKey == suppliedKey)
    Console.Write(_5._5 + _0._2 + _5._6);
```

The strings are stored in the embedded resource named `0`. Class `_7` reveals its
format: the first 32 bytes are an AES-256 key, the following 16 bytes are the IV,
and the remaining bytes are AES-CBC ciphertext. The resource can be extracted with
ILSpy and decrypted as follows:

```bash
dd if=0 of=cipher.bin bs=1 skip=48 status=none
openssl enc -d -aes-256-cbc \
  -K 7c05ff52467eb178e4f5283af4ccf853925a54c619f551d5534636eca63d9701 \
  -iv 5d6d0020032622a1328d430f7f687b15 \
  -in cipher.bin -out plain.bin
strings -a -el plain.bin
```

The decrypted strings include:

```text
ThisIsAReallyReallySecureKeyButYouCanReadItFromSourceSoItSucks
Nice here is the Flag:HTB{
SuP3rC00lFL4g
}
```

After bypassing authentication, enter this secret key:

```text
ThisIsAReallyReallySecureKeyButYouCanReadItFromSourceSoItSucks
```

The program concatenates the flag prefix, the static flag fragment, and the closing
brace.

## Tools

- `file` and `strings`
- ILSpy/`ilspycmd` or dnSpy
- OpenSSL

## Lessons

- Client-side authentication cannot protect a secret when the user controls the
  executable and can patch its decision logic.
- Obfuscated symbol names do not hide simple control flow from a .NET decompiler.
- Embedding an encryption key beside its ciphertext only obscures data; it does not
  protect it from static analysis.

## Flag

```text
HTB{redacted}
```
