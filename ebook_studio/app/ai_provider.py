"""Pluggable AI backend for content generation.

The app talks to whichever provider `get_provider()` returns, so swapping the
mock for a real LLM/image API later is a one-file change plus an env var.
"""

import hashlib
import json
import os
import textwrap
from abc import ABC, abstractmethod

from .goals import goal_label, render_cta

GENRE_PALETTES = {
    "business": ("#0f172a", "#38bdf8"),
    "self-help": ("#1e1b4b", "#f472b6"),
    "finance": ("#052e16", "#4ade80"),
    "health": ("#082f49", "#22d3ee"),
    "technology": ("#111827", "#a78bfa"),
    "fiction": ("#3b0764", "#facc15"),
}
DEFAULT_PALETTE = ("#1f2937", "#f9fafb")


class AIProvider(ABC):
    @abstractmethod
    def generate_profit_path(self, topic, goal):
        """Return a dict describing the monetization angle for `topic`
        before any book content is written — the "how could this make
        money" preview shown ahead of generation. Prices are suggestions,
        never guarantees.
        """

    @abstractmethod
    def generate_outline(self, title, topic, genre, num_chapters):
        """Return a list of `num_chapters` chapter title strings."""

    @abstractmethod
    def generate_chapter(self, title, topic, genre, chapter_title, index, total):
        """Return the prose content (str) for one chapter."""

    @abstractmethod
    def generate_cover_svg(self, title, genre, watermark=False):
        """Return an SVG document (str) usable as a book cover."""

    @abstractmethod
    def generate_marketing_package(self, title, topic, genre, goal, author_name, cta_type, cta_target):
        """Return the sales + monetization package: product description,
        sales page, FAQ, promo emails/social posts/video scripts, channel
        recommendations, repurposing plan, and book front-matter fields
        (subtitle, author bio, disclaimer).
        """


class MockAIProvider(AIProvider):
    """Deterministic, offline stand-in for a real LLM/image API.

    Produces topic-aware placeholder text so the full pipeline (outline ->
    chapters -> cover -> export) can be built, tested, and demoed without any
    API keys. Swap in a real provider via AI_PROVIDER=openai once keys exist.
    """

    _CHAPTER_ANGLES = [
        "Understanding the Fundamentals of {topic}",
        "Why {topic} Matters Right Now",
        "Common Mistakes People Make with {topic}",
        "A Step-by-Step Approach to {topic}",
        "Tools and Techniques for {topic}",
        "Real-World Examples of {topic} in Action",
        "Building a Long-Term Plan Around {topic}",
        "Advanced Strategies for {topic}",
        "Troubleshooting Problems with {topic}",
        "Putting {topic} into Practice",
        "Measuring Progress with {topic}",
        "The Future of {topic}",
    ]

    def generate_profit_path(self, topic, goal):
        title_guess = f"The {topic.title()} Blueprint" if len(topic) < 40 else topic.split(",")[0].title()
        return {
            "title": title_guess,
            "audience": f"People who want practical, no-fluff help with {topic}.",
            "format_suggestion": "A focused 25-40 page guide plus a companion checklist or worksheet.",
            "price_low": 17,
            "price_high": 27,
            "upgrades": [
                "Editable template or worksheet bundle",
                "Checklist pack for quick reference",
                "Private community or email support add-on",
            ],
            "sales_channels": ["Payhip", "Gumroad", "TikTok", "Pinterest", "relevant online communities"],
            "lead_opportunity": "Offer the first chapter or a short checklist for free in exchange for an email address.",
            "affiliate_ideas": [
                f"Tools and software related to {topic}",
                "Scheduling or booking software",
                "Relevant insurance or compliance services",
            ],
        }

    def generate_outline(self, title, topic, genre, num_chapters):
        chapters = []
        for i in range(num_chapters):
            template = self._CHAPTER_ANGLES[i % len(self._CHAPTER_ANGLES)]
            chapters.append(template.format(topic=topic))
        return chapters

    def generate_chapter(self, title, topic, genre, chapter_title, index, total):
        paragraphs = [
            f"In this chapter, we explore \"{chapter_title}\", a key part of "
            f"understanding {topic}. Chapter {index} of {total} builds on what "
            f"came before and lays the groundwork for what follows.",
            f"When it comes to {topic}, most people underestimate how much "
            f"consistency matters more than intensity. This section breaks down "
            f"the core ideas behind {chapter_title.lower()} into steps you can "
            f"actually apply this week, not just concepts to admire.",
            f"Consider a simple example: someone starting from scratch with "
            f"{topic}. By focusing on {chapter_title.lower()}, they avoid the "
            f"most common trap in this genre of {genre} writing — spending all "
            f"their energy on theory and none on action.",
            "Key takeaways from this chapter:\n"
            f"- Start small and build momentum around {topic}.\n"
            f"- Revisit \"{chapter_title}\" regularly as your circumstances change.\n"
            "- Track one metric that tells you whether you're actually improving.",
        ]
        return "\n\n".join(textwrap.fill(p, width=88) for p in paragraphs)

    def generate_cover_svg(self, title, genre, watermark=False):
        bg, accent = GENRE_PALETTES.get(genre.lower(), DEFAULT_PALETTE)
        safe_title = _escape_xml(title)
        lines = _wrap_title(title, 18)
        text_elements = "".join(
            f'<text x="300" y="{260 + i * 46}" font-size="34" font-family="Georgia, serif" '
            f'fill="#ffffff" text-anchor="middle" font-weight="bold">{_escape_xml(line)}</text>'
            for i, line in enumerate(lines)
        )
        watermark_element = (
            '<text x="300" y="450" font-size="48" font-family="Helvetica, Arial, sans-serif" '
            'fill="#ffffff" fill-opacity="0.18" text-anchor="middle" '
            'transform="rotate(-30 300 450)" font-weight="bold">FREE PREVIEW</text>'
            if watermark else ""
        )
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900" viewBox="0 0 600 900">
  <rect width="600" height="900" fill="{bg}"/>
  <rect x="24" y="24" width="552" height="852" fill="none" stroke="{accent}" stroke-width="3"/>
  <circle cx="300" cy="150" r="60" fill="{accent}" opacity="0.85"/>
  {text_elements}
  <text x="300" y="820" font-size="20" font-family="Helvetica, Arial, sans-serif" fill="{accent}"
        text-anchor="middle" letter-spacing="4">{_escape_xml(genre.upper())}</text>
  {watermark_element}
  <title>{safe_title}</title>
</svg>"""

    def generate_marketing_package(self, title, topic, genre, goal, author_name, cta_type, cta_target):
        byline = author_name or "the author"
        cta_text = render_cta(cta_type, cta_target)
        goal_word = goal_label(goal)
        social_posts = [
            f"New guide: {title}. If you're dealing with {topic}, this walks you through it step by step.",
            f"Most people get {topic} wrong in the same three ways. I wrote {title} to fix that.",
            f"Spent weeks putting together everything I know about {topic} into one guide: {title}.",
            f"\"{title}\" is live. Practical, no filler, built for people who want to actually act on {topic}.",
            f"If {topic} has been on your mind, {title} is the shortcut I wish I'd had.",
            f"Behind the scenes: why I wrote {title} and who it's for.",
        ]
        promo_emails = [
            {
                "subject": f"It's here: {title}",
                "body": (
                    f"Hey — {title} is officially out. If {topic} is something you've been meaning to "
                    f"tackle, this gives you a clear, practical path through it. {cta_text}"
                ),
            },
            {
                "subject": f"Why I wrote {title}",
                "body": (
                    f"I kept seeing the same mistakes around {topic}, so I put together everything I've "
                    f"learned into one guide. {cta_text}"
                ),
            },
            {
                "subject": "Last call",
                "body": (
                    f"Quick reminder that {title} is available now. Grab it before you forget. {cta_text}"
                ),
            },
        ]
        video_scripts = [
            {
                "title": f"3 mistakes people make with {topic}",
                "script": (
                    f"Hook: Most people get {topic} wrong before they even start. Body: walk through the "
                    f"top 3 mistakes covered in {title}, one sentence each. Close: {cta_text}"
                ),
            },
            {
                "title": f"What's inside {title}",
                "script": (
                    f"Hook: Here's exactly what you get in {title}. Body: preview 3 chapter takeaways. "
                    f"Close: {cta_text}"
                ),
            },
            {
                "title": "Behind the scenes",
                "script": (
                    f"Hook: Why I wrote a book about {topic}. Body: the gap I saw and how {title} fills "
                    f"it. Close: {cta_text}"
                ),
            },
        ]
        faq = [
            {"q": "Who is this for?", "a": f"Anyone who wants a practical, step-by-step path through {topic}."},
            {"q": "How long is it?", "a": "A focused guide, not padded filler — built to be read and used."},
            {"q": "Do I need prior experience?", "a": "No — it starts from the basics and builds up."},
            {"q": "What format do I get?", "a": "EPUB and PDF, so it works on any device or e-reader."},
            {"q": "Is this a one-time purchase?", "a": "Yes — you own it once you buy it."},
        ]
        calendar_activities = [
            "Post a quote or takeaway from the book on social media.",
            "Send an email to your list highlighting one chapter.",
            "Share a short video clip based on the video script pack.",
            "Reach out to a relevant community or forum with a helpful post (not a sales pitch).",
            "Offer the lead-magnet version to a new audience segment.",
            "Ask an early reader for a testimonial or review.",
            "Pitch a podcast or newsletter for a guest mention.",
            "Run a limited-time bundle offer with a related product.",
            "Repost a promotional asset with fresh framing.",
            "Review analytics and double down on whatever channel is converting.",
        ]
        promo_calendar = [
            f"Day {i + 1}: {calendar_activities[i % len(calendar_activities)]}" for i in range(30)
        ]
        disclaimer = (
            f"This book shares general information and personal perspective on {topic}. It is not "
            "professional, legal, financial, or medical advice — consult a qualified professional for "
            "guidance specific to your situation. Results mentioned are illustrative, not guaranteed."
            if goal != "publish_fiction" else ""
        )
        return {
            "subtitle": f"A practical guide to {topic}",
            "author_bio": f"{byline} wrote this book to turn hard-won experience with {topic} into a "
                           "clear, usable guide for readers starting from scratch.",
            "disclaimer": disclaimer,
            "product_description": (
                f"{title} is a practical, no-fluff guide to {topic} — built for readers who want to "
                f"take action, not just read theory. Goal: {goal_word.lower()}."
            ),
            "price_low": 17,
            "price_high": 27,
            "sales_page": (
                f"# {title}\n\n"
                f"## Finally, a straightforward guide to {topic}\n\n"
                f"If you've felt stuck or overwhelmed by {topic}, this book gives you a clear, "
                "step-by-step path — no jargon, no padding, just what actually works.\n\n"
                "### What you'll get\n"
                "- A complete, structured guide you can read in one sitting\n"
                "- Practical steps you can apply immediately\n"
                "- A resource you can come back to as a reference\n\n"
                f"### Who it's for\n{topic.capitalize()} can feel complicated — this book breaks it down "
                "for real people with real constraints.\n\n"
                f"{cta_text}"
            ),
            "checkout_description": f"A practical, step-by-step guide to {topic}. Instant EPUB/PDF download.",
            "faq": faq,
            "promo_emails": promo_emails,
            "social_posts": social_posts,
            "video_scripts": video_scripts,
            "channels": ["Payhip", "Gumroad", "Amazon KDP", "your own website", "email list", "social media"],
            "lead_magnet_note": f"Offer the first chapter or a short checklist from {title} as a free "
                                 "opt-in to grow your email list before asking for a sale.",
            "upsells": [
                "Editable template or worksheet bundle",
                "1:1 coaching or consultation add-on",
                "Private community access",
            ],
            "bundles": [
                f"Bundle {title} with a checklist or template pack",
                "Bundle with a related guide as a 'starter kit'",
            ],
            "affiliates": [
                f"Tools and software related to {topic}",
                "Scheduling or booking software",
                "Relevant insurance or compliance services",
            ],
            "repurposing_plan": [
                "5-7 blog posts, one per major chapter theme",
                "A welcome email sequence for new subscribers",
                "10-15 social posts pulled from key takeaways",
                "3 short video scripts covering the most actionable chapters",
                "A condensed slide deck for a workshop or webinar",
            ],
            "promo_calendar": promo_calendar,
            "cta_text": cta_text,
        }


class ClaudeProvider(AIProvider):
    """Real Claude-backed provider (Anthropic API).

    Not runnable in this sandbox: the `anthropic` package can't be installed
    here (no PyPI access) and there's no API key configured. The code below
    is complete and ready to go once both exist elsewhere:
      1. `pip install anthropic` (already in requirements.txt).
      2. Set ANTHROPIC_API_KEY and AI_PROVIDER=claude in the environment.
    """

    MODEL = "claude-opus-5"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "AI_PROVIDER=claude requires ANTHROPIC_API_KEY to be set."
            )
        import anthropic

        self._anthropic = anthropic
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_profit_path(self, topic, goal):
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=2048,
            thinking={"type": "adaptive"},
            output_config={
                "effort": "medium",
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "audience": {"type": "string"},
                            "format_suggestion": {"type": "string"},
                            "price_low": {"type": "integer"},
                            "price_high": {"type": "integer"},
                            "upgrades": {"type": "array", "items": {"type": "string"}},
                            "sales_channels": {"type": "array", "items": {"type": "string"}},
                            "lead_opportunity": {"type": "string"},
                            "affiliate_ideas": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": [
                            "title", "audience", "format_suggestion", "price_low", "price_high",
                            "upgrades", "sales_channels", "lead_opportunity", "affiliate_ideas",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            messages=[{
                "role": "user",
                "content": (
                    f"A user wants to turn this idea into a digital ebook product, with the goal of "
                    f"\"{goal_label(goal)}\": {topic}\n\n"
                    "Analyze how this could make money as a short practical ebook. Suggest a working "
                    "title, target-reader profile, a realistic format (length + companion assets), a "
                    "suggested price RANGE in USD (not a guarantee), 2-4 possible paid upgrades, the "
                    "best sales channels for this niche, one concrete free-lead-magnet idea, and 2-3 "
                    "realistic affiliate-product categories related to the topic. Be concrete and "
                    "specific to the topic, not generic."
                ),
            }],
        )
        text = next(b.text for b in response.content if b.type == "text")
        return json.loads(text)

    def generate_outline(self, title, topic, genre, num_chapters):
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=4096,
            thinking={"type": "adaptive"},
            output_config={
                "effort": "medium",
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "chapters": {
                                "type": "array",
                                "items": {"type": "string"},
                            }
                        },
                        "required": ["chapters"],
                        "additionalProperties": False,
                    },
                },
            },
            messages=[{
                "role": "user",
                "content": (
                    f"Write a chapter-title outline for a {genre} ebook titled "
                    f"\"{title}\" about {topic}. Produce exactly {num_chapters} "
                    "chapter titles, in reading order, each a short descriptive "
                    "phrase (no numbering)."
                ),
            }],
        )
        text = next(b.text for b in response.content if b.type == "text")
        chapters = json.loads(text)["chapters"]
        # The schema can't enforce exact array length, so pad/trim deterministically.
        if len(chapters) < num_chapters:
            chapters += [f"Chapter {i}" for i in range(len(chapters) + 1, num_chapters + 1)]
        return chapters[:num_chapters]

    def generate_chapter(self, title, topic, genre, chapter_title, index, total):
        with self.client.messages.stream(
            model=self.MODEL,
            max_tokens=4096,
            thinking={"type": "adaptive"},
            output_config={"effort": "medium"},
            messages=[{
                "role": "user",
                "content": (
                    f"Write chapter {index} of {total} for the {genre} ebook "
                    f"\"{title}\" (topic: {topic}). This chapter is titled "
                    f"\"{chapter_title}\". Write 500-900 words of prose in "
                    "well-formed paragraphs separated by blank lines. Do not "
                    "repeat the chapter title in the body."
                ),
            }],
        ) as stream:
            final = stream.get_final_message()
        if final.stop_reason == "refusal":
            raise RuntimeError(f"Content generation was declined for chapter {index}.")
        return next(b.text for b in final.content if b.type == "text")

    def generate_cover_svg(self, title, genre, watermark=False):
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=2048,
            thinking={"type": "adaptive"},
            output_config={"effort": "low"},
            messages=[{
                "role": "user",
                "content": (
                    f"Design a book cover as a single self-contained SVG, "
                    f"600x900 viewBox, for a {genre} ebook titled \"{title}\". "
                    "Use flat shapes and web-safe fonts only (no external "
                    "assets, no <image>, no <script>). Respond with only the "
                    "raw <svg>...</svg> markup, nothing else."
                ),
            }],
        )
        if response.stop_reason == "refusal":
            raise RuntimeError("Cover generation was declined.")
        text = next(b.text for b in response.content if b.type == "text").strip()
        if not text.startswith("<svg"):
            # Fall back to the deterministic template rather than ship bad markup.
            return MockAIProvider().generate_cover_svg(title, genre, watermark=watermark)
        return _insert_before_closing_svg(text, _watermark_fragment()) if watermark else text

    def generate_marketing_package(self, title, topic, genre, goal, author_name, cta_type, cta_target):
        cta_text = render_cta(cta_type, cta_target)
        byline = author_name or "the author"
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=8192,
            thinking={"type": "adaptive"},
            output_config={
                "effort": "medium",
                "format": {
                    "type": "json_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "subtitle": {"type": "string"},
                            "author_bio": {"type": "string"},
                            "disclaimer": {"type": "string"},
                            "product_description": {"type": "string"},
                            "price_low": {"type": "integer"},
                            "price_high": {"type": "integer"},
                            "sales_page": {"type": "string"},
                            "checkout_description": {"type": "string"},
                            "faq": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {"q": {"type": "string"}, "a": {"type": "string"}},
                                    "required": ["q", "a"],
                                    "additionalProperties": False,
                                },
                            },
                            "promo_emails": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {"subject": {"type": "string"}, "body": {"type": "string"}},
                                    "required": ["subject", "body"],
                                    "additionalProperties": False,
                                },
                            },
                            "social_posts": {"type": "array", "items": {"type": "string"}},
                            "video_scripts": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {"title": {"type": "string"}, "script": {"type": "string"}},
                                    "required": ["title", "script"],
                                    "additionalProperties": False,
                                },
                            },
                            "channels": {"type": "array", "items": {"type": "string"}},
                            "lead_magnet_note": {"type": "string"},
                            "upsells": {"type": "array", "items": {"type": "string"}},
                            "bundles": {"type": "array", "items": {"type": "string"}},
                            "affiliates": {"type": "array", "items": {"type": "string"}},
                            "repurposing_plan": {"type": "array", "items": {"type": "string"}},
                            "promo_calendar": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": [
                            "subtitle", "author_bio", "disclaimer", "product_description", "price_low",
                            "price_high", "sales_page", "checkout_description", "faq", "promo_emails",
                            "social_posts", "video_scripts", "channels", "lead_magnet_note", "upsells",
                            "bundles", "affiliates", "repurposing_plan", "promo_calendar",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            messages=[{
                "role": "user",
                "content": (
                    f"Build the full sales and monetization package for a {genre} ebook titled "
                    f"\"{title}\" about {topic}, written by {byline}. The author's goal is: "
                    f"{goal_label(goal)}.\n\n"
                    "Produce: a one-line subtitle; a short author bio (2-3 sentences); a disclaimer "
                    "paragraph if this is practical/business/health/financial advice content (empty "
                    "string if this is fiction or clearly doesn't need one); a 1-2 sentence product "
                    "description; a suggested USD price range (a realistic suggestion, not a "
                    "guarantee); a long-form sales page (markdown headings ok); a short checkout-page "
                    "description; 5 FAQ entries; 3 promotional emails (subject+body); 6 short social "
                    "media posts; 3 short video scripts (title+script outline); a list of recommended "
                    "sales channels; one lead-magnet idea derived from this book; 2-4 upsell ideas; "
                    "1-2 bundle ideas; 2-3 realistic affiliate-product categories; a repurposing plan "
                    "(5-7 items: blog posts, emails, social posts, video scripts, etc.); and a 30-item "
                    "day-by-day promotion calendar (one short action per day).\n\n"
                    f"If a call-to-action is provided, weave it naturally into the sales page and "
                    f"promotional emails: \"{cta_text}\"" if cta_text else
                    "There is no specific call-to-action for this book; focus purely on selling the "
                    "book itself."
                ),
            }],
        )
        if response.stop_reason == "refusal":
            raise RuntimeError("Marketing package generation was declined.")
        text = next(b.text for b in response.content if b.type == "text")
        data = json.loads(text)
        data["cta_text"] = cta_text
        return data


def get_provider():
    name = os.environ.get("AI_PROVIDER", "mock").lower()
    if name == "mock":
        return MockAIProvider()
    if name == "claude":
        return ClaudeProvider()
    raise ValueError(f"Unknown AI_PROVIDER: {name}")


def _escape_xml(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _wrap_title(title, width):
    return textwrap.wrap(title, width=width) or [title]


def _watermark_fragment():
    return (
        '<text x="300" y="450" font-size="48" font-family="Helvetica, Arial, sans-serif" '
        'fill="#ffffff" fill-opacity="0.18" text-anchor="middle" '
        'transform="rotate(-30 300 450)" font-weight="bold">FREE PREVIEW</text>'
    )


def _insert_before_closing_svg(svg, fragment):
    idx = svg.rfind("</svg>")
    return svg if idx == -1 else svg[:idx] + fragment + svg[idx:]


def cover_seed(title):
    """Small helper kept for tests wanting a stable hash of a title."""
    return hashlib.sha256(title.encode("utf-8")).hexdigest()[:8]
