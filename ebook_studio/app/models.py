"""Thin data-access helpers around the sqlite3 tables defined in database.py."""

from .database import get_conn


# ---- users -----------------------------------------------------------------

def create_user(email, password_hash, salt):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO users (email, password_hash, salt) VALUES (?, ?, ?)",
        (email, password_hash, salt),
    )
    conn.commit()
    return cur.lastrowid


def get_user_by_email(email):
    conn = get_conn()
    return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()


def get_user_by_id(user_id):
    conn = get_conn()
    return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def set_user_plan(user_id, plan, credits=None, credits_reset_at=None):
    conn = get_conn()
    if credits is not None:
        conn.execute(
            "UPDATE users SET plan = ?, credits = ?, credits_reset_at = ? WHERE id = ?",
            (plan, credits, credits_reset_at, user_id),
        )
    else:
        conn.execute("UPDATE users SET plan = ? WHERE id = ?", (plan, user_id))
    conn.commit()


def set_user_credits(user_id, credits, credits_reset_at=None):
    conn = get_conn()
    conn.execute(
        "UPDATE users SET credits = ?, credits_reset_at = ? WHERE id = ?",
        (credits, credits_reset_at, user_id),
    )
    conn.commit()


def decrement_credit(user_id):
    conn = get_conn()
    conn.execute(
        "UPDATE users SET credits = credits - 1 WHERE id = ? AND credits > 0",
        (user_id,),
    )
    conn.commit()


# ---- books -------------------------------------------------------------

def create_book(
    user_id, title, topic, genre, num_chapters, goal="sell_product",
    cta_type=None, cta_target=None, author_name=None, profit_path_json=None,
):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO books (user_id, title, topic, genre, num_chapters, goal, "
        "cta_type, cta_target, author_name, profit_path_json, status) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')",
        (user_id, title, topic, genre, num_chapters, goal, cta_type, cta_target,
         author_name, profit_path_json),
    )
    conn.commit()
    return cur.lastrowid


def get_book(book_id):
    conn = get_conn()
    return conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()


def list_books_for_user(user_id):
    conn = get_conn()
    return conn.execute(
        "SELECT * FROM books WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()


def update_book_status(book_id, status, error=None):
    conn = get_conn()
    conn.execute(
        "UPDATE books SET status = ?, error = ? WHERE id = ?",
        (status, error, book_id),
    )
    conn.commit()


def update_book_outputs(book_id, cover_svg_path=None, epub_path=None, pdf_path=None):
    conn = get_conn()
    conn.execute(
        "UPDATE books SET cover_svg_path = ?, epub_path = ?, pdf_path = ? WHERE id = ?",
        (cover_svg_path, epub_path, pdf_path, book_id),
    )
    conn.commit()


def update_book_marketing(book_id, marketing_json):
    conn = get_conn()
    conn.execute(
        "UPDATE books SET marketing_json = ? WHERE id = ?",
        (marketing_json, book_id),
    )
    conn.commit()


# ---- chapters ----------------------------------------------------------

def add_chapter(book_id, idx, title, content):
    conn = get_conn()
    conn.execute(
        "INSERT INTO chapters (book_id, idx, title, content) VALUES (?, ?, ?, ?)",
        (book_id, idx, title, content),
    )
    conn.commit()


def list_chapters(book_id):
    conn = get_conn()
    return conn.execute(
        "SELECT * FROM chapters WHERE book_id = ? ORDER BY idx ASC", (book_id,)
    ).fetchall()
