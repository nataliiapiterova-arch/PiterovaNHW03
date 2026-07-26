import os
import sqlite3
import threading

# Override with EBOOK_STUDIO_DATA_DIR to point at a mounted volume in
# production (container filesystems are ephemeral — without this, the DB,
# generated files, and session-signing key reset on every deploy/restart).
DATA_DIR = os.environ.get("EBOOK_STUDIO_DATA_DIR") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)
DB_PATH = os.path.join(DATA_DIR, "ebook_studio.db")
COVERS_DIR = os.path.join(DATA_DIR, "covers")
EXPORTS_DIR = os.path.join(DATA_DIR, "exports")

_local = threading.local()

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    plan TEXT NOT NULL DEFAULT 'free',
    credits INTEGER NOT NULL DEFAULT 1,
    credits_reset_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    genre TEXT NOT NULL,
    num_chapters INTEGER NOT NULL,
    goal TEXT NOT NULL DEFAULT 'sell_product',
    cta_type TEXT,
    cta_target TEXT,
    author_name TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    error TEXT,
    cover_svg_path TEXT,
    epub_path TEXT,
    pdf_path TEXT,
    profit_path_json TEXT,
    marketing_json TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES books(id),
    idx INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
"""


def init_db(db_path=None):
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(COVERS_DIR, exist_ok=True)
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    conn = get_conn(db_path)
    conn.executescript(SCHEMA)
    conn.commit()


def get_conn(db_path=None):
    path = db_path or DB_PATH
    conn = getattr(_local, "conn", None)
    if conn is None or getattr(_local, "path", None) != path:
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        _local.conn = conn
        _local.path = path
    return conn
