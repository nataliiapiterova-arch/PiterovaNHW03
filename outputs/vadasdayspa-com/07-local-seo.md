# Local SEO: Vada's Day Spa (2026-07-15)

> NEEDS DATA: GBP not connected in Windsor.ai. No `WINDSOR_API_KEY` is set, so this run
> could not pull the `google_my_business` connector: no native Google review list (so no
> per-review reply drafts for Google reviews), no review count or average rating from
> Google itself, no 90-day insights (impressions on Maps vs Search, calls, direction
> requests, website clicks), and no `search_keyword_value` terms. Connecting the GBP in
> Windsor.ai unlocks all of that read-only — Windsor never posts anything — and turns the
> review queue below into a real per-review approval list and the insights section into
> actual numbers. Everything below is built from public search evidence gathered in
> Wave 1 (2026-07-15) plus one attempted live search this run (search quota then
> exhausted). No metric below is invented; gaps are marked.

---

## GBP health

**Estimated profile health: 55 / 100** (qualitative — scored from public signals only;
the GBP dashboard itself was not readable this run).

What earns points: the profile appears claimed and active, the brand SERP is owned
(official site #1 for brand searches), hours are published and consistent in search
results, and the business ranks #1 organically for "day spa East Lansing MI" — proximity
and relevance signals are clearly working.

**Top 3 gaps, in order of value:**

1. **Entity fragmentation — five business-name variants across the web.** "Vada's Day
   Spa", "Vadas Day Spa", "Vada's Day Spa and Salon", "Vada's Day Spa and Beauty Salon",
   and "Vada Day Spa" all exist on live listings, plus two duplicate Facebook pages and
   two duplicate WellnessLiving listings, plus TripAdvisor filing the business under the
   wrong city (Lansing, not East Lansing) and Wheree filing it under the wrong category
   (Nail Salons). Google cross-checks GBP against these citations; every mismatch erodes
   the "near me" rankings the keyword map says this market runs on. This is the single
   most valuable fix in this file.
2. **Review equity stranded off-Google.** The strongest public review asset is a Birdeye
   aggregate of 4.6 stars / 128 reviews — but Birdeye is invisible to Google's local
   ranking and to AI assistants. Yelp shows only 12 reviews; the native Google count was
   not visible in search results this run and must be confirmed from the GBP dashboard.
   Meanwhile the top local competitor (Zoë Life) shows ~350 Google reviews at 4.9.
3. **Primary category unverified.** At least one directory (Wheree) already categorizes
   the business as a nail salon. If the GBP primary category is anything other than
   **"Day spa"**, every query in the keyword map's P1 clusters is handicapped. Two-minute
   check in the GBP dashboard; do it first.

## Insights snapshot

> NEEDS DATA: all of this section requires the Windsor.ai `google_my_business`
> connector. Once connected, this table fills from the last-90-days fields.

| Metric (last 90 days) | Value | Windsor field |
|---|---|---|
| Impressions — Google Search (desktop + mobile) | n/a | `impressions_desktop_search` + `impressions_mobile_search` |
| Impressions — Google Maps (desktop + mobile) | n/a | `impressions_desktop_maps` + `impressions_mobile_maps` |
| Calls from the profile | n/a | `calls` / `call_clicks` |
| Direction requests | n/a | `direction_requests` |
| Website clicks | n/a | `website_clicks` |
| Top search terms that surfaced the profile | n/a | `search_keyword_value` |

What we know from public data instead: the business already ranks #1 organic for
"day spa East Lansing MI" and top-3 for "spa packages Lansing MI", and its packages page
surfaces for spa-day-cost searches — so the profile is almost certainly earning
impressions on exactly the high-intent queries the client cares about. We just can't
count them yet.

## Review reply queue

**Public review footprint (verified sources, 2026-07-15 — do not quote beyond these):**

| Platform | Rating | Count | Status |
|---|---|---|---|
| Birdeye (aggregate) | 4.6 | 128 | Strong but invisible to Google/AI ranking |
| Chamber of Commerce | 4.7 | 88 | Name listed as "…and Salon" — NAP fix needed |
| BestProsInTown | n/a shown | 91 | — |
| Yelp | n/a shown | 12 | The platform AI assistants cite most; thinnest count |
| TripAdvisor | n/a shown | small count | Wrong city, wrong name, **one unanswered negative 2026 review** |
| Google (native) | unknown | unknown | > NEEDS DATA: confirm from GBP dashboard / Windsor |

**Google reviews:** cannot be read without the Windsor connection, so no Google reply
drafts exist this run. Once connected, every review with an empty `review_reply_comment`
gets a drafted reply queued here for approval.

### Queue item 1 — TripAdvisor negative review (2026), un-replied

- **Platform:** TripAdvisor ("Vada Day Spa", currently mis-filed under Lansing)
- **Stars / excerpt:** strongly negative; the only publicly visible fragment is the
  headline wording **"dishonest day spa"** (surfaced in Wave 1 search snippets). The
  full review text could not be retrieved this run (search quota exhausted; direct
  page fetches blocked).
- **Status: needs TripAdvisor access before the reply below can be finalized.** The
  draft addresses only the visible headline. Whoever posts it must first read the full
  review and adjust the specifics — never post a reply that ignores what the reviewer
  actually said.
- **Drafted reply (provisional — verify against full review text):**

  > Thank you for taking the time to share this, and I'm sorry your visit left you
  > feeling this way — that's not the experience we work for. Honesty matters to me
  > personally, and I'd like to understand exactly what happened so I can make it
  > right. Please call me directly at (517) 324-8770 or email vadasdayspa@gmail.com
  > and ask for Vada. — Vada, Owner, Vada's Day Spa

  - [ ] Approve (after reading the full review and adjusting)

  Notes on the draft: acknowledges without arguing, takes it offline with a real
  contact route, admits no liability, and comes from Vada by name (on-brand: the spa
  is personal and owner-led). While logged in to reply, also submit the two listing
  corrections (name → "Vada's Day Spa", city → East Lansing) — see Citations plan.

### Standing guidance for the human replying to reviews (until Windsor is connected)

- **Positive:** thank the reviewer for the specific thing they mentioned (the hot stone
  massage, the customized facial, the spa day with their daughter), mention the service
  and East Lansing naturally once, sign as Vada or "the Vada's Day Spa team". No keyword
  stuffing, no copy-paste replies.
- **Negative:** acknowledge, apologize for the experience (not for wrongdoing), move it
  offline to (517) 324-8770 or vadasdayspa@gmail.com, never argue publicly, never offer
  compensation in the public reply.
- **Rating-only (no text):** short warm thank-you; invite them back by name of a
  seasonal service.

## GBP post drafts

Four drafts for mid-July → mid-August 2026. Each is under 1,500 characters, uses the
keyword map's local modifiers (East Lansing MI primary; Lansing; near MSU; Okemos/
Haslett as service-area mentions), and follows brand voice (warm, personal, no
"discount"/"luxury" language). **Drafts only — a human publishes these in the GBP
dashboard.**

### Post 1 — Service spotlight: spa parties (the uncontested angle)

> **Planning a girls' spa day or bachelorette in East Lansing?**
>
> Some days are better shared. Vada's Day Spa specializes in private spa parties —
> book the spa for your group and spend the afternoon together over customized facials,
> relaxing massages, and spa manicures and pedicures. Bridal parties, birthdays,
> mother-daughter days, or just a long-overdue afternoon with your favorite people —
> we'll tailor the services to your group.
>
> We're at 740 W Lake Lansing Rd in East Lansing, minutes from Okemos, Haslett, and the
> MSU campus. Groups book up ahead of fall weekends, so if you have a date in mind,
> call us soon and we'll plan it together.

- **CTA:** Call — (517) 324-8770
- **Target URL:** https://vadasdayspa.com/ (switch to /spa-parties once the On-Page
  Copywriter's page exists — the GEO audit flags it as the fastest uncontested win)
- ~700 characters. [ ] Approve

### Post 2 — What's new: spa day packages, hour by hour

> **What's actually included in a spa day?**
>
> If you've never booked one, here's how a spa day at Vada's works. Our Pampering
> Package is about three hours: you'll start with a customized facial — Vada tailors it
> to your skin, not a set menu — then a relaxing full-body massage, and finish with a
> spa pedicure. Our Half-Day Package adds a spa manicure for the full four-hour reset.
>
> Packages run $160 to $240, which works out to less than booking each service
> separately — and you leave with an afternoon of it, not a rushed hour. Wear whatever
> is comfortable; we take care of the rest.
>
> Serving East Lansing, Lansing, Okemos, and Haslett since 2011.

- **CTA:** Book — https://vadasdayspa.com/spa-day-packages
- **Target URL:** https://vadasdayspa.com/spa-day-packages
- ~700 characters. [ ] Approve
- Note: verify package inclusions/prices against the live menu before publishing
  (client.md carries a CONFIRM on pricing).

### Post 3 — Service spotlight: hot stone vs. deep tissue massage

> **Hot stone or deep tissue — which massage do you need?**
>
> A question we hear all the time in East Lansing. Here's the short answer: deep tissue
> works out stubborn knots and tension — the choice after long weeks at a desk or hard
> workouts. Hot stone uses warmed stones to relax muscles gently and deeply — the choice
> when you want to fully unwind rather than work anything out. And if you're not sure,
> a Swedish massage is the relaxing middle ground.
>
> Tell us how you're feeling when you book and we'll match you with the right one.
> You'll leave relaxed either way — that part we can promise.

- **CTA:** Learn more — https://vadasdayspa.com/massages
- **Target URL:** https://vadasdayspa.com/massages
- ~650 characters. [ ] Approve
- Note: doubles as support for the keyword map's #1 visible gap ("massage east lansing").

### Post 4 — Offer/occasion: MSU move-in and gift certificates

> **MSU move-in is coming — treat yourself, or someone who earned it.**
>
> August in East Lansing means campus fills back up. If you're a parent dropping a
> student off, book yourself a relaxing massage or a spa day package before the drive
> home — we're 10 minutes from campus on Lake Lansing Road. If you know someone starting
> a stressful semester (or surviving one), a Vada's gift certificate turns into a
> customized facial, a massage, or a full spa day whenever they need it most.
>
> We've been East Lansing's day spa since 2011. Saturdays around move-in weekend fill
> early — call ahead and we'll hold your spot.

- **CTA:** Call — (517) 324-8770
- **Target URL:** https://vadasdayspa.com/
- ~640 characters. [ ] Approve
- Note: confirm gift certificates are sold directly (a third-party Giverrang listing
  exists; the keyword map recommends an on-site gift card page).

## Profile fixes

In fix order. Items 1–4 are dashboard checks the owner can do in one sitting.

1. [ ] **Verify primary category is "Day spa"** — not "Nail salon", not "Beauty salon".
   Add secondary categories: Massage spa, Facial spa, Nail salon, Waxing hair removal
   service, Permanent make-up clinic (each maps to a real service).
2. [ ] **Confirm the business name field is exactly "Vada's Day Spa"** — no "and Salon",
   no "and Beauty Salon", no descriptors (descriptors in the GBP name also violate
   Google's guidelines).
3. [ ] **Resolve the suite number once, then enforce it** — GBP address should read
   740 W Lake Lansing Rd #300 (or drop #300 everywhere; client.md carries the CONFIRM).
   Whatever the answer, the GBP, the website footer, and every citation must match.
4. [ ] **Confirm native Google review count and rating** and read/reply to any
   un-replied Google reviews (queue above takes over once Windsor is connected).
5. [ ] **Website field:** https://vadasdayspa.com — and add the booking link field
   (WellnessLiving URL) so "Book" appears on the profile.
6. [ ] **Hours:** confirm Mon 10–7, Tue–Thu 9–7, Fri 9–6, Sat 9–5, Sun closed matches
   the dashboard; add holiday hours through Labor Day.
7. [ ] **Services section:** list every service from client.md (massage types, customized
   facials, packages, waxing, lashes/brows, permanent makeup) with prices where the
   owner is comfortable — mirrors the keyword map's dedicated-page strategy.
8. [ ] **Photos:** add current interior/treatment-room photos and tag the
   Transformations gallery material; profiles with fresh photos win the Maps pack.
9. [ ] **Start the review-generation habit toward Google and Yelp** (not Birdeye):
   a post-visit text/email with the direct Google review link. 128 people already said
   yes on Birdeye; the ask works — it's pointed at the wrong platform.
10. [ ] **Connect the GBP in Windsor.ai** so the next run of this role produces real
    insights and a live per-review reply queue.
11. [ ] **Publish GBP posts on a rhythm** (the four drafts above; roughly one per week).

## Citations plan

**Canonical NAP block (paste exactly this everywhere):**

```
Vada's Day Spa
740 W Lake Lansing Rd #300
East Lansing, MI 48823
(517) 324-8770
https://vadasdayspa.com
vadasdayspa@gmail.com
Hours: Mon 10am–7pm | Tue–Thu 9am–7pm | Fri 9am–6pm | Sat 9am–5pm | Sun closed
Category: Day spa
```

> CONFIRM (carried from client.md): the "#300" suite number appears on some listings and
> not others. Confirm it before the cleanup sweep starts — changing it twice is worse
> than once.

This plan is **fix-first**: the highest-value citation work for this client is repairing
what exists, not adding volume. Part A before Part B.

### Part A — Fix existing listings (do these first; they are actively hurting)

| # | Directory / listing | Problem found | Action |
|---|---|---|---|
| 1 | **TripAdvisor** (tripadvisor.com, "Vada Day Spa", filed under Lansing) | Wrong name, **wrong city**, and the unanswered negative 2026 review | Claim the listing, correct name to "Vada's Day Spa" and city to East Lansing, post the approved reply from the queue above |
| 2 | **Facebook — duplicate pages** (facebook.com/VadasDaySpaEastLansing and facebook.com/vadasdayspasalon) | Two pages split the social entity; one uses "Vadas" (no apostrophe) | Pick the page with more followers/history as survivor, request Facebook merge (or mark the other permanently closed/redirect), set survivor name to "Vada's Day Spa", NAP to canonical |
| 3 | **WellnessLiving — duplicate listings** (/vadasdayspa/ and /vadasdayspaandsalon/) | Two booking-platform listings split the same business; this is also likely the booking system of record | Contact WellnessLiving support to merge into one listing under the canonical name; keep the surviving URL as the GBP booking link |
| 4 | **Wheree** (vadas-day-spa-and-beauty-salon.wheree.com) | Wrong name AND categorized as **"Nail Salons"** | Claim/suggest-edit: name → canonical, category → Day Spa |
| 5 | **Yelp** (yelp.com/biz/vadas-day-spa-east-lansing) | Name correct but only 12 reviews vs 128 on Birdeye — the review-equity problem; Yelp is what AI assistants cite | Verify NAP/suite, add full service list and photos; point a share of the review-ask rotation at Yelp (never incentivized — against Yelp policy) |
| 6 | **ClassPass** (classpass.com/studios/vadas-day-spa-and-salon-east-lansing) | Listed as "…and Salon" | Update business name to canonical via ClassPass partner support |
| 7 | **Chamber of Commerce** (chamberofcommerce.com) | Listed as "…and Salon"; carries 4.7/88 reviews worth keeping attached to the right entity | Claim and correct name + NAP |
| 8 | **Mindtrip.ai and Atly** | AI-native discovery products carrying "…and Beauty Salon" | Claim/correct where claimable — these feed AI answers directly (GEO audit) |
| 9 | **Instagram** (@vadasdayspasalon) | Display name "Vada Day Spa" | Set display name to "Vada's Day Spa"; keep handle; make bio NAP match canonical |
| 10 | **Groupon** | Page exists; business decision open (client.md CONFIRM) | Either use it or retire it — but correct the NAP to canonical either way |

### Part B — Add or verify presence (ranked by value for a day spa in East Lansing)

| # | Directory | Why it matters |
|---|---|---|
| 11 | **Bing Places** | Feeds Bing/Copilot answers; usually importable straight from a clean GBP — do it after the GBP is fixed |
| 12 | **Apple Business Connect** (Apple Maps) | Every iPhone "spa near me" in the car; unclaimed listings show bare pins |
| 13 | **lansing.org — Greater Lansing CVB "Spas & Wellness" page** | High-trust local source AI engines quote; competitors surface there, Vada's inclusion unconfirmed (GEO audit). Request listing |
| 14 | **Nextdoor (business page)** | East Lansing/Okemos/Haslett neighbors asking "who does good facials?" — the exact recommendation channel for this niche |
| 15 | **BBB profile** | Trust citation; competitor Tropical Touch carries a 1-star BBB entry — a clean accredited profile is a visible differentiator |
| 16 | **Greater Lansing Area Moms — beauty & wellness resource list** | Exactly the spa-party and gift-buyer audience; inclusion unconfirmed (GEO audit). Request listing |
| 17 | **Lansing Regional Chamber of Commerce membership directory** | Local authority citation + the membership is itself a networking channel for the private-parties business |

**NAP inconsistency summary being fixed above:** 5 name variants, 1 wrong city
(TripAdvisor), 1 wrong category (Wheree), 2 duplicate Facebook pages, 2 duplicate
WellnessLiving listings, and an unresolved suite number. Every fix uses the canonical
NAP block verbatim.

## Handoff to Client Report Builder

- **Review footprint:** 4.6 stars / 128 reviews (Birdeye aggregate) is the strongest
  verified public number; Yelp shows only 12; the native Google count is unverified —
  > NEEDS DATA: confirm from GBP dashboard before quoting any Google number.
- **Drafted replies awaiting approval:** 1 (the provisional TripAdvisor negative-review
  reply — must be verified against the full review text before posting). Google-review
  drafts are blocked until the GBP is connected in Windsor.ai.
- **Single most valuable GBP gap:** entity fragmentation — five business-name variants,
  two duplicate Facebook pages, two duplicate WellnessLiving listings, TripAdvisor under
  the wrong city, and Wheree under the wrong category. One cleanup sweep (Citations plan
  Part A) consolidates every "near me" signal onto one clean entity.
- **The insight number that lands:** *128 five-ish-star reviews (4.6) are sitting on
  Birdeye where Google and AI assistants never look — while only 12 show on Yelp and the
  top local competitor shows ~350 on Google. The reputation already exists; it's parked
  on the wrong platform.*

---
*Sources: Wave 1 files (01-keyword-map.md, 03-performance-snapshot.md, 04-geo-audit.md,
all 2026-07-15, built from live search evidence with URLs cited there);
context/client.md and context/brand-voice.md. Windsor.ai GBP connector: not connected
this run. Direct site/listing fetches blocked; live search quota exhausted after one
query this session. Nothing in this file publishes anything — every reply, post, and
listing edit above is a draft for human approval.*
