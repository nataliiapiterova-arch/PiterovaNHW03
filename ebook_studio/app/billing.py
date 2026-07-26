"""Plan/credit gating for book generation, plus Stripe Checkout billing.

Deliberately *not* "unlimited books" on any paid tier — a single complete
ebook (outline + full chapters + cover + marketing package) can burn a
meaningful amount of LLM spend, and a customer generating hundreds of long
books on a flat monthly fee would cost more than the subscription brings
in. Each paid plan gets a fixed, generous monthly credit allotment instead.

Real Stripe integration (`app/stripe_client.py`) is gated behind
STRIPE_SECRET_KEY + a price ID for the chosen plan. Without them, upgrading
falls back to an instant demo-mode flip so the product still works
end-to-end without payment credentials — see `stripe_enabled()`.
"""

import json
import os
from datetime import datetime, timedelta, timezone

from . import models, stripe_client

PLANS = {
    "free": {
        "label": "Free",
        "price_usd": 0,
        "monthly_credits": 1,
        "refreshes": False,
        "max_chapters": 3,
        "watermark": True,
        "commercial_use": False,
        "white_label": False,
        "description": "One short ebook, PDF, watermarked cover — try it out.",
    },
    "creator": {
        "label": "Creator",
        "price_usd": 19,
        "monthly_credits": 3,
        "refreshes": True,
        "max_chapters": 20,
        "watermark": False,
        "commercial_use": True,
        "white_label": False,
        "description": "3 complete ebooks per month, EPUB/PDF, professional covers.",
    },
    "publisher": {
        "label": "Publisher",
        "price_usd": 49,
        "monthly_credits": 10,
        "refreshes": True,
        "max_chapters": 20,
        "watermark": False,
        "commercial_use": True,
        "white_label": False,
        "description": "10 ebooks/month, commercial use, launch kits and content repurposing.",
    },
    "agency": {
        "label": "Agency",
        "price_usd": 99,
        "monthly_credits": 25,
        "refreshes": True,
        "max_chapters": 20,
        "watermark": False,
        "commercial_use": True,
        "white_label": True,
        "description": "25 client books/month, white-label exports and client commercial rights.",
    },
}

PLAN_ORDER = ["free", "creator", "publisher", "agency"]
_PAID_PLANS = [p for p in PLAN_ORDER if PLANS[p]["price_usd"] > 0]


def purchasable_plans():
    return list(_PAID_PLANS)


def plan_info(plan_key):
    return PLANS.get(plan_key, PLANS["free"])


def can_generate(user):
    return user["credits"] > 0


def consume_credit(user):
    models.decrement_credit(user["id"])


def max_chapters_for(user):
    return plan_info(user["plan"])["max_chapters"]


def watermark_for(user):
    return plan_info(user["plan"])["watermark"]


def ensure_credits_fresh(user):
    """Resets a paid user's credits to their plan's monthly allotment once
    the reset date has passed. Free plan credits never refresh — it's a
    one-time trial, not a monthly grant. Returns the (possibly updated)
    user row.
    """
    plan = plan_info(user["plan"])
    if not plan["refreshes"]:
        return user
    reset_at = user["credits_reset_at"]
    now = datetime.now(timezone.utc)
    needs_reset = not reset_at or now >= datetime.fromisoformat(reset_at)
    if not needs_reset:
        return user
    next_reset = (now + timedelta(days=30)).isoformat()
    models.set_user_credits(user["id"], plan["monthly_credits"], next_reset)
    return models.get_user_by_id(user["id"])


def stripe_enabled():
    return bool(os.environ.get("STRIPE_SECRET_KEY"))


def _price_id_for(plan_key):
    return os.environ.get(f"STRIPE_PRICE_ID_{plan_key.upper()}")


def start_upgrade(user, plan_key, success_url, cancel_url):
    """Returns a URL to send the browser to in order to upgrade to `plan_key`.

    With Stripe configured (secret key + a price ID for this plan): a
    Stripe-hosted Checkout Session URL — the plan flips over only once the
    webhook confirms payment (see `process_webhook`). Without it: flips the
    plan immediately (demo mode) and returns `success_url` directly, so the
    button still works before real payment credentials exist.
    """
    if plan_key not in _PAID_PLANS:
        raise ValueError(f"Not a purchasable plan: {plan_key}")
    price_id = _price_id_for(plan_key)
    if not stripe_enabled() or not price_id:
        upgrade_to_plan(user["id"], plan_key)
        return success_url
    return stripe_client.create_checkout_session(
        api_key=os.environ["STRIPE_SECRET_KEY"],
        price_id=price_id,
        customer_email=user["email"],
        client_reference_id=user["id"],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"plan": plan_key},
    )


def upgrade_to_plan(user_id, plan_key):
    plan = plan_info(plan_key)
    next_reset = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    models.set_user_plan(user_id, plan_key, credits=plan["monthly_credits"], credits_reset_at=next_reset)


def handle_checkout_completed(session):
    user_id = session.get("client_reference_id")
    plan_key = (session.get("metadata") or {}).get("plan")
    if user_id and plan_key in PLANS:
        upgrade_to_plan(int(user_id), plan_key)


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
