import os
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.export_utils import export_epub, export_pdf  # noqa: E402

CHAPTERS = [
    {"title": "Getting Started", "content": "Paragraph one.\n\nParagraph two with more text."},
    {"title": "Going Deeper", "content": "Another chapter of prose to test pagination and wrapping."},
]
COVER_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>'


class ExportEpubTests(unittest.TestCase):
    def test_epub_is_valid_zip_with_mimetype_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "book.epub")
            export_epub(path, "My Title", "Author", "business", CHAPTERS, COVER_SVG)

            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
                self.assertEqual(names[0], "mimetype")
                self.assertEqual(zf.read("mimetype").decode(), "application/epub+zip")
                self.assertIn("OEBPS/content.opf", names)
                self.assertIn("OEBPS/nav.xhtml", names)
                self.assertIn("OEBPS/chapter1.xhtml", names)
                self.assertIn("OEBPS/chapter2.xhtml", names)

                chapter1 = zf.read("OEBPS/chapter1.xhtml").decode()
                self.assertIn("Getting Started", chapter1)
                self.assertIn("Paragraph one.", chapter1)

    def test_epub_escapes_user_content(self):
        chapters = [{"title": "<b>Bold</b> & Co", "content": "Some <script>alert(1)</script> text."}]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "book.epub")
            export_epub(path, "Title", "Author", "business", chapters, COVER_SVG)
            with zipfile.ZipFile(path) as zf:
                chapter1 = zf.read("OEBPS/chapter1.xhtml").decode()
                self.assertNotIn("<script>", chapter1)
                self.assertIn("&lt;script&gt;", chapter1)


class ExportPdfTests(unittest.TestCase):
    def test_pdf_is_valid_and_nonempty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "book.pdf")
            export_pdf(path, "My Title", "Author", "business", CHAPTERS)
            with open(path, "rb") as f:
                data = f.read()
            self.assertTrue(data.startswith(b"%PDF-1.4"))
            self.assertTrue(data.rstrip().endswith(b"%%EOF"))
            self.assertIn(b"/Type /Catalog", data)
            self.assertIn(b"/Type /Pages", data)

    def test_pdf_handles_many_chapters_multi_page(self):
        chapters = [
            {"title": f"Chapter {i}", "content": "Lorem ipsum dolor sit amet. " * 200}
            for i in range(1, 6)
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "book.pdf")
            export_pdf(path, "Long Book", "Author", "business", chapters)
            with open(path, "rb") as f:
                data = f.read()
            # Several /Type /Page objects (not /Pages) should exist for a long book.
            self.assertGreater(data.count(b"/Type /Page "), 3)


if __name__ == "__main__":
    unittest.main()
