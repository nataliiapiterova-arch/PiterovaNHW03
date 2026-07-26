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

        chapters = models.list_chapters(book_id)
        self.assertEqual(len(chapters), 3)

    def test_generate_book_marks_failed_on_error(self):
        user_id = models.create_user("fail@example.com", "hash", "salt")
        book_id = models.create_book(user_id, "Broken Book", "topic", "business", 3)
        os.environ["AI_PROVIDER"] = "openai"  # requires OPENAI_API_KEY -> raises
        os.environ.pop("OPENAI_API_KEY", None)

        _generate_book(book_id)

        book = models.get_book(book_id)
        self.assertEqual(book["status"], "failed")
        self.assertIsNotNone(book["error"])
        os.environ["AI_PROVIDER"] = "mock"


if __name__ == "__main__":
    unittest.main()
