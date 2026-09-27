# Lead scraper agent

Finds outreach targets for Uncle T Agency: local businesses with no website and no online booking system, the exact gap Lexi sells into.

## What it does

`scripts/lead_scraper.py` searches Google Maps (via Apify) across a vertical's search terms and target suburbs, de-duplicates results, and for any business with a listed website, checks it with Firecrawl for a real booking system (a "Book Now" link, or a known platform like Calendly, Fresha, Booksy, Setmore). Results are ranked into three tiers and written to a CSV:

- **A, no website**: the strongest fit, scored highest.
- **B, website but no booking found**: also a real fit, just harder to spot without the check.
- **C, already has a booking system**: deprioritised, probably not worth pursuing.

Within each tier, results sort by Google review count, more reviews suggests a more established business worth the outreach effort.

## How to run it

```bash
uv run python scripts/lead_scraper.py --vertical "hair salon"
uv run python scripts/lead_scraper.py --vertical "hair salon" --suburbs Bellville,Parow --limit 30
```

Output lands in `outputs/leads/<date>-<vertical>-<suburbs>.csv`.

## Setup needed

Two things, both under the cloud environment's Edit settings (same screen used for the Firecrawl network fix on 27 Sept):

1. **Network access**: `api.apify.com` needs to be in the allowed hosts list.
2. **API key**: `APIFY_API_TOKEN` needs to be set (sign up free at console.apify.com, Console → Settings → Integrations for the token). `.env.example` documents it.

Both are environment-level settings, so once set they should carry into future sessions on this environment (unlike `.env` itself, which is machine-local and doesn't sync).

## Adding a new vertical

Edit `scripts/lead_scraper_verticals.json`, add a key with `terms` (search phrases Maps responds well to) and `suburbs`. No code changes needed. `context/business.md` lists the priority order for what's next: med spas, dog groomers, cleaning businesses, then plumbers, dentists, real estate agents, and a longer list of strong untapped verticals below that.

## First real run (27 Sept 2026, confirmed working)

Ran live for the first time: 16 search queries (hair salon terms × Bellville, Mitchell's Plain, Parow, Goodwood), 79 unique businesses after de-dupe, 54 with no website, 20 with a website but no booking system found, 5 already booked-up. Field names matched what the script expected exactly, no code changes needed there. Spot-checked against real Google listings, all correct, including REEVA Hair & Beauty Salon, already a warm lead in the pipeline.

One real bug found and fixed: the Google Maps actor ID was wrong (`apify~google-maps-scraper`, which doesn't exist). Corrected to `compass~crawler-google-places`, Apify's actual "Google Maps Scraper" actor.

**Real cost**: about $0.32 in Apify platform credit for this run (80 raw results, free-tier account), plus 25 Firecrawl scrapes (against a 1,000/month plan, negligible). A run like this roughly 15 times over before the Apify free tier's monthly credit runs out.

## Known limitations

- Booking-signal detection is a heuristic (keyword and known-platform matching in the page's text and links), not a certainty. A "no booking found" row can still be wrong if a site buries its booking link somewhere the scrape didn't reach.
- Output is a plain CSV for now, not pushed into Google Sheets automatically. See `plans/2026-09-27-lead-scraper-agent.md`'s Notes for planned Phase 2 work.

## Related

- `plans/2026-09-27-lead-scraper-agent.md`, the full build plan and design decisions.
- `context/ideas.md`, the original framing.
- `.claude/skills/apify`, `.claude/skills/firecrawl`, the two integrations this script builds on.
