from jwcrypto import jwk
import jwt
from jwt import PyJWKClient
import json
import secrets
import os


def setup_auth():
    kid = secrets.token_hex(16)
    private_key_jwk = jwk.JWK.generate(kty="RSA", size=2048, alg="RS256", use="sig")
    private_key_jwk.kid = kid

    private_jwk_json = private_key_jwk.export_private()
    public_jwk_json = private_key_jwk.export_public()

    if not os.path.exists("./keys"):
        os.mkdir("keys")
    with open("./keys/private_key.json", mode="w") as file:
        json.dump(json.loads(private_jwk_json), file)

    jwks = {"keys": [json.loads(public_jwk_json)]}

    with open("./static/.well-known/jwks.json", mode="w") as file:
        json.dump(jwks, file)

    return kid, private_jwk_json, public_jwk_json


def generate_token(claims, kid):
    headers = {"kid": kid, "alg": "RS256", "typ": "JWT"}
    with open("./keys/private_key.json") as file:
        private_key = jwk.JWK.from_json(file.read())

    private_pem = private_key.export_to_pem(private_key=True, password=None)

    token = jwt.encode(claims, private_pem, algorithm="RS256", headers=headers)
    return token


def verify_token(token):
    try:
        jwks_path = os.path.abspath("static/.well-known/jwks.json")
        jwks_client = PyJWKClient(f"file:///{jwks_path.replace(os.sep, '/')}")
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        # print(signing_key.algorithm_name)

        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=[signing_key.algorithm_name],
            options={"verify_signature": True},
        )
        return decoded
    except:
        return False
