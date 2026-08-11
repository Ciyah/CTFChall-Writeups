import hashlib
import secrets
from typing import Any

from bignum import add, inv, mod, mul, div
from trace import TRACE

from ec import G, N, point_add, scalar_mul, to_affine, to_jacobian, randomize_coordinates

TRACE.register("sign", "S")
TRACE.register("verify", "V")

def _hash_message(message):
    digest = hashlib.sha256(message).digest()
    return int.from_bytes(digest, "big")

def _random_scalar():
    scalar = 0
    while scalar == 0:
        scalar = secrets.randbelow(N)
    return scalar

def generate_keypair():
    private_key = _random_scalar()
    public_key = to_affine(scalar_mul(private_key, G))
    if public_key is None:
        raise ValueError("unexpected point at infinity while generating keypair")
    return private_key, public_key

def _configure_trace(tracked_functions):
    TRACE.configure(tracked_functions)
    TRACE.reset()

def _record_operation(name):
    TRACE.record(name)

def _finalize_trace(operation, tracked_functions, result, trace_path):
    payload = dict(result)
    payload["trace"] = TRACE.get_trace()

    if trace_path is not None:
        metadata = {
            "algorithm": "ECDSA",
            "curve": "secp256r1",
            "operation": operation,
            "tracked": sorted(tracked_functions or set()),
        }
        for key in ("hash", "r", "s"):
            if key in payload:
                metadata[key] = hex(payload[key])
        if "valid" in payload:
            metadata["valid"] = payload["valid"]
        TRACE.export_json(trace_path, metadata)

    return payload


def sign(privkey, tracked_functions=None, trace_path=None, message_length=32, hash_int=None, nonce=None):
    _configure_trace(tracked_functions)
    _record_operation("sign")

    if not 1 <= privkey < N: raise ValueError("private key out of range")
    if message_length <= 0: raise ValueError("message_length must be positive")
    if hash_int is not None and hash_int < 0: raise ValueError("hash_int must be non-negative")
    if nonce is not None and not 1 <= nonce < N: raise ValueError("nonce out of range")

    if hash_int is None:
        message = secrets.token_bytes(message_length)
        hash_int = _hash_message(message)

    while True:
        current_nonce = nonce if nonce is not None else _random_scalar()

        nonce_mask = secrets.randbelow(N)
        current_nonce = add(current_nonce, mul(nonce_mask, N))

        random_G = randomize_coordinates(G)
        point_r = scalar_mul(current_nonce, random_G)
        point_r = randomize_coordinates(point_r)

        current_nonce = mod(current_nonce, N)
        affine_r = to_affine(point_r)
        r = mod(affine_r[0], N)

        nonce_mask = secrets.randbelow(N)
        denominator = mul(nonce_mask, current_nonce) # masked nonce

        numerator = add(hash_int, mul(r, privkey))
        numerator = mul(nonce_mask, numerator)
        s = div(numerator, denominator, N)

        if r == 0:
            if nonce is not None: raise ValueError("fixed nonce produced r = 0")
            continue
        if s == 0:
            if nonce is not None: raise ValueError("fixed nonce produced s = 0")
            continue

        return _finalize_trace(
            "sign",
            tracked_functions,
            {"hash": hash_int, "r": r, "s": s},
            trace_path,
        )


def verify(hash_int, pubkey, signature, tracked_functions=None, trace_path=None):
    _configure_trace(tracked_functions)
    _record_operation("verify")

    r, s = signature
    if not (1 <= r < N and 1 <= s < N):
        return _finalize_trace(
            "verify",
            tracked_functions,
            {"valid": False},
            trace_path,
        )

    w = inv(s, N)
    u1 = mod(mul(hash_int, w), N)
    u2 = mod(mul(r, w), N)

    point_g = scalar_mul(u1, G)
    point_q = scalar_mul(u2, to_jacobian(pubkey))
    point_x = point_add(point_g, point_q)
    affine_x = to_affine(point_x)
    valid = affine_x is not None and mod(affine_x[0], N) == r

    return _finalize_trace(
        "verify",
        tracked_functions,
        {"valid": valid},
        trace_path,
    )
