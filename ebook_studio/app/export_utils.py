"""EPUB and PDF export built entirely on the standard library.

No PyPI packages (ebooklib, reportlab, ...) are available in this
environment, so EPUB is assembled directly as a zip archive per the OCF/EPUB3
spec, and PDF is written with a small hand-rolled generator using the
standard 14 built-in fonts (no font embedding needed).
"""

import html
import textwrap
import uuid
import zipfile


# ---------------------------------------------------------------------------
# EPUB
# ---------------------------------------------------------------------------

def export_epub(path, title, author, genre, chapters, cover_svg):
    """chapters: list of {"title": str, "content": str} in reading order."""
    book_uuid = str(uuid.uuid4())
    manifest_items = []
    spine_items = []
    chapter_files = []

    for i, chapter in enumerate(chapters, start=1):
        filename = f"chapter{i}.xhtml"
        chapter_files.append((filename, _chapter_xhtml(chapter["title"], chapter["content"])))
        manifest_items.append(
            f'<item id="chap{i}" href="{filename}" media-type="application/xhtml+xml"/>'
        )
        spine_items.append(f'<itemref idref="chap{i}"/>')

    nav_xhtml = _nav_xhtml(title, chapters)
    content_opf = _content_opf(book_uuid, title, author, manifest_items, spine_items)

    with zipfile.ZipFile(path, "w") as zf:
        # mimetype must be the first entry, stored uncompressed.
        zf.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", zipfile.ZIP_STORED)
        zf.writestr("META-INF/container.xml", _CONTAINER_XML)
        zf.writestr("OEBPS/content.opf", content_opf)
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml)
        zf.writestr("OEBPS/cover.svg", cover_svg)
        for filename, content in chapter_files:
            zf.writestr(f"OEBPS/{filename}", content)
    return path


_CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def _content_opf(book_uuid, title, author, manifest_items, spine_items):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">urn:uuid:{book_uuid}</dc:identifier>
    <dc:title>{html.escape(title)}</dc:title>
    <dc:creator>{html.escape(author)}</dc:creator>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="cover" href="cover.svg" media-type="image/svg+xml"/>
    {''.join(manifest_items)}
  </manifest>
  <spine>
    {''.join(spine_items)}
  </spine>
</package>
"""


def _nav_xhtml(title, chapters):
    links = "".join(
        f'<li><a href="chapter{i}.xhtml">{html.escape(c["title"])}</a></li>'
        for i, c in enumerate(chapters, start=1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>{html.escape(title)}</title></head>
<body>
  <nav epub:type="toc"><h1>{html.escape(title)}</h1><ol>{links}</ol></nav>
</body>
</html>
"""


def _chapter_xhtml(title, content):
    paragraphs = "".join(
        f"<p>{html.escape(p).replace(chr(10), '<br/>')}</p>"
        for p in content.split("\n\n")
        if p.strip()
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{html.escape(title)}</title></head>
<body>
  <h1>{html.escape(title)}</h1>
  {paragraphs}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

class SimplePDF:
    """Minimal single-column text PDF writer using the built-in Helvetica fonts."""

    PAGE_WIDTH = 612
    PAGE_HEIGHT = 792
    MARGIN = 54
    BODY_SIZE = 11
    BODY_LEADING = 15
    TITLE_SIZE = 20

    def __init__(self):
        self._pages = []  # list of list of (text, font_key, size)
        self._new_page()

    def _new_page(self):
        self._pages.append([])
        self._y = self.PAGE_HEIGHT - self.MARGIN

    def _ensure_space(self, needed):
        if self._y - needed < self.MARGIN:
            self._new_page()

    def add_heading(self, text):
        self._ensure_space(self.TITLE_SIZE + self.BODY_LEADING)
        self._pages[-1].append((text, "F2", self.TITLE_SIZE, self._y))
        self._y -= self.TITLE_SIZE + 10

    def add_paragraphs(self, text):
        max_chars = int((self.PAGE_WIDTH - 2 * self.MARGIN) / (self.BODY_SIZE * 0.5))
        for para in text.split("\n\n"):
            para = para.strip()
            if not para:
                continue
            for line in textwrap.wrap(para, width=max(max_chars, 20)):
                self._ensure_space(self.BODY_LEADING)
                self._pages[-1].append((line, "F1", self.BODY_SIZE, self._y))
                self._y -= self.BODY_LEADING
            self._y -= self.BODY_LEADING * 0.5  # paragraph gap

    def add_page_break(self):
        self._new_page()

    def save(self, path):
        objects = []  # list of bytes, index 0 unused; objects[i] is object (i+1)

        def add_object(body_bytes):
            objects.append(body_bytes)
            return len(objects)

        font_f1_num = None
        font_f2_num = None
        page_obj_nums = []
        content_obj_nums = []

        # Reserve numbers: 1=Catalog, 2=Pages, 3=F1, 4=F2, then contents+pages.
        catalog_num = 1
        pages_num = 2
        objects.append(b"")  # placeholder for catalog
        objects.append(b"")  # placeholder for pages
        # WinAnsiEncoding (~cp1252) so smart punctuation like em dashes,
        # which the mock/LLM text can contain, has a renderable glyph.
        font_f1_num = add_object(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        )
        font_f2_num = add_object(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        )

        for page_lines in self._pages:
            stream = self._render_content_stream(page_lines)
            stream_bytes = (
                f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1")
                + stream
                + b"\nendstream"
            )
            content_num = add_object(stream_bytes)
            content_obj_nums.append(content_num)

        for content_num in content_obj_nums:
            page_body = (
                f"<< /Type /Page /Parent {pages_num} 0 R "
                f"/MediaBox [0 0 {self.PAGE_WIDTH} {self.PAGE_HEIGHT}] "
                f"/Resources << /Font << /F1 {font_f1_num} 0 R /F2 {font_f2_num} 0 R >> >> "
                f"/Contents {content_num} 0 R >>"
            ).encode("latin-1")
            page_num = add_object(page_body)
            page_obj_nums.append(page_num)

        kids = " ".join(f"{n} 0 R" for n in page_obj_nums)
        objects[pages_num - 1] = (
            f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_nums)} >>"
        ).encode("latin-1")
        objects[catalog_num - 1] = f"<< /Type /Catalog /Pages {pages_num} 0 R >>".encode(
            "latin-1"
        )

        buf = bytearray(b"%PDF-1.4\n")
        offsets = [0]
        for i, body in enumerate(objects, start=1):
            offsets.append(len(buf))
            buf += f"{i} 0 obj\n".encode("latin-1") + body + b"\nendobj\n"

        xref_offset = len(buf)
        buf += f"xref\n0 {len(offsets)}\n".encode("latin-1")
        buf += b"0000000000 65535 f \n"
        for off in offsets[1:]:
            buf += f"{off:010d} 00000 n \n".encode("latin-1")
        buf += (
            f"trailer\n<< /Size {len(offsets)} /Root {catalog_num} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF"
        ).encode("latin-1")

        with open(path, "wb") as f:
            f.write(buf)
        return path

    @staticmethod
    def _pdf_escape(text):
        return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

    def _render_content_stream(self, lines):
        # Each line sets an absolute text matrix (Tm) rather than the
        # cursor-relative Td, since Td offsets accumulate from the previous
        # line's position and would drift the layout badly here.
        parts = [b"BT"]
        for text, font_key, size, y in lines:
            escaped = self._pdf_escape(text)
            parts.append(f"/{font_key} {size} Tf".encode("ascii"))
            parts.append(f"1 0 0 1 {self.MARGIN} {y:.2f} Tm".encode("ascii"))
            # cp1252 (~WinAnsiEncoding): covers em dashes/curly quotes that
            # plain latin-1/ascii can't; anything further out degrades to '?'.
            parts.append(b"(" + escaped.encode("cp1252", errors="replace") + b") Tj")
        parts.append(b"ET")
        return b"\n".join(parts)


def export_pdf(path, title, author, genre, chapters):
    pdf = SimplePDF()
    pdf.add_heading(title)
    pdf.add_paragraphs(f"by {author}    |    genre: {genre}")
    pdf.add_page_break()
    for chapter in chapters:
        pdf.add_heading(chapter["title"])
        pdf.add_paragraphs(chapter["content"])
        pdf.add_page_break()
    pdf.save(path)
    return path
