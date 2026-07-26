"""Plan/credit gating for book generation.

No real payment processor is wired up here (no API keys available). This is
intentionally a stub with the extension point clearly marked, so a real
Stripe (or similar) checkout + webhook can replace `upgrade_to_pro` without
touching the rest of the app.
"""

from . import models

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


def upgrade_to_pro(user_id):
    """Stub upgrade path.

    TODO: replace this with a real Stripe Checkout Session + webhook
    handler before charging real customers. Today this just flips the
    plan so the rest of the product (unlimited generation) can be built
    and demoed end-to-end without payment credentials.
    """
    models.set_user_plan(user_id, "pro")
