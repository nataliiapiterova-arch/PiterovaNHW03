# properebooks.com — Turn an idea into a sellable digital product

Not "AI writes you an ebook." The product is: pick a goal (sell a product,
generate leads, attract clients, build authority, create content faster,
or build for a client), see a **Profit Path** — a suggested title, audience,
price range, and sales channels — *before* spending a credit, then get a
complete launch package: the book (EPUB/PDF + cover), a sales package
(product description, sales page, FAQ, checkout copy), and a monetization
package (channels, lead-magnet version, upsells, affiliate ideas, a 30-day
promotion calendar). This is the MVP, built to run end-to-end with **zero
external services or paid API keys**, so it can be demoed today and wired
up to real AI/billing later.

## Why this product

Ebook-market research (mid-2026) points at AI-assisted publishing tools as a
growing category in their own right — but "generate an ebook" is a feature,
not an outcome. Most people don't want an ebook file; they want what the
ebook produces: sales, leads, authority, or an asset to sell to clients.
properebooks.com starts every generation with "what do you want this to
accomplish?" and tailors the whole output — not just the book — to that
goal. Monetization is a fixed, generous monthly credit allotment per plan
(never "unlimited" — a single complete book, sales package, and monetization
package can use meaningful AI resources, so an unlimited plan is a real
cost-abuse risk, not just a pricing nicety).

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
- **Goal-first flow** (`app/goals.py`): 7 goals (sell a product, generate
  leads, attract clients, build authority, create content, publish fiction,
  create for a client) drive the whole generation — which extra assets get
  produced, whether a CTA page/fields show up, and the "launch destination"
  options shown after generation.
- **AI generation**: pluggable `AIProvider` interface (`app/ai_provider.py`),
  with four methods: `generate_profit_path` (the pre-generation "how could
  this make money?" preview), `generate_outline`/`generate_chapter` (the
  book), `generate_cover_svg` (with an optional watermark for the Free
  plan), and `generate_marketing_package` (sales page, FAQ, promo emails,
  social posts, video scripts, channels, upsells, affiliates, repurposing
  plan, 30-day promo calendar, author bio, disclaimer). `MockAIProvider` is
  the default — deterministic, topic-aware placeholder content, no network
  calls. `ClaudeProvider` is a complete, ready-to-run implementation against
  the Anthropic API (`claude-opus-5`, structured-output JSON for the
  profit path and marketing package, streamed chapter text, refusal
  handling) — it just can't run *in this sandbox*, since neither the
  `anthropic` package nor an `ANTHROPIC_API_KEY` are available here. Switch
  providers with the `AI_PROVIDER` env var (`mock` | `claude`).
- **Export**: EPUB is assembled directly as a zip per the EPUB3 spec
  (`zipfile`, no `ebooklib`); PDF is a small hand-rolled writer using the
  built-in Helvetica fonts with WinAnsi encoding (`app/export_utils.py`, no
  `reportlab`).
- **Billing**: `app/billing.py` gates generation by plan/credits (**no
  unlimited tier** — Free/Creator/Publisher/Agency each get a fixed monthly
  credit allotment; Free is a one-time grant, paid plans refresh monthly via
  `ensure_credits_fresh`), and drives real Stripe Checkout + webhook handling
  (`app/stripe_client.py` — hand-rolled against Stripe's plain REST API and
  HMAC webhook signing, no `stripe` package needed). Without
  `STRIPE_SECRET_KEY` set (or a price ID for the specific plan), upgrading
  falls back to an instant demo-mode flip so the product still works
  end-to-end before payment credentials exist.

## Running it

No `pip install` is required for the mock/demo path (Jinja2 is the only
dependency and is already present in most Python environments; see
`requirements.txt` if you need to install it):

```bash
cd ebook_studio
python3 server.py
# open http://127.0.0.1:8000
```

Sign up, pick a goal ("What do you want your ebook to accomplish?"),
describe the topic, and you'll see a **Profit Path** preview — suggested
title, audience, price range, and sales channels — before anything is
generated. Click "Build This Product" and the app generates the book in a
background thread (usually instant with the mock
provider) and lets you download the EPUB/PDF once it's done.

### Environment variables

| Variable       | Default | Purpose                                             |
|----------------|---------|------------------------------------------------------|
| `HOST`/`PORT`  | `127.0.0.1` / `8000` | dev server bind address (`server.py` / local only — Railway's gunicorn process reads `$PORT` itself) |
| `AI_PROVIDER`  | `mock`  | `mock` or `claude`                                    |
| `ANTHROPIC_API_KEY` | —  | required if `AI_PROVIDER=claude`                      |
| `SECRET_KEY`   | auto-generated, persisted to `data/secret.key` | session-signing key — **set this explicitly in production** (see below) |
| `EBOOK_STUDIO_DATA_DIR` | `ebook_studio/data` | where the SQLite DB, covers, exports, and `secret.key` live — **point this at a persistent volume in production** |
| `STRIPE_SECRET_KEY` | — | your Stripe secret key; unset = demo-mode instant upgrade instead of real Checkout |
| `STRIPE_PRICE_ID_CREATOR` | — | Stripe Price ID for the $19/mo Creator plan |
| `STRIPE_PRICE_ID_PUBLISHER` | — | Stripe Price ID for the $49/mo Publisher plan |
| `STRIPE_PRICE_ID_AGENCY` | — | Stripe Price ID for the $99/mo Agency plan |
| `STRIPE_WEBHOOK_SECRET` | — | signing secret for the `checkout.session.completed` webhook (see below) |

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
   - Leave `STRIPE_*` unset to launch with demo-mode instant upgrades, or set
     all three (see **Stripe setup** below) for real billing.
5. Deploy, then generate a public domain (Settings → Networking → Generate
   Domain). Railway builds via Nixpacks (detects Python from
   `requirements.txt`) and starts the `web` process from the `Procfile`.

**Known limitation at this stage**: SQLite works fine for an MVP but doesn't
scale to concurrent writers under real traffic — see the production-hardening
list below for when to move off it (e.g. to Postgres).

### Stripe setup (optional — demo mode works without it)

1. Create a Stripe account and, in the Dashboard, create three Products
   (Creator $19/mo, Publisher $49/mo, Agency $99/mo), each with a recurring
   Price. Copy each Price's ID (`price_...`) into `STRIPE_PRICE_ID_CREATOR`
   / `STRIPE_PRICE_ID_PUBLISHER` / `STRIPE_PRICE_ID_AGENCY`. You can set up
   just one tier to start — the others fall back to demo mode individually
   if their price ID is missing.
2. Copy your **secret key** (Developers → API keys) into `STRIPE_SECRET_KEY`.
3. Add a webhook endpoint (Developers → Webhooks) pointing at
   `https://<your-railway-domain>/billing/webhook`, subscribed to the
   `checkout.session.completed` event. Copy its **signing secret**
   (`whsec_...`) into `STRIPE_WEBHOOK_SECRET`.
4. Redeploy (or just wait for the env vars to apply) — the "Upgrade to
   Creator/Publisher/Agency" buttons now redirect to a real Stripe Checkout
   page for that plan, and the plan only flips over once Stripe confirms
   payment via the webhook, not on click.

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

- **Real**: auth, sessions, CSRF protection, SQLite persistence, the goal
  picker, the Profit Path preview (free — no credit spent), the full
  generation pipeline (outline → chapters → front matter → optional CTA
  page → cover → marketing package → export) and background-job status
  polling, valid EPUB3 and PDF file output (including the generated front
  matter/CTA content), per-user ownership checks on every route, the sales
  + monetization package rendered on the book detail page, the free-plan
  watermarked cover, monthly credit refresh for paid plans, and Stripe
  Checkout + webhook billing across all three paid tiers. `ClaudeProvider`
  is real code too — it's just unexercised here for lack of network access
  and a key, not a `NotImplementedError` stub.
- **Demo-mode fallback (not a stub, a deliberate degrade path)**: without
  `STRIPE_SECRET_KEY` (or a price ID for a specific plan), upgrading to that
  plan flips instantly instead of redirecting to Stripe, so the product
  still works end-to-end before payment credentials exist.
- **Deliberately not implemented** (honestly labeled "not available yet" on
  the book detail page's launch-destination panel, not faked): audiobook
  creation (needs text-to-speech), translation (needs a translation
  pipeline), and one-click upsell/revised-edition generation. Also not
  implemented: real Amazon KDP/Gumroad/Payhip API integration — the app
  generates the content and copy for those (and a KDP submission checklist)
  but doesn't call their APIs to actually publish/list anything; mockup
  product images; and the promo calendar/repurposing plan are generated
  text, not scheduled/automated posting.

## Next steps to take this to production

1. `pip install anthropic`, set `ANTHROPIC_API_KEY` and `AI_PROVIDER=claude`,
   and smoke-test `ClaudeProvider` end-to-end (it hasn't run against the real
   API yet — written to the Claude API skill's current conventions, but
   unverified outside this sandbox).
2. Set up a real Stripe account/Prices/webhook (see **Stripe setup** above) —
   the integration code is done and tested (signature verification, demo
   fallback, webhook handling for all 3 tiers), just not yet exercised
   against live Stripe.
3. ~~Move off `wsgiref.simple_server` to a production WSGI server~~ — done:
   `Procfile` runs gunicorn. Still worth putting a real reverse proxy/CDN in
   front once traffic justifies it.
4. Add rate limiting on generation to bound LLM API cost per user.
5. Move off SQLite once concurrent writes become a bottleneck (a Postgres
   add-on is a one-click add in Railway) — fine for the MVP, not for scale.
6. Build real integrations for the "not available yet" launch-destination
   items (audiobook TTS, translation, direct KDP/Gumroad/Payhip publishing
   via their APIs) if usage shows demand for them.
