"""Minimal HMAC-signed session tokens (stdlib only).

We only ever need HS256-style signing/verification for our own cookies (we
are both issuer and verifier), so a full JWT library — which on this system
pulls in a `cryptography` build that's broken for this Python version — is
unnecessary. This gives the same signed + expiring token behavior with zero
third-party dependencies.
"""

import base64
import hashlib
import hmac
import json
import time


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(text: str) -> bytes:
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


def sign(payload: dict, secret: str) -> str:
    body = _b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature = _b64encode(
        hmac.new(secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
    )
    return f"{body}.{signature}"


def verify(token: str, secret: str):
    """Returns the payload dict if valid and unexpired, else None."""
    if not token or "." not in token:
        return None
    body, _, signature = token.partition(".")
    expected = _b64encode(
        hmac.new(secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
    )
    if not hmac.compare_digest(signature, expected):
        return None
    try:
        payload = json.loads(_b64decode(body))
    except (ValueError, UnicodeDecodeError):
        return None
    exp = payload.get("exp")
    if exp is not None and time.time() > exp:
        return None
    return payload
