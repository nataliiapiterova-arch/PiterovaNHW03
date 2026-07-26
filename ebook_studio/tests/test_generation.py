import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import database, models  # noqa: E402
from app.ai_provider import MockAIProvider  # noqa: E402
from app.generation import _generate_book  # noqa: E402


class MockProviderTests(unittest.TestCase):
    def test_outline_has_requested_chapter_count(self):
        provider = MockAIProvider()
        outline = provider.generate_outline("My Book", "gut health", "health", 5)
        self.assertEqual(len(outline), 5)
        self.assertTrue(all(isinstance(t, str) and t for t in outline))

    def test_chapter_mentions_topic(self):
        provider = MockAIProvider()
        content = provider.generate_chapter(
            "My Book", "gut health", "health", "Understanding Gut Health", 1, 5
        )
        self.assertIn("gut health", content)

    def test_cover_svg_is_well_formed_and_escaped(self):
        provider = MockAIProvider()
        svg = provider.generate_cover_svg('Title with <script> & "quotes"', "business")
        self.assertTrue(svg.startswith("<svg"))
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)

    def test_cover_svg_watermark_toggle(self):
        provider = MockAIProvider()
        plain = provider.generate_cover_svg("Title", "business")
        watermarked = provider.generate_cover_svg("Title", "business", watermark=True)
        self.assertNotIn("FREE PREVIEW", plain)
        self.assertIn("FREE PREVIEW", watermarked)

    def test_profit_path_has_expected_fields(self):
        provider = MockAIProvider()
        result = provider.generate_profit_path("starting a cleaning business", "sell_product")
        for key in ("title", "audience", "format_suggestion", "price_low", "price_high",
                    "upgrades", "sales_channels", "lead_opportunity", "affiliate_ideas"):
            self.assertIn(key, result)
        self.assertLess(result["price_low"], result["price_high"])

    def test_marketing_package_has_expected_fields_and_cta(self):
        provider = MockAIProvider()
        result = provider.generate_marketing_package(
            "The Guide", "gut health", "health", "attract_clients",
            "Jane Doe", "consultation", "https://example.com/book",
        )
        for key in ("subtitle", "author_bio", "disclaimer", "product_description", "price_low",
                    "price_high", "sales_page", "checkout_description", "faq", "promo_emails",
                    "social_posts", "video_scripts", "channels", "lead_magnet_note", "upsells",
                    "bundles", "affiliates", "repurposing_plan", "promo_calendar", "cta_text"):
            self.assertIn(key, result)
        self.assertEqual(len(result["promo_calendar"]), 30)
        self.assertIn("https://example.com/book", result["cta_text"])
        self.assertIn("Jane Doe", result["author_bio"])

    def test_marketing_package_fiction_has_no_disclaimer(self):
        provider = MockAIProvider()
        result = provider.generate_marketing_package(
            "A Novel", "a detective in space", "fiction", "publish_fiction", None, None, None,
        )
        self.assertEqual(result["disclaimer"], "")
        self.assertEqual(result["cta_text"], "")


class GenerationPipelineTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._orig_db_path = database.DB_PATH
        self._orig_covers_dir = database.COVERS_DIR
        self._orig_exports_dir = database.EXPORTS_DIR
        database.DB_PATH = os.path.join(self._tmpdir.name, "test.db")
        database.COVERS_DIR = os.path.join(self._tmpdir.name, "covers")
        database.EXPORTS_DIR = os.path.join(self._tmpdir.name, "exports")
        database._local.conn = None
        database.init_db()
        os.environ["AI_PROVIDER"] = "mock"

    def tearDown(self):
        database.DB_PATH = self._orig_db_path
        database.COVERS_DIR = self._orig_covers_dir
        database.EXPORTS_DIR = self._orig_exports_dir
        database._local.conn = None
        self._tmpdir.cleanup()

    def test_generate_book_end_to_end(self):
        user_id = models.create_user("gen@example.com", "hash", "salt")
        book_id = models.create_book(user_id, "Test Book", "productivity", "business", 3)

        _generate_book(book_id)

        book = models.get_book(book_id)
        self.assertEqual(book["status"], "complete")
        self.assertIsNone(book["error"])
        self.assertTrue(os.path.exists(book["cover_svg_path"]))
        self.assertTrue(os.path.exists(book["epub_path"]))
        self.assertTrue(os.path.exists(book["pdf_path"]))
        self.assertIsNotNone(book["marketing_json"])

        # 1 front-matter chapter ("About This Book") + 3 content chapters;
        # no CTA chapter since the default goal (sell_product) doesn't need one.
        chapters = models.list_chapters(book_id)
        self.assertEqual(len(chapters), 4)
        self.assertEqual(chapters[0]["title"], "About This Book")

    def test_generate_book_adds_cta_chapter_when_goal_needs_it(self):
        user_id = models.create_user("cta@example.com", "hash", "salt")
        book_id = models.create_book(
            user_id, "Client Guide", "hiring a contractor", "business", 3,
            goal="attract_clients", cta_type="consultation", cta_target="https://example.com/book",
        )

        _generate_book(book_id)

        book = models.get_book(book_id)
        self.assertEqual(book["status"], "complete")
        chapters = models.list_chapters(book_id)
        # front matter + 3 content chapters + CTA chapter
        self.assertEqual(len(chapters), 5)
        self.assertEqual(chapters[-1]["title"], "Take the Next Step")
        self.assertIn("https://example.com/book", chapters[-1]["content"])

    def test_generate_book_marks_failed_on_error(self):
        user_id = models.create_user("fail@example.com", "hash", "salt")
        book_id = models.create_book(user_id, "Broken Book", "topic", "business", 3)
        os.environ["AI_PROVIDER"] = "claude"  # requires ANTHROPIC_API_KEY -> raises
        os.environ.pop("ANTHROPIC_API_KEY", None)

        _generate_book(book_id)

        book = models.get_book(book_id)
        self.assertEqual(book["status"], "failed")
        self.assertIsNotNone(book["error"])
        os.environ["AI_PROVIDER"] = "mock"


if __name__ == "__main__":
    unittest.main()
