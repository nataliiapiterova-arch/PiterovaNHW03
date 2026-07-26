# properebooks.com — AI Ebook Studio

A SaaS product concept for properebooks.com: users sign up, describe a topic,
and get a full AI-generated ebook back — outline, chapter text, a cover, and
downloadable EPUB/PDF files. This is the MVP, built to run end-to-end with
**zero external services or paid API keys**, so it can be demoed today and
wired up to a real LLM later.

## Why this product

Ebook-market research (mid-2026) points at AI-assisted publishing tools as a
growing category in their own right — creators want to generate a catalog of
niche titles quickly rather than write one book slowly. Rather than selling
ebooks, this app sells the *generation tool itself*, with a free tier (1 book)
and a Pro tier (unlimited) as the monetization hook.

## Stack

Deliberately dependency-light — this environment has no PyPI access, so
everything runs on the Python standard library plus **Jinja2** for templates
(no third-party auth, web framework, PDF, EPUB, or image library):

- **Web layer**: hand-rolled WSGI router (`app/wsgi_app.py`) — no Flask/
  FastAPI available in this sandbox. `server.py` serves it with
  `wsgiref.simple_server` for local dev; the `Procfile` serves the same
  `app.wsgi_app:app` callable with gunicorn in production (e.g. on Railway).
- **Auth**: PBKDF2-SHA256 password hashing + a small stdlib-only signed
  session-cookie scheme (`app/tokens.py`) — PyJWT was dropped because its
  `cryptography` dependency's native extension doesn't load on this box's
  Python version; sessions only ever need HMAC-SHA256, which `hmac`/`hashlib`
  already provide.
- **Storage**: SQLite via `sqlite3` (`app/database.py`, `app/models.py`).
- **AI generation**: pluggable `AIProvider` interface (`app/ai_provider.py`).
  `MockAIProvider` is the default — deterministic, topic-aware placeholder
  text and an SVG cover, no network calls. `ClaudeProvider` is a complete,
  ready-to-run implementation against the Anthropic API (`claude-opus-5`,
  structured-output outline generation, streamed chapter text, refusal
  handling) — it just can't run *in this sandbox*, since neither the
  `anthropic` package nor an `ANTHROPIC_API_KEY` are available here. Switch
  providers with the `AI_PROVIDER` env var (`mock` | `claude`).
- **Export**: EPUB is assembled directly as a zip per the EPUB3 spec
  (`zipfile`, no `ebooklib`); PDF is a small hand-rolled writer using the
  built-in Helvetica fonts with WinAnsi encoding (`app/export_utils.py`, no
  `reportlab`).
- **Billing**: `app/billing.py` gates generation by plan/credits. Upgrading
  to Pro is a stub that just flips the plan in the DB — there's no payment
  processor wired up. The TODO for swapping in real Stripe Checkout +
  webhooks is marked inline.

## Running it

No `pip install` is required for the mock/demo path (Jinja2 is the only
dependency and is already present in most Python environments; see
`requirements.txt` if you need to install it):

```bash
cd ebook_studio
python3 server.py
# open http://127.0.0.1:8000
```

Sign up, click "New book", fill in a title/topic/genre, and the app
generates the book in a background thread (usually instant with the mock
provider) and lets you download the EPUB/PDF once it's done.

### Environment variables

| Variable       | Default | Purpose                                             |
|----------------|---------|------------------------------------------------------|
| `HOST`/`PORT`  | `127.0.0.1` / `8000` | dev server bind address (`server.py` / local only — Railway's gunicorn process reads `$PORT` itself) |
| `AI_PROVIDER`  | `mock`  | `mock` or `claude`                                    |
| `ANTHROPIC_API_KEY` | —  | required if `AI_PROVIDER=claude`                      |
| `SECRET_KEY`   | auto-generated, persisted to `data/secret.key` | session-signing key — **set this explicitly in production** (see below) |
| `EBOOK_STUDIO_DATA_DIR` | `ebook_studio/data` | where the SQLite DB, covers, exports, and `secret.key` live — **point this at a persistent volume in production** |

## Deploying on Railway

The app ships with a `Procfile` (gunicorn, reading `$PORT`) and a `requirements.txt`
Railway's Nixpacks builder can use directly — no Dockerfile needed.

1. Push this repo to GitHub (already done on this branch) and create a new
   Railway project from it.
2. In the service's **Settings**, set **Root Directory** to `ebook_studio` —
   Railway then builds/runs from that subfolder and picks up its `Procfile`
   and `requirements.txt` automatically.
3. **Attach a volume** (Settings → Volumes), mount path e.g. `/data`. Without
   this, the container filesystem is wiped on every deploy/restart — that
   means the SQLite DB (all users and books), generated covers/exports, and
   the session-signing key all reset. With the volume attached, set the env
   var `EBOOK_STUDIO_DATA_DIR=/data` (see table above) so the app writes
   there instead of its default in-repo `data/` folder.
4. Set environment variables (Settings → Variables):
   - `SECRET_KEY` — a random 64-char hex string (e.g. `python3 -c "import secrets; print(secrets.token_hex(32))"`).
     Setting this explicitly (rather than relying on the auto-generated
     `secret.key` file) means sessions survive redeploys even without the
     volume.
   - `AI_PROVIDER=mock` to launch immediately with placeholder book content,
     or `AI_PROVIDER=claude` + `ANTHROPIC_API_KEY=<your key>` for real
     AI-generated books.
5. Deploy, then generate a public domain (Settings → Networking → Generate
   Domain). Railway builds via Nixpacks (detects Python from
   `requirements.txt`) and starts the `web` process from the `Procfile`.

**Known limitation at this stage**: SQLite works fine for an MVP but doesn't
scale to concurrent writers under real traffic — see the production-hardening
list below for when to move off it (e.g. to Postgres).

## Tests

`pytest` isn't installed in this sandbox either, so tests use `unittest`:

```bash
cd ebook_studio
python3 -m unittest discover -s tests -v
```

Covers password hashing/session round-trips, credit gating, the full
outline → chapters → cover → export pipeline, and that the generated
EPUB/PDF files are structurally valid (and that user-supplied text is
properly escaped, not just concatenated, when it ends up in generated
XHTML/PDF).

## What's a stub vs. real

- **Real**: auth, sessions, CSRF protection, SQLite persistence, the full
  generation pipeline and background-job status polling, valid EPUB3 and PDF
  file output, per-user ownership checks on every book/download route.
- **Stub (clearly marked with TODOs in code)**: `billing.upgrade_to_pro` (no
  real payment processor). `ClaudeProvider` is real code, not a stub — it's
  just unexercised here for lack of network access and a key.

## Next steps to take this to production

1. `pip install anthropic`, set `ANTHROPIC_API_KEY` and `AI_PROVIDER=claude`,
   and smoke-test `ClaudeProvider` end-to-end (it hasn't run against the real
   API yet — written to the Claude API skill's current conventions, but
   unverified outside this sandbox).
2. Replace the billing stub with real Stripe Checkout + webhook handling.
3. ~~Move off `wsgiref.simple_server` to a production WSGI server~~ — done:
   `Procfile` runs gunicorn. Still worth putting a real reverse proxy/CDN in
   front once traffic justifies it.
4. Add rate limiting on generation to bound LLM API cost per user.
5. Move off SQLite once concurrent writes become a bottleneck (a Postgres
   add-on is a one-click add in Railway) — fine for the MVP, not for scale.
