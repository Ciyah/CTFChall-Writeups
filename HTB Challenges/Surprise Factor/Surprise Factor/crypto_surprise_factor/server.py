import hashlib, json, secrets, sys

from ecdsa import sign
from ec import G, scalar_mul, to_affine
from secret import PRIVATE_KEY

FLAG = open("flag.txt").read().strip()

MESSAGE_LENGTH = 32
PUBLIC_KEY = to_affine(scalar_mul(PRIVATE_KEY, G))

if PUBLIC_KEY is None:
    raise ValueError("unexpected point at infinity while deriving public key")

AVAILABLE_FUNCTIONS = [
    "add",
    "sub",
    "neg",
    "mul",
    "square",
    "double",
    "triple",
    "octuple",
    "half",
    "mod",
    "p256_quasi_reduce",
    "binary_division_odd_modulus",
    "inv",
    "div",
    "is_infinity",
    "to_jacobian",
    "to_affine",
    "randomize_coordinates",
    "is_on_curve_affine",
    "point_double",
    "point_add",
    "scalar_mul",
    "sign",
    "verify",
]


def parse_request(raw_request):
    if not raw_request.strip():
        raise ValueError("expected a JSON request on stdin")

    request = json.loads(raw_request)
    if not isinstance(request, dict):
        raise ValueError("request must be a JSON object")
    return request


def validate_tracked_functions(tracked_functions):
    requested = set(tracked_functions)
    unknown = sorted(requested.difference(AVAILABLE_FUNCTIONS))
    if unknown:
        names = ", ".join(unknown)
        raise ValueError(f"unknown traceable functions: {names}")
    return requested


def emit_response(payload):
    print(json.dumps(serialize_response(payload)), flush=True)
    return 0


def serialize_response(value):
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return hex(value)
    if isinstance(value, list):
        return [serialize_response(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize_response(item) for key, item in value.items()}
    return value


def parse_integer(value, field_name):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value, 0)
    raise ValueError(f"{field_name} must be an integer or a string encoding an integer")


def handle_sign(request):
    tracked_functions = request.get("track", [])
    if not isinstance(tracked_functions, list):
        raise ValueError("track must be a JSON array of function names")

    tracked_functions = validate_tracked_functions(tracked_functions)
    result = sign(
        PRIVATE_KEY,
        tracked_functions=tracked_functions,
        message_length=MESSAGE_LENGTH,
    )
    result["public_key"] = {
        "x": PUBLIC_KEY[0],
        "y": PUBLIC_KEY[1],
    }
    return result


def handle_submit(request):
    private_key = parse_integer(request.get("d"), "d")
    candidate_public_key = to_affine(scalar_mul(private_key, G))
    valid = candidate_public_key == PUBLIC_KEY
    result = {"valid": valid}
    if valid:
        result["flag"] = FLAG
    return result


def handle_request(request, current_hash):
    action = request.get("action", "sign")
    if action == "sign":
        return handle_sign(request), current_hash
    if action == "submit":
        return handle_submit(request), current_hash

    raise ValueError("action must be 'sign', or 'submit'")


current_hash = None
for raw_request in sys.stdin:
    if not raw_request.strip():
        continue
    try:
        request = parse_request(raw_request)
        response, current_hash = handle_request(request, current_hash)
        emit_response(response)
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        emit_response({"error": str(error)})