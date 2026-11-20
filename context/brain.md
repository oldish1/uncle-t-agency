# The brain: how this workspace fits together

> The map of everything Claude can use here. Read this to know what exists before saying something doesn't. Keep it current: when a skill, app, connector or folder is added, add a line here.

## Layers

| Layer | Where | What it is |
|---|---|---|
| Rules | `CLAUDE.md`, `reference/writing-style.md` | Who we are, how Claude behaves, tool routing |
| Memory | `context/`, `ledger/`, `docs/_index.md` | The business, the work record, the doc index |
| Open work | `todo/` (start at `todo/README.md`) | Everything still to do, by area |
| Plans and outputs | `plans/`, `outputs/`, `reference/research/` | Plans, deliverables, research |
| Skills | `.claude/skills/` | Know-how Claude loads when a job matches |
| Commands | `.claude/commands/` | Buttons: `/prime`, `/log`, `/seo`, `/handoff` and more |
| Apps and scripts | `apps/`, `scripts/` | Things built here |
| Connectors | the Claude app, plus the tools listed below | Reach into Gmail, Calendar, Drive, Make, Netlify and more |

## Skills by job
- **Sales (the priority):** `sales-coach` (daily lessons, roleplay, objections), `outreach-writer` (WhatsApp drafts from the Pipeline Sheet)
- **Clients and Lexi:** `lexi-onboarding` (take a signed client live), `/seo` (Found Check, monthly visibility, local SEO and AI search)
- **Websites:** `web-builder`, `design-taste-frontend`, `scroll-craft`, `hallmark`, `impeccable`, `extract-design`, `gsap-*`, `transitions-*`
- **Instagram and content:** the `ig-*` skills (reel, caption, carousel, profile, plan, viral, repost, DMs), `humanizer`, `writing-style`
- **Research and scraping:** `firecrawl` (default web), `apify` and `apify-ultimate-scraper` (Maps, social), `supadata` (video transcripts), `deep-research`, `academic`, `x-search`, `substack`, `podcast-search`
- **Workspace:** `test`, `task-audit`, `diagram`, `new-capability`, `connectors`, Google Calendar and Gmail helpers

## Connectors and tools (what Claude can reach)
Gmail, Google Calendar, Drive, Docs, Sheets, Slides, Make (read, build and edit scenarios), Netlify (deploys), GitHub (this repo), Higgsfield and Muapi (video and image), plus proxy-connected Apify, Firecrawl, Supadata. Telegram runs through Make. Check what's actually connected before promising anything.

## Apps and agents
| Thing | Where | State (20 Nov) |
|---|---|---|
| Lexi, WhatsApp booking | Make 5043763, `context/lexi.md` | Live for CHALES, frozen at fix14 |
| Lexi 2.0 | `plans/lexi2-design.md` | Fresh build, zero warnings by design |
| Lexi Call, phone receptionist | `apps/lexi-call` | Built on Bland, test calendar |
| Rex, Theo's assistant | `apps/rex` | Live on Telegram, WhatsApp blocked by Meta limit |
| Chief of Staff, daily brief | `apps/chief-of-staff` | Playbook written, scheduled run needs Sheets access |
| Scout and lead finder | `scripts/lead_scraper.py`, `apps/lead-finder` | Built, needs keys and credits |
| CHALES website | `apps/chales-site/site` | Live, SEO pass done 20 Nov |
| Agency website | `apps/uncletsautomation` | Live at uncletsautomation.co.za |
| Nita's bot and site | `apps/rags-to-riches-bot`, `apps/rags-to-riches-site` | Bot on test number |
| T and T Engineering site | `apps/tt-engineering` | Built, lead closed |

## How work flows
1. `/prime` loads this brain and the top of `todo/`. 2. Work happens, ledger rows are written as it goes. 3. New method that repeats 3 or more times becomes a skill. 4. Anything left over goes into `todo/`. 5. `/log` ends the session.

## One brain, one branch
Until 20 Nov, parallel sessions each wrote to their own branch and could not see each other. They are merged now (`outputs/2026-11-20-branch-merge-notes.md`). Start new sessions from main after it is merged, and check `git branch -r` before saying something doesn't exist.

## Where the money questions are decided
Prices: `context/numbers.md` (check the ledger's latest decision). Offer: `context/offer.md`. Priorities: `context/strategy.md` and `todo/README.md`.
