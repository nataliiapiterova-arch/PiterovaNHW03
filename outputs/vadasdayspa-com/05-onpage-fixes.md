# On-Page Fixes: Vada's Day Spa (2026-07-15)

> **DRAFT for human review. Nothing here is published.**
>
> **Method note (read before using):** direct fetches of vadasdayspa.com were blocked by
> network policy this run, so no page HTML was read. "Current title" values come from the
> technical audit's SERP-rendered titles (reliable). Current meta descriptions, current
> H1s, and current body copy were **not readable this run** — nothing below claims to
> quote them. All H1s, heading outlines, and copy are written fresh from client.md and
> brand-voice.md and must be **verified against the live page before pasting** (the live
> page may already contain sections proposed here, or copy worth keeping).
>
> **Two owner decisions gate this file** (flagged throughout):
> 1. Homepage target city: Lansing (current) vs East Lansing (the actual location). Both
>    options are drafted; do not ship either until the owner picks.
> 2. The fate of /makeup: redirect into /permanent-makeup, or differentiate as a real
>    event/bridal makeup service.

---

## Keyword-cluster → page mapping (reconciled)

Two corrections to the keyword map, based on the audit's index list:

- **Facials:** the map recommends a "new dedicated page," but **/facials already exists,
  is indexed, and has the site's best title** ("Facials East Lansing MI | Dermaplaning,
  BB Glow & More"). Action: strengthen /facials, do not build a duplicate.
- **Lash and brow:** the map recommends a "new page," but **/lashes already exists and is
  indexed** (with a stuffed title). Action: fix /lashes, do not build a duplicate.

| Cluster (intent) | Page | Action here |
|---|---|---|
| Day spa core (transactional/local) | / | Metadata + H1 + outline + first-fold copy (city decision pending) |
| Spa day packages (transactional/local) | /spa-day-packages | Full rework: metadata, H1, outline, copy, FAQ, schema |
| Massage therapy (transactional/local) | /massages | Strongest rebuild — invisible on "massage east lansing" |
| Facials (transactional/local) | /facials | Title: **no change** (it's the model). New meta, outline notes, schema |
| Waxing (transactional/local) | /waxing | Metadata + H1 + outline + schema |
| Permanent makeup (transactional/local) | /permanent-makeup | Metadata + H1 + FAQ block + schema |
| Lash and brow (transactional/local) | /lashes | Metadata + H1 (de-stuff) |
| Couples massage (transactional/local) | **no page** | → New pages needed (confirm service first) |
| Spa mani/pedi (transactional/local) | **no page** | → New pages needed |
| Gift cards (transactional, seasonal) | **no page** | → New pages needed |
| Question/informational cluster | /blog + on-page FAQs | Question-shaped H2s below; full posts → Blog Writer |

---

## Metadata rewrites

Title rule used: 50–60 chars, primary keyword front-loaded, location for local, brand at
the end only where it fits — the pattern /facials already proves on this site. Current
metas were not readable this run; every meta below is new. Character counts shown.

| URL | Current title (SERP-rendered) | New title | New meta description | Target keyword |
|---|---|---|---|---|
| / | "Day Spa in Lansing, MI \| …" | **Option A (East Lansing):** "Day Spa in East Lansing, MI \| Facials, Massage & Packages" (57) **Option B (keep Lansing):** "Day Spa in Lansing, MI \| Facials, Massage & Spa Packages" (56) — **> CONFIRM: owner decision, see below** | "Massage, customized facials, nails and spa day packages in East Lansing. Vada's has pampered mid-Michigan since 2011 — call (517) 324-8770 to book." (147) | day spa east lansing mi / day spa lansing mi |
| /spa-day-packages | "Luxury Spa Day Packages & Deals" (no brand, no location) | "Spa Day Packages in Lansing, MI from $160 \| Vada's Day Spa" (58) — keeps "Lansing" per the keyword map ("spa packages lansing mi" is where it ranks top-3 today) | "Spa day packages from $160 — combine a rejuvenating facial, relaxing massage and spa mani-pedi in one visit. 2 to 4 hours of pampering in East Lansing." (151) | spa packages lansing mi |
| /massages | "Relaxing & Therapeutic Spa Massages" (no brand, no location) | "Massage Therapy East Lansing MI \| Deep Tissue & Hot Stone" (57) | "Swedish, deep tissue and hot stone massage in East Lansing. Unhurried, customized sessions at Vada's Day Spa on Lake Lansing Rd. Call (517) 324-8770." (149) | massage east lansing |
| /facials | "Facials East Lansing MI \| Dermaplaning, BB Glow & More" | **No change — this is the model title the rest of the site is copying.** Rewriting it risks a page that already gets the pattern right. | "Customized facials in East Lansing — dermaplaning, BB Glow and classic spa facials tailored to your skin by Vada. See what your skin has been missing." (150) | facials east lansing mi |
| /waxing | (no location, per audit) | "Waxing in East Lansing, MI \| Facial & Body \| Vada's Day Spa" (59) | "Facial and body waxing in East Lansing by an experienced esthetician. Gentle, private and unhurried — brows to full body. Book at Vada's Day Spa." (145) | waxing east lansing mi |
| /permanent-makeup | "Wake Up Perfect with Permanent Makeup" (no brand, no location) | "Permanent Makeup in East Lansing, MI \| Wake Up Ready" (52) — keeps their "wake up" hook, adds the geo the SERP requires | "Wake up ready with permanent makeup in East Lansing. Natural-looking brows and eyeliner from Vada's Day Spa. Ask about healing time, cost and touch-ups." (152) | permanent makeup east lansing |
| /lashes | "Eyelashes, Lash Services, Brows and Lashes - Vada's Day Spa - East Lansing, Michigan" (stuffed, 85 chars) | "Lash Lifts & Brow Tinting East Lansing MI \| Vada's Day Spa" (58) | "Lash perms and eyebrow tinting in East Lansing. Low-maintenance lashes and brows that last for weeks — no daily curling or filling in. Book with Vada." (150) | lash lift east lansing |
| /makeup | "Vada's Day Spa" (bare default) | **Recommended: 301 → /permanent-makeup** (see New pages / decisions). If kept as a distinct event/bridal service: "Makeup Services East Lansing MI \| Vada's Day Spa" (48) | If kept: "Professional makeup application in East Lansing for weddings, proms and special events. Look your best in photos — book your session with Vada." (143) | makeup east lansing (only if kept) |
| /contact | "Schedule Contact Us Your Spa Appointment" (garbled; Google is rewriting it) | "Contact & Book \| Vada's Day Spa, East Lansing, MI" (49) | "Book your spa appointment in East Lansing. Call (517) 324-8770 or visit us at 740 W Lake Lansing Rd. Open Monday through Saturday, closed Sunday." (145) | book spa appointment east lansing (navigational) |
| /blog | "Blog \| Spa Tips & Beauty Insights" (no brand) | "Spa Tips & Beauty Insights \| Vada's Day Spa Blog" (48) | "Spa advice from Vada's Day Spa in East Lansing: what a spa day costs, how to choose a massage, facial care between visits, and more." (132 — hub page, acceptable) | informational hub |
| /gallery | (not flagged; audit did not capture a title) | "Transformations Gallery \| Vada's Day Spa, East Lansing" (54) — **verify current title before replacing; it was not observed this run** | "Real results from Vada's Day Spa: facials, lashes, brows and permanent makeup on real East Lansing clients. See the transformations, then book yours." (149) | brand/proof (supports all clusters) |
| /about | (not flagged; title not observed this run) | No rewrite proposed blind. After the crawl, apply the same pattern if it lacks brand/location, e.g. "About Vada \| Day Spa in East Lansing Since 2011" (47). | "Vada opened her East Lansing day spa in 2011 after years as a spa specialist — and a nurse before that. Meet the person behind your next spa day." (145) **> CONFIRM: nursing background approved for marketing use (client.md flag)** | brand |

**Canonical + Open Graph (every page above):** self-referencing canonical
(`<link rel="canonical" href="https://vadasdayspa.com/<path>">`); `og:title` = the new
title without the brand suffix; `og:description` = the new meta. Canonicals were not
verifiable this run — the crawl in the audit's step 1 must confirm none currently point
elsewhere.

**> CONFIRM (homepage city):** the site says Lansing; the address, GBP, and every review
platform say East Lansing. Option A (East Lansing) matches the entity signals and the
modifier every winning competitor uses; Option B keeps the bigger-catchment term the page
already ranks #1 for. This is the audit's flagged owner decision — the compromise either
way is to put the *other* city (plus Okemos, Haslett, MSU) in body copy and schema
`areaServed`, which the drafts below do.

---

## H1 fixes

Current H1s were **not readable this run** — the audit could not verify them, and no live
fetch was possible. Do not treat "current H1" as known; verify each page has exactly one
H1 and replace it with the target below.

| URL | Current H1 | New H1 (exactly one per page) | Intent it matches |
|---|---|---|---|
| / | not readable this run | Option A: "A Day Spa in East Lansing for Massage, Facials & Spa Days" / Option B: same with "Lansing" — **follows the title decision** | "day spa near me / east lansing" — ready to book a spa visit |
| /spa-day-packages | not readable this run | "Spa Day Packages in Lansing & East Lansing" | "spa packages lansing mi" — ready to buy a package |
| /massages | not readable this run | "Massage Therapy in East Lansing, MI" | "massage east lansing" — ready to book a massage |
| /facials | not readable this run | "Customized Facials in East Lansing, MI" | "facials east lansing mi" — ready to book a facial |
| /waxing | not readable this run | "Facial & Body Waxing in East Lansing, MI" | "waxing east lansing mi" |
| /permanent-makeup | not readable this run | "Permanent Makeup in East Lansing, MI" | "permanent makeup east lansing / lansing mi" |
| /lashes | not readable this run | "Lash Lifts & Brow Tinting in East Lansing, MI" | "lash lift east lansing" |
| /contact | not readable this run | "Contact Vada's Day Spa & Book Your Appointment" | navigational booking intent |

---

## Heading outline (per money page)

Built from the keyword map's related and fan-out queries. Target term noted per heading.
H2s = buying-decision subtopics; H3s = long-tail specifics; question-shaped H2s (marked
**Q**) get answer-first openings so the money page also earns PAA/AI citations.

> DRAFT — verify against the live page before pasting; current on-page structure was not
> readable this run. Where the live page already covers a section, keep the better version.

### Homepage (/)

- **H1:** A Day Spa in East Lansing for Massage, Facials & Spa Days *(day spa east lansing — pending city decision)*
  - **H2:** Spa Services in East Lansing *(day spa services)*
    - H3: Massage Therapy *(massage east lansing — links to /massages)*
    - H3: Customized Facials *(customized facial lansing — links to /facials)*
    - H3: Manicures & Pedicures *(spa pedicure east lansing)*
    - H3: Waxing, Lashes & Brows *(waxing / lash lift east lansing — links to /waxing, /lashes)*
    - H3: Permanent Makeup *(permanent makeup lansing mi — links to /permanent-makeup)*
  - **H2:** Spa Day Packages — Our Most-Loved Way to Visit *(spa day packages near me — links to /spa-day-packages)*
  - **H2 (Q):** What's Included in a Spa Day at Vada's? *(what is included in a spa day package — fan-out)*
  - **H2:** Serving East Lansing, Lansing, Okemos & Haslett *(local modifiers; MSU mention in copy)*
  - **H2:** Why Visit Vada's *(best day spa east lansing — proof: since 2011, 4.6★/128 reviews, owner-led)*
  - **H2:** Book Your Visit *(booking CTA: phone + hours)*

### /spa-day-packages

- **H1:** Spa Day Packages in Lansing & East Lansing *(spa packages lansing mi)*
  - **H2:** Choose Your Spa Day *(spa day packages near me)*
    - H3: Mini Spa Day — $160 *(package price anchor)*
    - H3: Pampering Package — $210
    - H3: Half-Day Spa Package — $240 *(half day spa package)*
    - *(> CONFIRM: package names/prices current as of client.md; verify before publishing)*
  - **H2 (Q):** What's Included in Each Spa Package? *(what is included in a spa day package)*
    - H3: The Facial *(rejuvenating full facial — their own phrase)*
    - H3: The Massage *(relaxing full-body massage)*
    - H3: The Spa Manicure & Pedicure *(spa mani pedi lansing)*
  - **H2 (Q):** How Much Does a Spa Day Cost? *(how much is a spa day — answer-first: "$160 to $240 at Vada's…")*
  - **H2 (Q):** Are Packages Cheaper Than Booking Separately? *(fan-out; SERP consensus = yes, and Vada's pricing supports it)*
  - **H2:** Spa Days for Two, Groups & Gifts *(spa day for two, couples spa day lansing — links to future couples + gift card pages; > CONFIRM couples service exists)*
  - **H2 (Q):** What Should I Wear — and What Happens When I Arrive? *(what to wear to a day spa / first spa day)*
  - **H2:** How to Book Your Spa Day *(process: call, choose, arrive)*
  - **H2:** Spa Package FAQs *(→ FAQPage schema; tipping, timing, weekday booking from the fan-out list)*

### /massages (the rebuild — biggest gap)

- **H1:** Massage Therapy in East Lansing, MI *(massage east lansing)*
  - **H2:** Massage Services & What Each One Is For *(types of massage — the depth the winning studio pages have)*
    - H3: Swedish Massage — for Relaxation *(swedish massage lansing)*
    - H3: Deep Tissue Massage — for Tension & Knots *(deep tissue massage lansing)*
    - H3: Hot Stone Massage — for Deep Warmth *(hot stone massage east lansing)*
  - **H2 (Q):** Hot Stone vs. Deep Tissue — Which Is Right for You? *(the heavily-asked comparison; answer-first)*
  - **H2:** Your Massage Therapist *(massage therapist east lansing mi — name + credentials; > CONFIRM: therapist name(s) and licensure to publish)*
  - **H2 (Q):** How Often Should You Get a Massage? *(fan-out; answer-first)*
  - **H2:** Massage Near MSU and Across Greater Lansing *(massage near MSU / near me — areas served: East Lansing, Lansing, Okemos, Haslett)*
  - **H2:** Add a Massage to a Spa Day *(links to /spa-day-packages — the internal-link fix the keyword map calls for)*
  - **H2:** Massage FAQs *(→ FAQPage schema: what to wear, how early to arrive, tipping)*
  - **H2:** Book a Massage *(phone + hours CTA)*

### /waxing (strengthen — already page 1)

- **H1:** Facial & Body Waxing in East Lansing, MI *(waxing east lansing mi)*
  - **H2:** Facial Waxing *(facial waxing lansing)* — H3s per area: Brows / Lip / Chin / Full Face
  - **H2:** Body Waxing *(body waxing east lansing)* — H3s per area offered *(> CONFIRM: exact menu incl. Brazilian — the map targets "brazilian wax east lansing" but the service is unconfirmed)*
  - **H2 (Q):** How Long Does Waxing Last — and How Long Should Hair Be? *(fan-out pair, answer-first)*
  - **H2:** Why Wax at a Day Spa *(private room, unhurried, experienced esthetician — vs. Bliss's geo page)*
  - **H2:** Book Your Wax *(CTA)*

### /permanent-makeup (strengthen — page 1, high-ticket)

- **H1:** Permanent Makeup in East Lansing, MI *(permanent makeup east lansing)*
  - **H2:** Permanent Makeup Services *(H3s per offering — brows, eyeliner; > CONFIRM exact menu, e.g. lip blushing/microblading, before listing)*
  - **H2 (Q):** How Long Does Permanent Makeup Last? *(top question query, answer-first)*
  - **H2 (Q):** Permanent Makeup vs. Microblading — What's the Difference? *(fan-out)*
  - **H2 (Q):** Does It Hurt, and What's the Healing Time? *(fan-out pair)*
  - **H2:** Before & After *(links to /gallery — the proof asset that exists)*
  - **H2:** Pricing & Consultations *(permanent eyeliner cost signals; > CONFIRM whether prices are published)*
  - **H2:** Book a Consultation *(CTA)*

---

## Money-page copy (top 3)

> **DRAFT — verify against the live page before pasting; current on-page copy was not
> readable this run.** These are written fresh from client.md facts and brand-voice.md
> rules (warm, personal, "we" + Vada by name, contractions, no exclamation marks, no
> "team of experts", no medical claims, no "luxury/world-class"). Paragraph-level rewrites
> of existing weak copy are **not possible blind** — do them in the verification pass.

### Homepage — first fold

*(H1)* **A Day Spa in East Lansing for Massage, Facials & Spa Days**

Vada's Day Spa has been East Lansing's place to slow down since 2011. Come in for a
relaxing massage, a customized facial, a spa manicure and pedicure — or make a day of it
with one of our spa packages. You'll be looked after by people who know your name, in a
spa that never feels rushed.

Rated 4.6 stars by more than 120 clients across Lansing, East Lansing, Okemos and
Haslett. *(> CONFIRM: re-check review count before publishing — client.md flags it)*

**Call (517) 324-8770 to book** · 740 W Lake Lansing Rd, East Lansing · Open Mon–Sat

**Missing sections to add** (verify not already present): the services grid with links to
all six service pages; a "What's included in a spa day" answer-first block; an areas-served
paragraph naming Lansing, Okemos, Haslett and MSU (this is where the *non-chosen* city
from the title decision lives); a review/proof strip.

### /spa-day-packages — first fold

*(H1)* **Spa Day Packages in Lansing & East Lansing**

A spa day at Vada's brings your favorite treatments together in one unhurried visit: a
rejuvenating full facial, a relaxing full-body massage, and a pampering spa manicure and
pedicure. Packages run 2 to 4 hours and start at $160 — and booking a package costs less
than booking the same treatments separately.

Choose the Mini ($160), the Pampering Package ($210), or the Half-Day ($240), and we'll
take care of the rest. *(> CONFIRM: names, inclusions and prices against the live menu)*

**Call (517) 324-8770 to reserve your spa day.**

**Missing sections to add** (verify first): per-package inclusion lists with durations; the
"How much does a spa day cost?" answer-first block; a gifts/groups section pointing at the
future gift-card page; a first-visit expectations block (what to wear, when to arrive); an
FAQ section matching the FAQPage schema below (tipping guidance: 15–20% is the accepted
norm; weekdays are the quieter time to book).

### /massages — first fold (full rebuild)

*(H1)* **Massage Therapy in East Lansing, MI**

Whether you're carrying stress in your shoulders or just overdue for an hour to yourself,
we'll match the massage to you: Swedish for relaxation, deep tissue for stubborn knots and
tension, or hot stone when you want warmth that reaches all the way in. Every session at
Vada's is customized — tell us what you need and we'll adjust pressure, focus and pace.

Minutes from MSU on Lake Lansing Rd, serving East Lansing, Lansing, Okemos and Haslett.

**Call (517) 324-8770 to book your massage.**

**Missing sections to add** (this page needs the most): a modality menu with plain-English
"what it's for" descriptions and durations/prices (> CONFIRM pricing publication policy —
client.md flags "publishing full price lists" as an owner decision); a therapist
credibility block (name, license, years — > CONFIRM details); the hot-stone-vs-deep-tissue
comparison; a cross-sell block into /spa-day-packages; a short FAQ. Without this depth the
page cannot compete with the dedicated massage studios that own this SERP.

---

## Schema (JSON-LD)

NAP matches client.md's canonical form exactly. **> CONFIRM: suite "#300" — client.md
flags that some listings omit it; whatever the owner decides must be used identically in
schema, footer, and every citation.** Geo coordinates and social profile URLs were not
obtainable this run — placeholders are marked. No schema was verifiable on the live pages;
the crawl should confirm none of this duplicates existing markup before pasting.

### Homepage — `DaySpa` (subtype of LocalBusiness)

```json
{
  "@context": "https://schema.org",
  "@type": "DaySpa",
  "@id": "https://vadasdayspa.com/#dayspa",
  "name": "Vada's Day Spa",
  "url": "https://vadasdayspa.com/",
  "telephone": "+1-517-324-8770",
  "email": "vadasdayspa@gmail.com",
  "priceRange": "$$",
  "foundingDate": "2011",
  "image": "https://vadasdayspa.com/CONFIRM-image-path.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "740 W Lake Lansing Rd #300",
    "addressLocality": "East Lansing",
    "addressRegion": "MI",
    "postalCode": "48823",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "CONFIRM — pull from Google Maps pin",
    "longitude": "CONFIRM — pull from Google Maps pin"
  },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "10:00", "closes": "19:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday"], "opens": "09:00", "closes": "19:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "09:00", "closes": "18:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "17:00" }
  ],
  "areaServed": [
    { "@type": "City", "name": "East Lansing" },
    { "@type": "City", "name": "Lansing" },
    { "@type": "City", "name": "Okemos" },
    { "@type": "City", "name": "Haslett" }
  ],
  "sameAs": [
    "CONFIRM — Facebook URL",
    "CONFIRM — Instagram URL",
    "CONFIRM — Yelp profile URL"
  ]
}
```

### /massages — `Service` + `BreadcrumbList`

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "serviceType": "Massage therapy",
      "name": "Massage Therapy in East Lansing, MI",
      "url": "https://vadasdayspa.com/massages",
      "provider": { "@id": "https://vadasdayspa.com/#dayspa" },
      "areaServed": [
        { "@type": "City", "name": "East Lansing" },
        { "@type": "City", "name": "Lansing" },
        { "@type": "City", "name": "Okemos" },
        { "@type": "City", "name": "Haslett" }
      ],
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Massage services",
        "itemListElement": [
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Swedish massage" } },
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Deep tissue massage" } },
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Hot stone massage" } }
        ]
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://vadasdayspa.com/" },
        { "@type": "ListItem", "position": 2, "name": "Massage Therapy", "item": "https://vadasdayspa.com/massages" }
      ]
    }
  ]
}
```

### /spa-day-packages — `Service` + `BreadcrumbList` + `FAQPage`

The FAQ answers below must appear verbatim in the visible FAQ section of the page —
adjust both together or neither.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "serviceType": "Day spa packages",
      "name": "Spa Day Packages in Lansing & East Lansing",
      "url": "https://vadasdayspa.com/spa-day-packages",
      "provider": { "@id": "https://vadasdayspa.com/#dayspa" },
      "areaServed": [
        { "@type": "City", "name": "East Lansing" },
        { "@type": "City", "name": "Lansing" },
        { "@type": "City", "name": "Okemos" },
        { "@type": "City", "name": "Haslett" }
      ],
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Spa day packages",
        "itemListElement": [
          { "@type": "Offer", "price": "160", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Mini Spa Day" } },
          { "@type": "Offer", "price": "210", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Pampering Package" } },
          { "@type": "Offer", "price": "240", "priceCurrency": "USD", "itemOffered": { "@type": "Service", "name": "Half-Day Spa Package" } }
        ]
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://vadasdayspa.com/" },
        { "@type": "ListItem", "position": 2, "name": "Spa Day Packages", "item": "https://vadasdayspa.com/spa-day-packages" }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How much does a spa day cost at Vada's?",
          "acceptedAnswer": { "@type": "Answer", "text": "Spa day packages at Vada's run from $160 for the Mini Spa Day to $240 for the Half-Day package. Each combines a facial, massage, and spa manicure and pedicure, and costs less than booking the same treatments separately." }
        },
        {
          "@type": "Question",
          "name": "What is included in a spa day package?",
          "acceptedAnswer": { "@type": "Answer", "text": "Every package includes a rejuvenating facial, a relaxing full-body massage, and a pampering spa manicure and pedicure. Packages run 2 to 4 hours depending on which you choose." }
        },
        {
          "@type": "Question",
          "name": "How much should I tip at a day spa?",
          "acceptedAnswer": { "@type": "Answer", "text": "15 to 20 percent of the service price is the accepted norm at day spas, the same as you would tip elsewhere. Tip in cash or ask at the front desk when you check out." }
        },
        {
          "@type": "Question",
          "name": "What should I wear to my spa day?",
          "acceptedAnswer": { "@type": "Answer", "text": "Wear whatever is comfortable. You'll be draped during your massage and facial, and for the pedicure loose pants or a skirt makes things easier. Arrive about ten minutes early so you can settle in." }
        }
      ]
    }
  ]
}
```

*(> CONFIRM before pasting: package names/prices; the tipping and what-to-wear answers
reflect SERP-consensus guidance from the keyword map — have Vada approve the wording as
house policy.)*

### /facials, /waxing, /permanent-makeup, /lashes — `Service` + `BreadcrumbList` pattern

Reuse the /massages block, changing three values per page:

| Page | `serviceType` | `name` | Breadcrumb item 2 |
|---|---|---|---|
| /facials | "Facial treatments" | "Customized Facials in East Lansing, MI" | Facials |
| /waxing | "Waxing services" | "Facial & Body Waxing in East Lansing, MI" | Waxing |
| /permanent-makeup | "Permanent makeup" | "Permanent Makeup in East Lansing, MI" | Permanent Makeup |
| /lashes | "Lash and brow services" | "Lash Lifts & Brow Tinting in East Lansing, MI" | Lashes & Brows |

Add a `FAQPage` node to /permanent-makeup once its FAQ section (how long it lasts,
vs. microblading, healing) is written on-page — answers must match the visible text.

### /contact — no new type needed

The homepage `DaySpa` node carries NAP sitewide; on /contact just ensure the visible
NAP matches it character-for-character (including the suite decision).

---

## Internal links

| # | From URL | To URL | Anchor text |
|---|---|---|---|
| 1 | / | /spa-day-packages | "spa day packages from $160" |
| 2 | / | /massages | "massage therapy in East Lansing" |
| 3 | /spa-day-packages | /massages | "relaxing full-body massage" |
| 4 | /spa-day-packages | /facials | "rejuvenating customized facial" |
| 5 | /massages | /spa-day-packages | "add your massage to a spa day package" |
| 6 | /facials | /spa-day-packages | "make it a spa day — facial, massage and mani-pedi in one visit" |
| 7 | /waxing | /facials | "pair your wax with a customized facial" |
| 8 | /permanent-makeup | /gallery | "see before-and-after transformations" |
| 9 | /lashes | /permanent-makeup | "permanent makeup for brows and eyeliner" |
| 10 | /about | /contact | "book your appointment with Vada" |

(When the Blog Writer's posts go live: every massage-question post links to /massages,
every cost/what's-included post links to /spa-day-packages, with those same descriptive
anchors.)

---

## New pages needed (clusters with no home)

| Cluster | Proposed URL | One-line brief |
|---|---|---|
| Couples massage / couples spa day (P2) | /couples-massage | Dedicated geo-titled page targeting "couples massage lansing mi" — the direct Zoë Life gap. **> CONFIRM FIRST: that Vada's can actually do side-by-side couples services; do not build otherwise.** |
| Gift cards (P3, seasonal) | /gift-cards | Capture "spa gift card lansing mi" on-site before Q4 — demand proven by third-party gift listings already ranking; include occasions (Mother's Day, graduation, MSU parents' weekend). |
| Spa manicure & pedicure (P3) | /nails | Target "spa pedicure east lansing" as the pampering upgrade and package component — explicitly not a head-on "nail salon" play (that SERP belongs to dedicated nail salons). |
| /makeup decision (audit handoff) | — | **Recommended: 301 /makeup → /permanent-makeup** (bare default title suggests a thin/leftover page, and the topics overlap). Only keep it if event/bridal makeup is a real, bookable service — then apply the /makeup row in the metadata table. Owner call. |
| Question set (informational) | /blog/* | "How much is a spa day", "hot stone vs deep tissue", "what to wear to a spa" → Blog Writer (06); the money-page FAQ blocks above cover the transactional-adjacent slice. |

Note for the coordinator: the keyword map's "new facials page" and "new lash page" are
**not** in this table — both pages already exist (/facials, /lashes) and are handled as
strengthens above.

---

## Handoff to the Client Report Builder (08)

- **12 pages covered:** 10 metadata rewrites, 1 deliberate no-change (/facials — already
  the model title), 1 held for a crawl (/about). 8 new H1s, 5 full heading outlines, 3
  first-fold copy drafts, 6 ready-to-paste JSON-LD blocks/patterns, 10 internal links,
  3–4 new pages briefed.
- **Best before/after for the report:** /massages title — before: "Relaxing & Therapeutic
  Spa Massages" (no location, no brand, invisible for "massage east lansing"); after:
  "Massage Therapy East Lansing MI | Deep Tissue & Hot Stone" (57 chars, geo-targeted,
  names the two most-searched modalities). It's the highest-priority cluster fix and the
  clearest illustration of the site-wide pattern change.
- **Caveat to state in the report:** all copy and H1 work is draft pending a live-page
  verification pass (site fetch was blocked this run), and two owner decisions gate
  publication: homepage city targeting and /makeup's fate.
