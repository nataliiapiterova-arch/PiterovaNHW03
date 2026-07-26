"""Tiny WSGI application: routing, cookies, templates, forms.

No web framework is installable in this environment (no PyPI access), so
this hand-rolled router covers exactly what the product needs: GET/POST
routes with path params, signed-cookie sessions, CSRF-protected forms,
Jinja2 rendering, and safe static/file serving.
"""

import json
import mimetypes
import os
import re
from http import cookies as http_cookies
from urllib.parse import parse_qs

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import auth, billing, models
from .ai_provider import get_provider
from .database import init_db
from .generation import start_generation
from .goals import CTA_OPTIONS, GOAL_ORDER, GOALS, needs_cta

APP_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")
STATIC_DIR = os.path.join(APP_DIR, "static")

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)

_ROUTES = []  # list of (method, compiled_regex, param_names, handler)


def route(path, methods=("GET",)):
    param_names = re.findall(r"<(\w+)>", path)
    pattern = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path)
    compiled = re.compile(f"^{pattern}$")

    def decorator(fn):
        for method in methods:
            _ROUTES.append((method, compiled, param_names, fn))
        return fn

    return decorator


class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ["REQUEST_METHOD"]
        self.path = environ.get("PATH_INFO", "/")
        self.query = parse_qs(environ.get("QUERY_STRING", ""))
        self._form = None
        self.cookies = http_cookies.SimpleCookie()
        raw_cookie = environ.get("HTTP_COOKIE")
        if raw_cookie:
            self.cookies.load(raw_cookie)
        self.user = None
        self.csrf_token = None

    @property
    def form(self):
        if self._form is None:
            try:
                length = int(self.environ.get("CONTENT_LENGTH") or 0)
            except ValueError:
                length = 0
            body = self.environ["wsgi.input"].read(length) if length else b""
            self._form = {
                k: v[0] for k, v in parse_qs(body.decode("utf-8")).items()
            }
        return self._form

    def cookie(self, name):
        morsel = self.cookies.get(name)
        return morsel.value if morsel else None


class Response:
    def __init__(self, body="", status="200 OK", headers=None, content_type="text/html; charset=utf-8"):
        self.body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.status = status
        self.headers = headers or []
        self.headers.append(("Content-Type", content_type))

    def set_cookie(self, name, value, http_only=True, max_age=None):
        parts = [f"{name}={value}", "Path=/", "SameSite=Lax"]
        if http_only:
            parts.append("HttpOnly")
        if max_age is not None:
            parts.append(f"Max-Age={max_age}")
        self.headers.append(("Set-Cookie", "; ".join(parts)))


def redirect(location, status="302 Found"):
    return Response("", status=status, headers=[("Location", location)])


def not_found():
    return Response("<h1>404 Not Found</h1>", status="404 Not Found")


def render(request, template_name, **context):
    template = jinja_env.get_template(template_name)
    context.setdefault("user", request.user)
    context.setdefault("csrf_token", request.csrf_token)
    context.setdefault("plans", billing.PLANS)
    return Response(template.render(**context))


def require_login(request):
    """Returns a redirect Response if not logged in, else None."""
    if request.user is None:
        return redirect("/login")
    return None


def check_csrf(request):
    submitted = request.form.get("csrf_token")
    return submitted and request.csrf_token and submitted == request.csrf_token


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@route("/")
def landing(request):
    return render(request, "landing.html")


@route("/pricing")
def pricing(request):
    return render(request, "pricing.html", stripe_enabled=billing.stripe_enabled())


@route("/signup", methods=("GET",))
def signup_form(request):
    if request.user:
        return redirect("/dashboard")
    return render(request, "signup.html", error=None)


@route("/signup", methods=("POST",))
def signup_submit(request):
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    try:
        user_id = auth.signup(email, password)
    except ValueError as exc:
        return render(request, "signup.html", error=str(exc))
    resp = redirect("/dashboard")
    resp.set_cookie(auth.SESSION_COOKIE_NAME, auth.create_session_token(user_id), max_age=auth.SESSION_TTL_SECONDS)
    return resp


@route("/login", methods=("GET",))
def login_form(request):
    if request.user:
        return redirect("/dashboard")
    return render(request, "login.html", error=None)


@route("/login", methods=("POST",))
def login_submit(request):
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    try:
        user = auth.login(email, password)
    except ValueError as exc:
        return render(request, "login.html", error=str(exc))
    resp = redirect("/dashboard")
    resp.set_cookie(auth.SESSION_COOKIE_NAME, auth.create_session_token(user["id"]), max_age=auth.SESSION_TTL_SECONDS)
    return resp


@route("/logout", methods=("POST",))
def logout(request):
    resp = redirect("/")
    resp.set_cookie(auth.SESSION_COOKIE_NAME, "", max_age=0)
    return resp


@route("/dashboard")
def dashboard(request):
    redirect_resp = require_login(request)
    if redirect_resp:
        return redirect_resp
    books = models.list_books_for_user(request.user["id"])
    return render(request, "dashboard.html", books=books, goals=GOALS)


@route("/books/new", methods=("GET",))
def new_book_form(request):
    redirect_resp = require_login(request)
    if redirect_resp:
        return redirect_resp
    return render(
        request, "new_book.html", error=None,
        goals=GOALS, goal_order=GOAL_ORDER, cta_options=CTA_OPTIONS,
        max_chapters=billing.max_chapters_for(request.user),
    )


def _new_book_form_kwargs(request, error):
    return dict(
        error=error, goals=GOALS, goal_order=GOAL_ORDER, cta_options=CTA_OPTIONS,
        max_chapters=billing.max_chapters_for(request.user),
    )


@route("/books/new", methods=("POST",))
def new_book_submit(request):
    """Step 1: turn a topic + goal into a "Profit Path" preview — no
    credit is spent yet. The user confirms (or edits the suggested title)
    on the next screen before generation actually starts.
    """
    redirect_resp = require_login(request)
    if redirect_resp:
        return redirect_resp
    if not check_csrf(request):
        return Response("<h1>403 Invalid CSRF token</h1>", status="403 Forbidden")

    user = request.user
    if not billing.can_generate(user):
        return render(request, "new_book.html", **_new_book_form_kwargs(
            request, "You're out of credits for this plan. Upgrade to generate more books."
        ))

    goal = request.form.get("goal", "sell_product").strip()
    if goal not in GOALS:
        goal = "sell_product"
    topic = request.form.get("topic", "").strip()
    title = request.form.get("title", "").strip()
    genre = request.form.get("genre", "self-help").strip()
    author_name = request.form.get("author_name", "").strip()
    cta_type = request.form.get("cta_type", "").strip() or None
    cta_target = request.form.get("cta_target", "").strip() or None
    if not needs_cta(goal):
        cta_type, cta_target = None, None
    try:
        num_chapters = int(request.form.get("num_chapters", "8"))
    except ValueError:
        num_chapters = 8
    num_chapters = max(3, min(num_chapters, billing.max_chapters_for(user)))

    if not topic:
        return render(request, "new_book.html", **_new_book_form_kwargs(
            request, "Tell us what the ebook is about."
        ))

    try:
        profit_path = get_provider().generate_profit_path(topic, goal)
    except RuntimeError as exc:
        return render(request, "new_book.html", **_new_book_form_kwargs(request, str(exc)))

    return render(
        request, "profit_path.html",
        profit_path=profit_path, goal=goal, goal_meta=GOALS[goal], topic=topic,
        title=title, genre=genre, num_chapters=num_chapters, author_name=author_name,
        cta_type=cta_type, cta_target=cta_target,
        profit_path_json=json.dumps(profit_path),
    )


@route("/books/confirm", methods=("POST",))
def new_book_confirm(request):
    """Step 2: the user clicked "Build This Product" — this is where a
    credit actually gets spent and generation kicks off.
    """
    redirect_resp = require_login(request)
    if redirect_resp:
        return redirect_resp
    if not check_csrf(request):
        return Response("<h1>403 Invalid CSRF token</h1>", status="403 Forbidden")

    user = request.user
    if not billing.can_generate(user):
        return render(request, "new_book.html", **_new_book_form_kwargs(
            request, "You're out of credits for this plan. Upgrade to generate more books."
        ))

    goal = request.form.get("goal", "sell_product").strip()
    if goal not in GOALS:
        goal = "sell_product"
    topic = request.form.get("topic", "").strip()
    genre = request.form.get("genre", "self-help").strip()
    author_name = request.form.get("author_name", "").strip() or None
    cta_type = request.form.get("cta_type", "").strip() or None
    cta_target = request.form.get("cta_target", "").strip() or None
    if not needs_cta(goal):
        cta_type, cta_target = None, None
    profit_path_json = request.form.get("profit_path_json", "")
    try:
        suggested_title = json.loads(profit_path_json).get("title", "") if profit_path_json else ""
    except (ValueError, AttributeError):
        suggested_title = ""
    title = request.form.get("title", "").strip() or suggested_title or topic[:80]
    try:
        num_chapters = int(request.form.get("num_chapters", "8"))
    except ValueError:
        num_chapters = 8
    num_chapters = max(3, min(num_chapters, billing.max_chapters_for(user)))

    if not topic:
        return render(request, "new_book.html", **_new_book_form_kwargs(
            request, "Tell us what the ebook is about."
        ))

    book_id = models.create_book(
        user["id"], title, topic, genre, num_chapters, goal=goal,
        cta_type=cta_type, cta_target=cta_target, author_name=author_name,
        profit_path_json=profit_path_json or None,
    )
    billing.consume_credit(user)
    start_generation(book_id)
    return redirect(f"/books/{book_id}")


KDP_CHECKLIST = [
    "Create (or sign in to) your Amazon KDP account at kdp.amazon.com.",
    "Upload the EPUB as your manuscript file.",
    "Upload the print-ready PDF cover, or use KDP's cover creator with the SVG as a reference.",
    "Set your title, subtitle, and author name to match the generated front matter.",
    "Paste the generated product description into the KDP book description field.",
    "Choose categories and keywords relevant to your topic.",
    "Set your price within KDP's royalty tiers (35% or 70%, depending on price and region).",
    "Preview with KDP's online reviewer before publishing.",
]


@route("/books/<book_id>")
def book_detail(request, book_id):
    redirect_resp = require_login(request)
    if redirect_resp:
        return redirect_resp
    book = models.get_book(book_id)
    if book is None or book["user_id"] != request.user["id"]:
        return not_found()
    chapters = models.list_chapters(book_id) if book["status"] == "complete" else []
    marketing = json.loads(book["marketing_json"]) if book["marketing_json"] else None
    profit_path = json.loads(book["profit_path_json"]) if book["profit_path_json"] else None
    return render(
        request, "book_detail.html", book=book, chapters=chapters,
        marketing=marketing, profit_path=profit_path, goal_meta=GOALS.get(book["goal"], {}),
        kdp_checklist=KDP_CHECKLIST,
    )


@route("/books/<book_id>/cover.svg")
def book_cover(request, book_id):
    redirect_resp = require_login(request)
    if redirect_resp:
        return redirect_resp
    book = models.get_book(book_id)
    if book is None or book["user_id"] != request.user["id"] or not book["cover_svg_path"]:
        return not_found()
    with open(book["cover_svg_path"], "rb") as f:
        return Response(f.read(), content_type="image/svg+xml")


@route("/books/<book_id>/download/<fmt>")
def book_download(request, book_id, fmt):
    redirect_resp = require_login(request)
    if redirect_resp:
        return redirect_resp
    book = models.get_book(book_id)
    if book is None or book["user_id"] != request.user["id"]:
        return not_found()
    path = book["epub_path"] if fmt == "epub" else book["pdf_path"] if fmt == "pdf" else None
    if not path or not os.path.exists(path):
        return not_found()
    content_type = "application/epub+zip" if fmt == "epub" else "application/pdf"
    with open(path, "rb") as f:
        data = f.read()
    safe_name = re.sub(r"[^\w\-]+", "_", book["title"])[:60] or "book"
    headers = [("Content-Disposition", f'attachment; filename="{safe_name}.{fmt}"')]
    return Response(data, headers=headers, content_type=content_type)


def _absolute_url(request, path):
    scheme = request.environ.get("HTTP_X_FORWARDED_PROTO", request.environ.get("wsgi.url_scheme", "http"))
    host = request.environ.get("HTTP_X_FORWARDED_HOST", request.environ.get("HTTP_HOST", "localhost"))
    return f"{scheme}://{host}{path}"


@route("/billing/upgrade", methods=("POST",))
def upgrade(request):
    redirect_resp = require_login(request)
    if redirect_resp:
        return redirect_resp
    if not check_csrf(request):
        return Response("<h1>403 Invalid CSRF token</h1>", status="403 Forbidden")
    plan_key = request.form.get("plan", "").strip()
    if plan_key not in billing.purchasable_plans():
        return render(request, "pricing.html", error="Unknown plan.", stripe_enabled=billing.stripe_enabled())
    success_url = _absolute_url(request, "/dashboard?upgraded=1")
    cancel_url = _absolute_url(request, "/pricing")
    try:
        target = billing.start_upgrade(request.user, plan_key, success_url, cancel_url)
    except (RuntimeError, ValueError) as exc:
        return render(request, "pricing.html", error=str(exc), stripe_enabled=True)
    return redirect(target)


@route("/billing/webhook", methods=("POST",))
def stripe_webhook(request):
    try:
        length = int(request.environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        length = 0
    payload = request.environ["wsgi.input"].read(length) if length else b""
    sig_header = request.environ.get("HTTP_STRIPE_SIGNATURE")
    if not billing.process_webhook(payload, sig_header):
        return Response("", status="400 Bad Request")
    return Response("", status="200 OK")


def serve_static(request, subpath):
    full_path = os.path.normpath(os.path.join(STATIC_DIR, subpath))
    if not full_path.startswith(STATIC_DIR) or not os.path.isfile(full_path):
        return not_found()
    content_type = mimetypes.guess_type(full_path)[0] or "application/octet-stream"
    with open(full_path, "rb") as f:
        return Response(f.read(), content_type=content_type)


# ---------------------------------------------------------------------------
# WSGI entrypoint
# ---------------------------------------------------------------------------

_db_initialized = False


def _ensure_db():
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True


def dispatch(environ):
    _ensure_db()
    request = Request(environ)

    if request.path.startswith("/static/"):
        return serve_static(request, request.path[len("/static/"):])

    user, csrf_token = auth.current_user_from_cookie(request.cookie(auth.SESSION_COOKIE_NAME))
    request.user = billing.ensure_credits_fresh(user) if user else None
    request.csrf_token = csrf_token

    for method, pattern, param_names, handler in _ROUTES:
        if method != request.method:
            continue
        match = pattern.match(request.path)
        if match:
            kwargs = {name: match.group(name) for name in param_names}
            return handler(request, **kwargs)

    return not_found()


def app(environ, start_response):
    response = dispatch(environ)
    start_response(response.status, response.headers)
    return [response.body]
