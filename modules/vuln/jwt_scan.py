import base64
import json


def _decode_segment(segment):
    padding = "=" * (-len(segment) % 4)
    return json.loads(base64.urlsafe_b64decode(segment + padding))


def run(context):
    auth_header = context.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        print("[JWT] No Bearer token found")
        return

    token = auth_header.split(" ", 1)[1]

    parts = token.split(".")
    if len(parts) != 3:
        print("[JWT] Authorization header is not a JWT")
        return

    try:
        payload = _decode_segment(parts[1])
        context.evidence["jwt_payload"] = payload
        print("[JWT] Decoded JWT payload")

    except Exception:
        print("[JWT] Failed to decode JWT")

