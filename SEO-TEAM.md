# Specialist SEO Team for Claude Code

A replica of the "SEO team in Claude Code" pattern: one coordinator command orchestrating 8 specialist subagents. Everything is plain markdown in `.claude/` — no paid tools required.

```
                    ┌──────────────┐
                    │ 00 Coordinator│   /seo-team command
                    └──────┬───────┘
      ┌───────────┬────────┼────────────┬─────────────┐
 01 Keyword   02 Technical  03 Analytics  04 AI Search/GEO   ← research (parallel)
 Research     Audit
      └───────────┴────────┼────────────┴─────────────┘
        ┌──────────────────┼──────────────────┐
   05 On-Page Copy   06 Blog/Content     07 Local SEO        ← execution (parallel)
        └──────────────────┼──────────────────┘
                    ┌──────┴───────┐
                    │ 08 Client    │
                    │    Report    │
                    └──────────────┘
```

## Quick start

From this repo in Claude Code:

```
/seo-team Joe's Plumbing, joesplumbing.example.com, serves Austin TX,
competitors: abcplumbing.com radiantplumbing.com, goal: more calls
```

The coordinator collects anything missing, then runs the phases. Deliverables land in `seo-workspace/<client>/` as numbered markdown files, ending with a client-facing report (`08-client-report.md`).

## The team

| # | Agent | File | Does |
|---|-------|------|------|
| 00 | Coordinator | `.claude/commands/seo-team.md` | Intake, dispatch, integration, close-out |
| 01 | Keyword Research | `.claude/agents/seo-keyword-research.md` | Clusters, intent, keyword→page map |
| 02 | Technical Audit | `.claude/agents/seo-technical-audit.md` | Crawls the live site; indexability, metadata, schema |
| 03 | Analytics | `.claude/agents/seo-analytics.md` | GSC/GA4 export analysis, quick wins, or a measurement plan |
| 04 | AI Search / GEO | `.claude/agents/seo-ai-search-geo.md` | Entity + citability for ChatGPT/Perplexity/AI Overviews |
| 05 | On-Page Copy | `.claude/agents/seo-onpage-copy.md` | Titles, metas, H1s, copy rewrites, internal links |
| 06 | Blog / Content | `.claude/agents/seo-blog-content.md` | Calendar, briefs, drafts, refreshes |
| 07 | Local SEO | `.claude/agents/seo-local.md` | GBP, citations/NAP, local pages, reviews |
| 08 | Client Report | `.claude/agents/seo-client-report.md` | One plain-language report from all deliverables |

You can also invoke any specialist directly, e.g. *"use the seo-technical-audit agent on example.com"*.

## Design choices (why this differs from a demo)

- **No invented data.** Every agent is forbidden from fabricating search volumes, traffic, rankings, or review counts. Numbers must come from files you provide (GSC/GA4 exports) or from pages the agent actually fetched; everything else is labeled as inference.
- **No paid connectors.** Instead of a data pipeline subscription (e.g. Windsor.ai), agent 03 works from free CSV exports out of Google Search Console and GA4. Drop them in the client workspace and mention the paths when you run `/seo-team`.
- **Files are the memory.** Each run's deliverables persist in `seo-workspace/`, so the next run (or next month's report) builds on real history.

## Getting real data (all free)

1. **Google Search Console** → Performance → Export (CSV). The single highest-value input.
2. **GA4** → Reports → export, or connect via the GSC/GA4 APIs later.
3. Re-run `/seo-team` (or just the `seo-analytics` agent) pointing at the export files.

## Honest expectations

Setup takes minutes; rankings don't. This team is excellent at audits, plans, briefs, copy, and reporting — the human still owns publishing, GBP access, link building, and judgment. Re-run monthly with fresh exports for compounding value.
