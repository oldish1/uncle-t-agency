# Plan: Lead scraper agent, Google Maps to a ranked outreach list

**Created:** 2026-09-27
**Status:** Built, blocked on environment setup for the first live run
**Request:** An automated tool that finds Cape Town businesses with no website and no online booking system, the exact gap Uncle T Agency sells into, so Theo stops hand-building the prospect list.
**Purpose:** Turn hours of manual searching into a script that pulls a ranked, ready-to-contact list, starting with hair salons and reusable for every other vertical `context/business.md` already flags.

---

## Overview

### What This Plan Accomplishes

A script that pulls local businesses from Google Maps (via Apify), checks whether each one already has a website, and for those that do, checks whether that site has a visible booking link (via Firecrawl). It lands the results in a ranked CSV that sorts the best prospects (no website, or a website with no booking system, decent review count) to the top.

### Why This Matters

Theo's target is 5 paying clients by December, and outreach volume is the bottleneck, `context/numbers.md` shows a 20-salon list built by hand plus 5 warm leads. This script turns "find another 20 salons" from an evening of scrolling Google Maps into a few minutes of running a script, freeing that time for the actual selling (the walk-in pitch, `outputs/2026-09-27-lexi-walkin-pitch.md`, needs targets to walk in on).

---

## Current State

### Relevant Existing Structure

- `.claude/skills/apify/SKILL.md`, the workspace's existing Apify integration, already knows `apify/google-maps-scraper` as one of its "workhorse" actors, and documents the self-setup flow if `APIFY_API_TOKEN` isn't in `.env` yet.
- `.claude/skills/firecrawl` (referenced via `scripts/firecrawl_tool.py`), the workspace's web-scraping tool, used here to check a candidate's website for a booking link.
- `scripts/firecrawl_tool.py`, the pattern to follow: a small `argparse` CLI, a client class that wraps the API with clear errors, reads its key via `scripts/utils/config.py`'s `get_env()`.
- `scripts/utils/config.py`, shared `.env` loader, already handles the "key missing" case with a plain-English error.
- `context/business.md`, defines the target area (Cape Town's Cape Flats-adjacent suburbs: Bellville, Mitchell's Plain, Parow, Goodwood) and the vertical priority order (hair salons and med spas and dog groomers and cleaning businesses now; plumbers, dentists, real estate agents next; hair braiders, nail/lash techs, driving schools, cake bakers, mobile detailers, beauty therapists, appliance repair, seamstresses flagged as strong untapped verticals).
- `context/numbers.md`, current prospect tracking is entirely manual: a 20-salon outreach list and 5 warm leads, sitting in Google Sheets, no automation behind it.
- `context/tech-stack.md`, confirms Google Sheets is already the workspace's CRM stand-in, and that Google Drive is connected (reachable through the Drive connector).
- `context/ideas.md`, "Lead scraper agent" entry (added 27 Sept 2026), the original framing this plan formalises.

### Gaps or Problems Being Addressed

- No automated way to find prospects, everything so far has been manual.
- No way to tell, at a glance, which businesses on Maps are worth walking into versus ones that already have a booking system and aren't a fit.
- "Has a website" isn't the same as "doesn't need Lexi", plenty of local sites are a static page with no booking, that distinction currently requires opening every site by hand.

---

## Integration Type

**Classification:** Script
**Reasoning:** This is a workspace tool Theo (or Claude, on his behalf) runs on demand to produce a list, not something that needs to auto-load context every session (not a Skill) and not a single-prompt slash command (it needs real logic: two API calls, a scoring pass, a CSV writer). It follows the exact shape of `scripts/firecrawl_tool.py`.
**Location:** `scripts/lead_scraper.py`, using the existing `.claude/skills/apify` and `.claude/skills/firecrawl` integrations rather than duplicating their API logic.
**Auto-discovery:** N/A, it's a script, invoked directly (`uv run python scripts/lead_scraper.py ...`) or via a Claude session reading this plan.

---

## Proposed Changes

### Summary of Changes

- Add `scripts/lead_scraper.py`: takes a vertical (e.g. "hair salon") and a suburb list, runs the Apify Google Maps actor, then Firecrawl-checks every result that has a website for a booking link, scores and ranks the results, writes a CSV.
- Add a small config file mapping vertical name to the search terms Maps actually responds well to (e.g. "hair salon" needs to search "hair salon Bellville", "hair salon Parow", one query per suburb, not one combined query).
- Output lands in `outputs/leads/YYYY-MM-DD-{vertical}-{suburb-or-all}.csv`.
- Document the tool in `context/ideas.md` (move from "parked" to "built") and add a short usage note to `context/business.md` or a new `docs/` entry once proven, so future sessions know it exists.

### New Files to Create

| File Path | Purpose |
|-----------|---------|
| `scripts/lead_scraper.py` | The CLI tool: runs Maps search, checks websites for booking links, scores, writes CSV. |
| `scripts/lead_scraper_verticals.json` | Search-term mapping per vertical (e.g. `"hair salon": ["hair salon", "hairdresser", "hair boutique"]`), so new verticals are a config edit, not a code change. |
| `outputs/leads/.gitkeep` | Placeholder so the output folder exists and is tracked, individual run CSVs are the actual outputs. |

### Files to Modify

| File Path | Changes |
|-----------|---------|
| `context/ideas.md` | Move the "Lead scraper agent" entry from parked framing to "built, see scripts/lead_scraper.py", once Step 5 (first real run) passes. |
| `.env.example` | Confirm `APIFY_API_TOKEN` is documented (it already should be, per the apify skill's self-setup note), add a one-line comment pointing at this script as a consumer. |
| `ledger/theo.md` | Row per meaningful step, as the workspace's standing rule requires. |

### Files to Delete (if any)

None.

---

## Design Decisions

### Key Decisions Made

1. **A script, not a skill**: this is a tool that gets run with specific arguments (vertical, suburbs) to produce a specific output, not something that should auto-load into every session's context. Matches `scripts/firecrawl_tool.py` and `scripts/gmail_tool.py`'s existing pattern.
2. **Reuse the Apify and Firecrawl skills' API patterns rather than building new HTTP clients from scratch**: `get_env()` for keys, the same error-handling shape as `firecrawl_tool.py`, so this tool feels like it belongs in the workspace, not bolted on.
3. **Vertical config as a separate JSON file, not hardcoded**: `context/business.md` already lists a dozen future verticals. A new vertical should mean adding a few search terms to a config file, not touching the script's logic.
4. **CSV to `outputs/leads/`, not straight into Google Sheets**: keeps the first version simple and reviewable (Theo can open the CSV, sanity-check it, delete junk results, before it ever touches his live prospect tracker). Pushing straight to Sheets is a natural Phase 2 once the scoring is trusted, `context/tech-stack.md` confirms Sheets is already reachable via the Drive connector.
5. **Two-pass check, not just "has a website"**: a business having a website says nothing about whether it takes bookings online. The Firecrawl pass specifically looks for booking-related signals (a "Book Now" link, an embedded Calendly/Fresha/booking widget, a "make an appointment" call to action) so the ranking reflects the actual sales angle: no online booking, not no website.
6. **Suburb-by-suburb queries, not one broad search**: Google Maps search results are locality-biased and cap out around 20-60 results per query depending on the actor's settings, one query per suburb per vertical gets fuller, more locally accurate coverage than one big search for "hair salon Cape Town."

### Alternatives Considered

- **A general web search instead of Apify's Maps actor**: rejected, Google Maps listings are the closest thing to a structured local-business directory with phone numbers and websites already attached, a general search would need far more cleanup.
- **Skipping the Firecrawl booking-check pass, just using "has no website" as the filter**: rejected, too many real prospects have a static website with no booking system, filtering on website-existence alone would miss a big chunk of the actual target market (this matches the request's own framing: the pain point is no booking system, not no website).
- **Building this as a Skill that auto-triggers on "find me leads"**: considered, but a script Theo (or Claude) runs deliberately with clear arguments is more predictable and controllable for something that spends Apify/Firecrawl credits, worth revisiting as a skill once the scoring logic is proven and trusted.

### Open Questions

- **Exact Apify actor input shape**: `apify/google-maps-scraper`'s input fields (search terms, location, result limit, language) need to be confirmed against the actor's store page at build time, per the apify skill's own instruction to fetch the page if unsure. Not a blocker, just needs doing during implementation, not guessed here.
- **Credit budget per run**: Apify and Firecrawl are both pay-as-you-go. Worth estimating cost for, say, a 4-suburb x 1-vertical run (roughly 100-200 Maps results, a subset of those needing a Firecrawl check) before the first real run, and saying that number to Theo rather than assuming it's negligible.
- **Booking-system detection accuracy**: "does this site have a booking link" is a heuristic (looking for known booking-platform patterns and phrases), not a certainty. Worth a manual spot-check of the first run's results before trusting the ranking fully.

---

## Step-by-Step Tasks

### Step 1: Confirm Apify is actually usable in this session

**Actions:**
- Check `.env` for `APIFY_API_TOKEN`. If missing, walk through the apify skill's self-setup flow (sign up, get token from Console → Settings → Integrations, add to `.env`).
- Confirm `api.apify.com` is reachable from this environment's network policy, the same way Firecrawl's `api.firecrawl.dev` needed adding earlier this week, if this is a fresh container, check the environment's network access setting.

**Files affected:**
- `.env` (not committed)

---

### Step 2: Confirm the Google Maps actor's real input shape

**Actions:**
- Fetch `apify/google-maps-scraper`'s store page (or run a tiny test call) to confirm the exact input JSON field names for: search term, location/coordinates or address text, result limit, language.
- Run one small test query (a single suburb, low result limit) to see real output field names (name, address, phone, website, rating, review count, category) before writing the parsing code.

**Files affected:**
- None yet (research step)

---

### Step 3: Build `scripts/lead_scraper_verticals.json`

**Actions:**
- Create the vertical-to-search-terms mapping, starting with hair salons: `{"hair salon": {"terms": ["hair salon", "hairdresser", "hair boutique", "hair studio"], "suburbs": ["Bellville", "Mitchell's Plain", "Parow", "Goodwood"]}}`.
- Leave room for the next verticals from `context/business.md` (med spa, dog groomer, cleaning business) as additional keys, don't build them yet, just structure the file so adding them later is a config edit.

**Files affected:**
- `scripts/lead_scraper_verticals.json` (created)

---

### Step 4: Build `scripts/lead_scraper.py`

**Actions:**
- CLI interface: `uv run python scripts/lead_scraper.py --vertical "hair salon" [--suburbs Bellville,Parow] [--limit 50]`.
- For each suburb, call the Apify Maps actor (via `run-sync-get-dataset-items` for a first pass, small enough not to need async polling), collect results.
- De-duplicate by phone number or exact name+address (Maps sometimes returns near-duplicates across suburb queries when areas border each other).
- For each result that has a website URL, call Firecrawl's `scrape` endpoint (via the existing `FirecrawlClient` pattern from `scripts/firecrawl_tool.py`, import and reuse it rather than re-implementing) and check the returned markdown for booking signals: links or text containing "book", "appointment", known platform names (Calendly, Fresha, Square, SimplyBook, Setmore, Booksy).
- Score each result: no website scores highest, website with no detected booking signal scores next, website with a booking signal scores lowest (deprioritised, they're less of a fit). Within each tier, sort by review count descending (more reviews suggests a more established, better-resourced business worth the outreach effort).
- Write results to `outputs/leads/{date}-{vertical}-{suburbs}.csv` with columns: `name, phone, address, suburb, rating, review_count, has_website, website_url, has_booking_signal, score_tier`.
- Print a plain-English summary at the end: how many found, how many in each score tier, roughly how many Apify/Firecrawl calls were spent.

**Files affected:**
- `scripts/lead_scraper.py` (created)

---

### Step 5: First real run and manual validation

**Actions:**
- Run for hair salons across the four core suburbs.
- Open the resulting CSV, spot-check 5-10 rows against the real Google Maps listing and the real website (where one exists) to confirm the booking-signal detection is reasonably accurate.
- Report the credit cost actually incurred (Apify run + Firecrawl scrape count) to Theo, so future runs have a real cost reference instead of an estimate.

**Files affected:**
- `outputs/leads/{date}-hair-salon-*.csv` (created)

---

### Step 6: Document and log

**Actions:**
- Update `context/ideas.md`'s lead scraper entry to reflect it's built and where (`scripts/lead_scraper.py`), with a one-line usage example.
- Write ledger rows as each step completes, not batched at the end.

**Files affected:**
- `context/ideas.md`
- `ledger/theo.md`

---

## Connections & Dependencies

### Files That Reference This Area

- `context/ideas.md` already has the "Lead scraper agent" entry this plan formalises.
- `context/business.md` is the source of truth for target suburbs and vertical priority order, the vertical config file should stay in sync with it as new verticals get added.
- `outputs/2026-09-27-lexi-walkin-pitch.md`, the walk-in pitch script this tool feeds targets to.

### Updates Needed for Consistency

- Once proven, worth a `/document` pass so `docs/_index.md` gets a row pointing future sessions at this script, matching the workspace's own rule ("Build something new, create a doc and add a row").

### Impact on Existing Workflows

- None on Lexi or any live client system, this is a standalone research/outreach tool.
- Adds ongoing Apify and Firecrawl credit spend whenever it's run, worth keeping an eye on via each tool's own usage dashboard.

---

## Validation Checklist

- [ ] `APIFY_API_TOKEN` confirmed working in this environment
- [ ] Apify Maps actor's real input/output shape confirmed against its store page, not guessed
- [ ] `scripts/lead_scraper_verticals.json` created with hair salon terms and the four core suburbs
- [ ] `scripts/lead_scraper.py` runs end to end for at least one vertical/suburb combination
- [ ] Output CSV has all required columns and sensible values (no blank names, phone numbers look like real SA numbers)
- [ ] Booking-signal detection spot-checked against 5-10 real websites for accuracy
- [ ] Real credit cost for one run reported to Theo
- [ ] `context/ideas.md` updated to reflect the built tool

---

## Success Criteria

The implementation is complete when:

1. Running the script for "hair salon" across Bellville, Mitchell's Plain, Parow and Goodwood produces a ranked CSV with no-website and no-booking-system prospects sorted to the top.
2. A manual spot-check of 5-10 results confirms the booking-signal detection is accurate enough to trust (not necessarily perfect, but not misleading).
3. Theo can hand this CSV straight to the walk-in pitch process, or paste rows into his existing Google Sheet prospect tracker, without needing to research each business by hand first.
4. Adding a second vertical (e.g. dog groomers) is a config-file edit to `scripts/lead_scraper_verticals.json`, not a code change.

---

## Notes

- This is explicitly Phase 1 (CSV output, hair salons only, manual review before use). Phase 2 ideas, not part of this plan: auto-pushing results straight into a Google Sheet via the Drive connector, expanding to the next verticals `context/business.md` flags, and possibly a lightweight dedup pass against Theo's existing 20-salon list so re-runs don't resurface businesses already contacted.
- Keep an eye on Apify and Firecrawl spend, both are pay-as-you-go; this tool should make outreach faster, not quietly expensive. Report real costs after the first run rather than assuming the estimate holds.
- Worth revisiting whether this becomes a Skill (auto-triggering on "find me leads for X") once the scoring logic has proven itself over a few real runs, consistent with how `new-capability` and other tools in this workspace graduate from script to skill once trusted.

---

## Implementation Notes

**Implemented:** 2026-09-27

### Summary

Built `scripts/lead_scraper.py` and `scripts/lead_scraper_verticals.json` (hair salon, four core suburbs). The script runs the Apify Google Maps actor across suburb/term combinations, de-duplicates by phone or name+address, checks any listed website with Firecrawl for booking-platform signals (a small hardcoded list: "book now," Calendly, Fresha, Booksy, Setmore, and others), scores into three tiers (no website / website no booking / website with booking), and writes a ranked CSV to `outputs/leads/`. CLI help text and argument parsing verified working. The missing-key failure path was verified: it produces a clean, plain-English message and exit code 1, not a stack trace. `.env.example` got a one-line pointer to this script as a consumer of `APIFY_API_TOKEN`.

### Deviations from Plan

- Built a small purpose-specific `FirecrawlBookingChecker` class inside `lead_scraper.py` rather than importing `FirecrawlClient` from `firecrawl_tool.py` directly. Reason: this script only needs one call shape (scrape a URL, check its text for booking signals) and importing the CLI-oriented `FirecrawlClient` would couple this script to that file's error-handling conventions for no real benefit. Both hit the same Firecrawl `/scrape` endpoint.
- Could not complete Step 2 (confirming the Apify Google Maps actor's exact input/output field names against a live call) or Step 5 (a real run and manual validation), because this container's network policy was blocking `api.apify.com`, and no `APIFY_API_TOKEN` exists in this fresh session. The field names used (`searchStringsArray`, `title`, `website`, `totalScore`, `reviewsCount`, etc.) are the actor's documented shape as of writing, not verified live. A `--raw-sample` flag was added specifically so the first real run can confirm or correct these without needing to re-read the script.

### Issues Encountered

- `api.apify.com` denied by this environment's network policy (same class of issue Firecrawl hit earlier this session). Theo needs to add it under the environment's network settings.
- No `APIFY_API_TOKEN` in this fresh container's `.env` (private/machine-local files don't sync between sessions, documented workspace behaviour). Theo needs to add his Apify token via the environment's settings.
- Both are environment-setup steps outside this script's own code; nothing in the script itself is blocked once those are sorted.
