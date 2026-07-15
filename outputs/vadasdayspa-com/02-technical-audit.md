# Technical Audit: Vada's Day Spa (2026-07-15)

> NEEDS DATA: direct crawl blocked by network policy; on-page checks (robots.txt,
> sitemap, canonicals, meta robots, schema/JSON-LD, page weight, Core Web Vitals,
> mobile viewport, internal link depth, redirect chains, 4xx checks) require a run
> with unrestricted network or a DataForSEO OnPage crawl. Everything below is based
> on what search engines externally expose: which pages are indexed and how their
> titles render in search results, plus third-party listing data. On-page items not
> observable this way are marked **not verifiable this run** — they are not "passed".

## Health score

**62 / 100 (provisional, external-signals only).** Indexability looks healthy — all
core pages are in Google's index — but the metadata layer is weak on exactly the
pages that earn bookings, and the site targets "Lansing" on the homepage while the
business, its address, and its reviews all say East Lansing. Score covers only the
observable portion; a full crawl could move it in either direction.

## Critical issues

| Issue | Pages affected | Evidence | Fix |
|---|---|---|---|
| *None verified this run.* All money pages found indexed; nothing observed actively blocks ranking. | — | 12 URLs surfaced via `site:` queries: home, /spa-day-packages, /massages, /facials, /waxing, /lashes, /permanent-makeup, /makeup, /about, /contact, /gallery, /blog | Re-check after a full crawl — noindex tags, sitemap errors, and mobile blockers are exactly the criticals a crawl catches and search results can't. |

## Important issues

| Issue | Pages affected | Evidence | Fix |
|---|---|---|---|
| Missing/default title tag | /makeup | Renders in search results as just "Vada's Day Spa" — no service keyword, no location | Write a real title ("Makeup Services in East Lansing, MI \| Vada's Day Spa") — or see the overlap issue below first |
| Likely page overlap: /makeup vs /permanent-makeup | /makeup, /permanent-makeup | Two indexed URLs for adjacent topics; /makeup has no distinct title, suggesting a thin or leftover page | Decide: if /makeup is a distinct service (event/bridal makeup), differentiate it; if not, 301 it to /permanent-makeup |
| Garbled contact-page title | /contact | Renders as "Schedule Contact Us Your Spa Appointment" in one query and bare "Vada's Day Spa" in another — the inconsistency means Google is rewriting a weak title | Replace with "Contact & Book \| Vada's Day Spa, East Lansing, MI" |
| Money-page titles missing location and/or brand | /spa-day-packages ("Luxury Spa Day Packages & Deals"), /massages ("Relaxing & Therapeutic Spa Massages"), /waxing (no location), /permanent-makeup ("Wake Up Perfect with Permanent Makeup" — no brand, no location) | Titles as rendered in SERPs; only /facials ("Facials East Lansing MI \| Dermaplaning, BB Glow & More") gets the local pattern right | Standardize on the /facials pattern: `<Service> East Lansing MI \| <differentiator> \| Vada's Day Spa`, within ~60 characters |
| Homepage targets the wrong city | / (homepage) | Title reads "Day Spa in Lansing, MI \| …" while the address, GBP, and every review platform say East Lansing | Confirm the intended target with the owner (client.md flags this). If East Lansing customers are the base, retitle to "Day Spa in East Lansing, MI \| …" and add Lansing/Okemos/Haslett in page copy instead |
| Keyword-stuffed lashes title | /lashes | "Eyelashes, Lash Services, Brows and Lashes - Vada's Day Spa - East Lansing, Michigan" — redundant, well over 60 chars, will be truncated/rewritten | "Lash Lifts & Brow Tinting in East Lansing, MI \| Vada's Day Spa" |
| No dedicated pages for named core services | Nails (manicures/pedicures), hair styling, gift cards | Manicure/pedicure appears in the homepage title and packages copy, hair styling and gift certificates appear in on-site text, but no /nails, /hair, or /gift-cards URL surfaced in the index | Create dedicated pages — a service without its own URL can't rank for its own query ("pedicure east lansing" has nowhere to land) |
| No individual blog posts indexed | /blog/* | Only the /blog hub page surfaces for `site:vadasdayspa.com/blog`; zero post URLs found | Verify with a crawl whether posts exist but aren't indexed (sitemap/canonical problem) or don't exist (content gap — hand to Blog Writer) |
| Business name inconsistent across listings (local trust signal) | Off-site, affects local pack | "Vada's Day Spa" (site, Yelp, Birdeye) vs "Vada's Day Spa and Salon" (ChamberOfCommerce, BestProsInTown, LocalStylist, ClassPass) vs "Vada's Day Spa and Beauty Salon" (Wheree); suite "#300" present on site, absent on several listings; Wheree categorizes the business under "Nail Salons" | Pick one canonical name + address form (client.md flags this) and hand the cleanup list to the Local SEO Manager (07) |

## Minor issues

- /blog title ("Blog | Spa Tips & Beauty Insights") and /spa-day-packages title omit the brand name — small CTR/branding loss.
- Phone number is consistent everywhere observed ((517) 324-8770) — keep it that way when fixing listings; only names/suite vary.

## Not verifiable this run (do not assume these passed)

robots.txt rules; XML sitemap presence/freshness; canonical tags; meta robots;
meta descriptions (search snippets seen may be Google-generated); H1s and heading
hierarchy; JSON-LD schema (LocalBusiness/Service/FAQPage); page weight,
render-blocking resources, image formats; mobile viewport; internal link depth and
orphan pages; redirect chains and internal 4xx errors.

## What's already good

- Every money page is indexed: packages, massages, facials, waxing, lashes, permanent makeup, plus about/contact/gallery — Google can find and surface the whole service catalog.
- Clean, readable, flat URL structure (/massages, /facials, /spa-day-packages) — services sit one level below home, so 2-click reachability from the homepage is very likely.
- /facials already has a model title ("Facials East Lansing MI | Dermaplaning, BB Glow & More") — the fix for the other pages is to copy a pattern that already exists on the site.
- Contact details (address with suite, phone, hours) are consistently exposed on the site's own pages and picked up verbatim by search engines.
- Strong third-party review footprint to build on: 4.6 stars / 128 reviews (Birdeye), 4.7 / 88 elsewhere.

## Fix order

1. **Run the missing crawl** (unrestricted network or DataForSEO OnPage) to clear the "not verifiable" column — any noindex/sitemap/canonical problem found there jumps to the front of this list.
2. **Owner decision: Lansing vs East Lansing targeting, and /makeup's fate** — these gate the title rewrites, so decide before writing.
3. **Rewrite titles (and metas) on money pages** — /makeup, /contact, /spa-day-packages, /massages, /waxing, /permanent-makeup, /lashes, homepage — using the /facials pattern. Highest-leverage change available without a crawl.
4. **Create the missing service pages** (nails, gift cards; hair if still offered) so the new titles have complete coverage of what the business sells.
5. **NAP/name cleanup across directories** (Local SEO Manager) — do after the canonical name decision in step 2, since the same decision feeds both.
6. **Blog: verify post indexation, then fill the content gap** (Blog Writer) — depends on step 1's sitemap findings.

## Handoff

**To the On-Page Copywriter (05):** rewrite titles/metas in this priority order —
(1) /makeup (bare default title), (2) /contact (garbled, being rewritten by Google),
(3) /spa-day-packages, /massages, /waxing, /permanent-makeup (no location, mostly no
brand), (4) /lashes (stuffed, over-length), (5) homepage (pending the Lansing vs East
Lansing decision). Model everything on /facials. Meta descriptions are unverified for
all pages — write fresh ones for every page you touch. Schema is unverified: include
LocalBusiness + Service JSON-LD in your recommendations using the canonical NAP
(740 W Lake Lansing Rd #300, East Lansing, MI 48823, (517) 324-8770).

**To the Client Report Builder (08), headline findings:** (a) the site tells Google
it's in Lansing while every review platform says East Lansing; (b) booking pages are
indexed but carry titles with no location — easy, high-impact fixes; (c) a full
technical crawl is still owed (blocked this run) and may add findings.
