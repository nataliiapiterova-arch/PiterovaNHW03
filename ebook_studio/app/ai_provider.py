"""Pluggable AI backend for content generation.

The app talks to whichever provider `get_provider()` returns, so swapping the
mock for a real LLM/image API later is a one-file change plus an env var.
"""

import hashlib
import os
import textwrap
from abc import ABC, abstractmethod

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
    def generate_outline(self, title, topic, genre, num_chapters):
        """Return a list of `num_chapters` chapter title strings."""

    @abstractmethod
    def generate_chapter(self, title, topic, genre, chapter_title, index, total):
        """Return the prose content (str) for one chapter."""

    @abstractmethod
    def generate_cover_svg(self, title, genre):
        """Return an SVG document (str) usable as a book cover."""


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

    def generate_cover_svg(self, title, genre):
        bg, accent = GENRE_PALETTES.get(genre.lower(), DEFAULT_PALETTE)
        safe_title = _escape_xml(title)
        lines = _wrap_title(title, 18)
        text_elements = "".join(
            f'<text x="300" y="{260 + i * 46}" font-size="34" font-family="Georgia, serif" '
            f'fill="#ffffff" text-anchor="middle" font-weight="bold">{_escape_xml(line)}</text>'
            for i, line in enumerate(lines)
        )
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900" viewBox="0 0 600 900">
  <rect width="600" height="900" fill="{bg}"/>
  <rect x="24" y="24" width="552" height="852" fill="none" stroke="{accent}" stroke-width="3"/>
  <circle cx="300" cy="150" r="60" fill="{accent}" opacity="0.85"/>
  {text_elements}
  <text x="300" y="820" font-size="20" font-family="Helvetica, Arial, sans-serif" fill="{accent}"
        text-anchor="middle" letter-spacing="4">{_escape_xml(genre.upper())}</text>
  <title>{safe_title}</title>
</svg>"""


class OpenAIProvider(AIProvider):
    """Real-LLM backed provider.

    TODO before enabling in production:
      1. `pip install openai` (or your preferred SDK) and add it to requirements.txt.
      2. Set OPENAI_API_KEY (and AI_PROVIDER=openai) in the environment.
      3. Implement each method below using chat completions for text and an
         image-generation endpoint for covers (or keep generate_cover_svg and
         only replace the two text methods, since SVG covers need no image API).
      4. Add retry/backoff and cost/rate limiting before exposing this to
         paying customers, since every call here is billed.
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "AI_PROVIDER=openai requires OPENAI_API_KEY to be set."
            )

    def generate_outline(self, title, topic, genre, num_chapters):
        raise NotImplementedError("Wire up a real chat-completions call here.")

    def generate_chapter(self, title, topic, genre, chapter_title, index, total):
        raise NotImplementedError("Wire up a real chat-completions call here.")

    def generate_cover_svg(self, title, genre):
        raise NotImplementedError("Wire up a real image-generation call here.")


def get_provider():
    name = os.environ.get("AI_PROVIDER", "mock").lower()
    if name == "mock":
        return MockAIProvider()
    if name == "openai":
        return OpenAIProvider()
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


def cover_seed(title):
    """Small helper kept for tests wanting a stable hash of a title."""
    return hashlib.sha256(title.encode("utf-8")).hexdigest()[:8]
