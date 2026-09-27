# Handoff: lead scraper's Firecrawl key added, needs a fresh session to pick up

## What we were working on and why

Continuing straight on from the previous handoff (`outputs/handoffs/2026-09-27-lead-scraper-and-lexi-cleanup.md`): getting the lead scraper's first real run proven end to end, including the Firecrawl booking-signal check that splits businesses with a website into "no booking system" versus "already has one."

## Where we got to

### Done and proven live
- **Apify token fixed and confirmed working.** The token Theo had saved had two look-alike character swaps (0/O, O/Q) from an earlier screenshot paste, caught by curling Apify's own `/users/me` endpoint directly rather than trusting the script's error message alone. The corrected token is saved in this environment's Environment variables box.
- **The real actor-name bug found and fixed.** The original build used `apify~google-maps-scraper`, which doesn't exist on Apify. Swapped in `compass~crawler-google-places` (the standard Google Maps actor, 40M+ total runs), confirmed its input schema (`searchStringsArray`, `maxCrawledPlacesPerSearch`, `language`, `skipClosedPlaces`) matches the script exactly. Fixed in `scripts/lead_scraper.py` line 39.
- **First real run, booking check skipped** (no Firecrawl key yet at the time): 145 unique hair salons across Bellville, Mitchell's Plain, Parow, Goodwood. 88 with no website, 57 with one. Reeva Hair & Beauty Salon, one of the five warm leads, turned up organically with no website, a good sign the targeting works. Output: `outputs/leads/2026-09-27-hair-salon-all.csv`.
- **Firecrawl key added to this environment**, tonight, in the same Environment variables box as `APIFY_API_TOKEN`. First paste was missing the `FIRECRAWL_API_KEY=` prefix (just the bare `fc-...` value on its own line), caught from a screenshot and corrected. The corrected version (`FIRECRAWL_API_KEY=fc-b4bdd475b16146daad2bbc4bfd8d320e`) should now be saved.
- All of this is committed and pushed to `claude/lead-scraper-lexi-cleanup-iqki7h` (commit `7e5873d` plus the ledger rows from tonight).

### Not done, pick this up first

1. **The Firecrawl key hasn't been verified live yet.** Environment variable changes only take effect on a brand new session, not one already running, confirmed by testing: `uv run python scripts/firecrawl_tool.py status` still failed with "not set" in this session even after Theo saved the key. This is expected, not a bug. **First thing to do in the new session:**
   ```
   uv run python scripts/firecrawl_tool.py status
   ```
   If it reports the key is still missing, the save didn't take, double-check the Environment variables box shows a clean `FIRECRAWL_API_KEY=fc-...` line (no stray line breaks, no missing prefix) and ask Theo to re-save.

2. **Rerun the lead scraper with the booking check included**, once Firecrawl's status check passes:
   ```
   uv run python scripts/lead_scraper.py --vertical "hair salon"
   ```
   (No `--skip-booking-check` this time.) This should split the 57 "has a website" results from the earlier run into tier B (website, no booking found) and tier C (website, already has booking), instead of leaving them all unclassified.

3. **Spot-check 5-10 of the newly-classified website rows** against the real site, confirm the booking-signal detection (looks for "book now," "book an appointment," Calendly/Fresha/Booksy/SimplyBook/Setmore/Square/Acuity/Timify/Schedulicity mentions) isn't producing obviously wrong classifications.

4. **Report the real Firecrawl credit cost** for checking ~57 sites, so future runs have an actual number instead of an estimate. `docs/lead-scraper-agent.md` and the plan (`plans/2026-09-27-lead-scraper-agent.md`) both still say this is pending, update them once known.

## Gotchas for the next session

- **Environment variable and network changes never apply mid-session.** Confirmed twice tonight (Apify's network+token addition earlier, Firecrawl's key just now). Any future setup step like this always needs a fresh session to verify, don't waste time re-testing in the same one.
- **Screenshots of the Environment variables box are easy to mistype from.** Two separate errors happened tonight from the same source: a character-level OCR slip on the Apify token (0/O, O/Q) and a missing `KEY=` prefix on the Firecrawl line. When Theo shares a screenshot of this box, verify the exact string against the actual API before assuming it's right, a direct curl to the provider's own auth-check endpoint (Apify: `GET /v2/users/me?token=...`, Firecrawl: worth checking what `firecrawl_tool.py status` calls) is faster and more reliable than eyeballing a photo.
- **`.env` and `private/` never sync between sessions** on this workspace, this is by design, not a bug, documented in earlier handoffs too. Anything needed for a fresh container (Apify token, Firecrawl key, network allowlist) has to be set in this specific environment's own Edit screen, and it only takes effect on the next new session.

## What to do next, in order

1. `uv run python scripts/firecrawl_tool.py status`, confirm it reports the account (not "not set").
2. `uv run python scripts/lead_scraper.py --vertical "hair salon"` (full run, booking check included).
3. Spot-check 5-10 of the website-tier rows against the real sites.
4. Report the real Firecrawl credit cost to Theo, update `docs/lead-scraper-agent.md` and the plan's known-limitations section.
5. Once trusted: hand the CSV to Theo for outreach, or plan the Google Sheets push (Phase 2, not scoped yet).
6. Still separately queued, not part of this thread: Lexi Voice build (`plans/2026-09-27-lexi-voice-receptionist.md`), needs its own fresh session and a Retell account.
