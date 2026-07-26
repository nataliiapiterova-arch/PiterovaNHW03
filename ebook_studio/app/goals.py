"""Catalog of "what do you want this ebook to accomplish?" goals.

The selected goal drives generation: which extra assets get produced
(sales page vs. opt-in copy vs. consultation CTA), the tone of the book
itself, and what the post-generation "launch destination" screen offers.
"""

GOALS = {
    "sell_product": {
        "label": "Sell it as a digital product",
        "short_label": "Sell a digital product",
        "outcome": "I have a finished product I can start selling.",
        "needs_cta": False,
        "needs_white_label": False,
    },
    "build_list": {
        "label": "Generate leads",
        "short_label": "Build my email list",
        "outcome": "I have a lead magnet that grows my audience.",
        "needs_cta": True,
        "needs_white_label": False,
    },
    "attract_clients": {
        "label": "Attract clients",
        "short_label": "Attract clients",
        "outcome": "The ebook explains my expertise and helps convert readers into clients.",
        "needs_cta": True,
        "needs_white_label": False,
    },
    "build_authority": {
        "label": "Build my authority",
        "short_label": "Build authority",
        "outcome": "I become a published author with a professional book attached to my name or brand.",
        "needs_cta": False,
        "needs_white_label": False,
    },
    "create_content": {
        "label": "Create content for my audience",
        "short_label": "Create content faster",
        "outcome": "One idea gives me weeks of content.",
        "needs_cta": False,
        "needs_white_label": False,
    },
    "publish_fiction": {
        "label": "Publish fiction",
        "short_label": "Publish fiction",
        "outcome": "A complete story, ready to publish.",
        "needs_cta": False,
        "needs_white_label": False,
    },
    "client_project": {
        "label": "Create a book for a client",
        "short_label": "Create for a client",
        "outcome": "I can sell ebook and lead-magnet creation as a service.",
        "needs_cta": True,
        "needs_white_label": True,
    },
}

GOAL_ORDER = [
    "sell_product",
    "build_list",
    "attract_clients",
    "build_authority",
    "create_content",
    "publish_fiction",
    "client_project",
]

CTA_OPTIONS = [
    ("consultation", "Schedule a consultation"),
    ("estimate", "Request an estimate"),
    ("mailing_list", "Join a mailing list"),
    ("purchase", "Purchase a service"),
    ("website", "Visit a website"),
    ("social", "Follow a social account"),
]

CTA_LABELS = dict(CTA_OPTIONS)


def goal_label(key):
    return GOALS.get(key, {}).get("short_label", key)


def needs_cta(key):
    return GOALS.get(key, {}).get("needs_cta", False)


_CTA_TEMPLATES = {
    "consultation": "Ready to talk it through? Schedule a free consultation: {target}",
    "estimate": "Want to know what this would cost? Request an estimate: {target}",
    "mailing_list": "Want more like this? Join the mailing list: {target}",
    "purchase": "Ready to get started? {target}",
    "website": "Learn more and see what's next: {target}",
    "social": "Keep up with new content and updates: {target}",
}


def render_cta(cta_type, cta_target):
    """Renders a plain-language call-to-action sentence for the book's
    final page. Falls back to a generic phrasing if the type/target are
    missing so the page never renders as empty or broken.
    """
    if not cta_type or not cta_target:
        return ""
    template = _CTA_TEMPLATES.get(cta_type, "Get in touch: {target}")
    return template.format(target=cta_target)
