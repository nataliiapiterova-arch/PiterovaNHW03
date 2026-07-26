"""Plan/credit gating for book generation, plus Stripe Checkout billing.

Real Stripe integration (`app/stripe_client.py`), gated behind
STRIPE_SECRET_KEY/STRIPE_PRICE_ID being set. Without them, upgrading falls
back to an instant demo-mode flip so the product still works end-to-end
without payment credentials — see `stripe_enabled()`.
"""

import json
import os

from . import models, stripe_client

PLANS = {
    "free": {"label": "Free", "price_usd": 0, "monthly_books": 1},
    "pro": {"label": "Pro", "price_usd": 19, "monthly_books": None},  # None = unlimited
}


def can_generate(user):
    if user["plan"] == "pro":
        return True
    return user["credits"] > 0


def consume_credit(user):
    if user["plan"] != "pro":
        models.decrement_credit(user["id"])


def stripe_enabled():
    return bool(os.environ.get("STRIPE_SECRET_KEY") and os.environ.get("STRIPE_PRICE_ID"))


def start_upgrade(user, success_url, cancel_url):
    """Returns a URL to send the browser to in order to upgrade.

    With Stripe configured: a Stripe-hosted Checkout Session URL — the
    plan flips to "pro" only once the webhook confirms payment (see
    `process_webhook`). Without it: flips the plan immediately (demo mode)
    and returns `success_url` directly, so the button still works before
    real payment credentials exist.
    """
    if not stripe_enabled():
        upgrade_to_pro(user["id"])
        return success_url
    return stripe_client.create_checkout_session(
        api_key=os.environ["STRIPE_SECRET_KEY"],
        price_id=os.environ["STRIPE_PRICE_ID"],
        customer_email=user["email"],
        client_reference_id=user["id"],
        success_url=success_url,
        cancel_url=cancel_url,
    )


def upgrade_to_pro(user_id):
    models.set_user_plan(user_id, "pro")


def handle_checkout_completed(session):
    user_id = session.get("client_reference_id")
    if user_id:
        upgrade_to_pro(int(user_id))


def process_webhook(payload, sig_header):
    """Verifies and handles a Stripe webhook delivery.

    `payload` must be the raw request body bytes. Returns True if the
    signature verified and the event was processed, False otherwise (the
    caller should respond 400 on False so Stripe retries/alerts).
    """
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        return False
    if not stripe_client.verify_webhook_signature(payload, sig_header, webhook_secret):
        return False
    event = json.loads(payload)
    if event.get("type") == "checkout.session.completed":
        handle_checkout_completed(event["data"]["object"])
    return True
