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

## Known limitations (as of first build, 27 Sept 2026)

- The Apify Google Maps actor's exact field names weren't verified against a live call when this was built (network was blocked in that session). Use `--raw-sample` on the first real run to confirm, and fix up the field names in `lead_scraper.py` if Apify's actor has changed shape since.
- Booking-signal detection is a heuristic (keyword and known-platform matching in the page's text and links), not a certainty. Spot-check the first run's results before trusting the ranking fully.
- Output is a plain CSV for now, not pushed into Google Sheets automatically. See `plans/2026-09-27-lead-scraper-agent.md`'s Notes for planned Phase 2 work.

## Related

- `plans/2026-09-27-lead-scraper-agent.md`, the full build plan and design decisions.
- `context/ideas.md`, the original framing.
- `.claude/skills/apify`, `.claude/skills/firecrawl`, the two integrations this script builds on.
