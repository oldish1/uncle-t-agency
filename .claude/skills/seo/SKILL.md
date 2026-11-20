---
name: seo
description: >
  Local search visibility check and fix plan for a small business: Google Maps and Business Profile,
  Google results, and AI answers (ChatGPT, Claude, Gemini, Perplexity). Use when the user says /seo,
  "Found Check", "rank her on Google", "get X on page one", "why isn't X showing", "audit this website",
  GEO, AEO, AI SEO, Google Business Profile, reviews for ranking, or asks to check a client or prospect's
  visibility. Produces a short WhatsApp-ready report (Found Check) or a full plan.
user-invocable: true
---

# SEO / Get Found

The workflow we worked out on CHALES Hair Boutique (Oct to Nov 2026), written down so it isn't rebuilt each time. Used for the free Found Check (lead magnet) and for paid Get Found work. Product idea: `outputs/2026-11-20-get-found-offer.md`.

## Rules that come from mistakes we already made

1. **Look before you claim.** Before saying a page, listing or plan doesn't exist, check: `git fetch`, `git branch -r`, `ls outputs plans`, grep the ledger and `context/`, and look at the live site. On CHALES we twice said things didn't exist (service pages, Google listing) that other sessions had built.
2. **One failed search is not proof.** A Maps scraper missing a listing means "not found by that method". Use two methods (Maps scrape and web search) and ask the owner before saying "she isn't on Google".
3. **Read the live site before asking for facts.** Prices, hours and FAQs are usually already on the page.
4. **Facts must match everywhere**: name, address, phone, hours on the site, Google listing, social bios and the booking system. Mismatches are a finding, not a detail.
5. **Never promise a ranking or a date.** Promise the work and a monthly report with real numbers.
6. **Google's rules**: no fake reviews, no reviews for discounts, never hide the Google review button from unhappy clients.
7. **Say what you couldn't check** (Apify out of credit, PageSpeed quota, tool blocked) instead of guessing.
8. **Private things stay private**: bank details on a client's site get flagged to the owner, not repeated in public reports.

## Modes

Read the first word of the arguments.

### `/seo <business name or url>`: Found Check (default, ~15 minutes)

Goal: one short report the owner can read on WhatsApp, with the 3 biggest problems and one fix they can do today.

1. **Collect**: business name, suburb, website, what they sell, main competitor if known. Missing a website is itself the finding.
2. **Site check**: `python3 scripts/seo_check.py <url>`. Run it on the home page and one service page if there is one. It reports title, schema, phones, hours, analytics, photos, sitemap, AI bot access and risks like public bank details. Trust its findings, but eyeball the page for context.
3. **Google Maps and listing**: `apify` skill, actor `compass~crawler-google-places` with the business name and suburb and `maxReviews: 5`, plus a competitor query like "hair salon <suburb>" (10 results). Record rating and review count for the business and the top competitors. If Apify says the monthly credit is used up, say so and use Firecrawl search instead.
4. **Search and AI baseline**: run these with WebSearch (standard mode), in parallel: the business name + suburb; "best <trade> <suburb>"; "<main service> <suburb>"; "<service 2> <suburb>". Note who appears (directory pages like Fresha dominating is a finding) and whether the business appears at all. Empty results for a service ("nobody ranks for nanoplastia Bellville") are an opportunity, say so.
5. **Write the report** (format below), save to `outputs/found-checks/YYYY-MM-DD-<slug>.md`.
6. **Log it**: one ledger row, `sales/research` or `marketing/research`.

### `/seo full <business or url>`: full audit and plan

Everything in the Found Check, plus: every page in the sitemap through `seo_check.py`, a read of each service page against `references/page-checklist.md`, reviews and photos comparison against the top 3 competitors, the 8-search tracking sheet, and a phased plan with who does what. Save to `plans/<date>-<slug>-seo-plan.md`. For deeper method use the claude-seo repo's `seo-local` and `seo-geo` skills if installed (github.com/AgriciDaniel/claude-seo, MIT licensed, read-only clone works).

### `/seo monthly <client>`: monthly check

Re-run the 8 searches from `references/monthly-check.md` in Google, ChatGPT, Claude with web search, and Perplexity (the tools you can't run, mark "ask the owner to check"). Compare to last month's file in `outputs/found-checks/` or the client's folder. Report: reviews gained, rating, calls and direction requests (from Google profile screenshots the owner sends), rank for each search, what moved, next 3 actions. Save and log.

### `/seo fix <url>`: apply fixes to a client site

Only after the owner agreed. Pull the live site first and never deploy an old copy over it (the live page changed twice behind our back on CHALES). Make changes in the client's `apps/` folder, deploy as a draft preview, send the link, publish only on a yes. Test locally for broken images and page errors before the draft.

## Found Check report format

Plain English, written to the owner, no jargon, under 250 words, follows `reference/writing-style.md` (no em dashes). Structure:

```
Hi <name>, I had a look at how <business> shows up when people search.

What I found:
1. <biggest problem, with the proof: "Searching 'hair salon Oakdale' shows 5 salons, you're not one">
2. <second>
3. <third>

What's working: <one genuine good thing>

One thing you can do today: <a 10-minute action>

I can fix all of this for you. Want me to show you how?
```

Rank problems by how many customers they cost: not showing on Maps or Google for the main service, then no reviews, then website problems, then small stuff. Compare with a real nearby competitor by name when you have numbers ("Salon X has 29 reviews, you have 3").

## Costs and limits

- Apify free plan is $5 a month; one Maps scrape is cents but a lead scraper run eats it. If it's blocked, fall back to Firecrawl.
- PageSpeed Insights' free API quota is often used up. Say "speed not measured" rather than guess.
- Real Maps position by area, search volumes and backlinks need paid tools (DataForSEO, Local Falcon). Don't pretend to have them.

## References

- `references/page-checklist.md`: what a service page needs to be found and quoted by AI.
- `references/monthly-check.md`: the 8-search tracking template and AI crawler notes.
- CHALES worked example: `plans/2026-11-04-chales-google-page-one.md`, `outputs/2026-11-20-chales-claude-ai-search-playbook.md`.
