"""Minimal Stripe REST client (stdlib only — no `stripe` package needed).

Stripe's API is plain HTTPS, form-encoded requests with bearer-token auth,
and webhook signatures are just HMAC-SHA256 — both are simple enough that
hand-rolling avoids a dependency this sandbox can't install anyway. Swap
this for the official `stripe` package later if you want more of the API
surface (subscription management, customer portal, etc.) than the two
calls used here.
"""

import hashlib
import hmac
import json
import time
import urllib.error
import urllib.parse
import urllib.request

STRIPE_API_BASE = "https://api.stripe.com/v1"


def _request(path, data, api_key):
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(f"{STRIPE_API_BASE}/{path}", data=body, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Stripe API error ({exc.code}): {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach Stripe: {exc.reason}") from exc


def create_checkout_session(api_key, price_id, customer_email, client_reference_id, success_url, cancel_url):
    """Creates a subscription Checkout Session and returns its hosted URL."""
    data = {
        "mode": "subscription",
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": "1",
        "customer_email": customer_email,
        "client_reference_id": str(client_reference_id),
        "success_url": success_url,
        "cancel_url": cancel_url,
    }
    session = _request("checkout/sessions", data, api_key)
    return session["url"]


def verify_webhook_signature(payload, sig_header, webhook_secret, tolerance_seconds=300):
    """Verifies a Stripe webhook per their documented scheme: HMAC-SHA256
    over "{timestamp}.{payload}", compared against the "v1" signature in
    the Stripe-Signature header. `payload` must be the raw request body
    bytes (not re-serialized JSON) — Stripe signs the exact bytes sent.
    """
    if not sig_header:
        return False
    try:
        parts = dict(kv.split("=", 1) for kv in sig_header.split(",") if "=" in kv)
    except ValueError:
        return False
    timestamp = parts.get("t")
    signature = parts.get("v1")
    if not timestamp or not signature:
        return False
    try:
        if abs(time.time() - int(timestamp)) > tolerance_seconds:
            return False
    except ValueError:
        return False
    signed_payload = f"{timestamp}.".encode("utf-8") + payload
    expected = hmac.new(webhook_secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
