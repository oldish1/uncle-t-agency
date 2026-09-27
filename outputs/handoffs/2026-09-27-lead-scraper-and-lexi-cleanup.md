# Handoff: lead scraper agent built, Lexi's loose ends closed, voice scoped

## What we were working on and why

Two threads tonight, both flowing from Theo's push to land 5 paying clients by December:

1. **Close out Lexi's remaining loose ends.** The 27 Sept membership/client-template session had actually landed on a stray, already-merged branch and never reached main, so this session started by pulling that work in, then fixing the two real bugs it left behind (the RENEW/final-wash staff alerts pointing at Lexi's own number instead of Chanté's, and a save error in the reminders scenario).
2. **Give Theo tools to find and close more clients**: a cold walk-in pitch script (any local salon, not just the five warm leads), a Lexi Voice build plan, and a lead scraper agent to automate the prospect-hunting he's been doing by hand.

## Where we got to

### Done and proven live
- **Lexi is fully done.** Booking, cancel, reschedule, membership tracker (balance/renew/wash deduction), appointment reminders, and both staff alerts (final-wash, RENEW) are all live and correct. Both alerts now point at Chanté's real WhatsApp number (`27814332756`), found and fixed live in Make with Theo, tracked down through a genuinely painful canvas-hunting session (see Gotchas). The reminders scenario also got a small cleanup: a dead `SetVariables` module that was blocking saves in Make's own editor was removed entirely (verified clean, 4 modules, still active, 17:00 daily schedule intact).
- **Walk-in pitch script**: `outputs/2026-09-27-lexi-walkin-pitch.md`. Pain-first, cold-visit-ready, no client names attached (Theo wants to walk into any local salon, not just the warm list). Includes the real demo number now (`076 492 4196`, Uncle T Demo), confirmed by Theo and recorded in `context/tech-stack.md`.
- **Lexi Voice, scoped**: `plans/2026-09-27-lexi-voice-receptionist.md`. Retell over Vapi to start, WhatsApp Business Calling on Chales' existing number (free, SIP already available), demo number only until proven, reuses the live scenario's booking logic in a new standalone Make scenario. Not built yet, deliberately meant for its own fresh session/branch.
- **Lead scraper agent, built**: `scripts/lead_scraper.py` and `scripts/lead_scraper_verticals.json` (hair salon vertical, Bellville/Mitchell's Plain/Parow/Goodwood). Searches Google Maps via Apify, de-dupes, checks any website found with Firecrawl for real booking-platform signals, ranks into three tiers (no website highest, website-no-booking next, website-with-booking deprioritised), writes a CSV to `outputs/leads/`. Documented in `docs/lead-scraper-agent.md`, `context/ideas.md` updated from parked to built.

### Not done — pick this up next
1. **The lead scraper's first real run hasn't happened.** Built and verified working up to the point of needing live API access: CLI parses clean, the missing-key error path is a plain message not a crash. Two environment blockers were found and Theo just fixed both live, in the environment's Edit screen:
   - `api.apify.com` added to allowed network domains.
   - `APIFY_API_TOKEN=<token>` added to the plain Environment variables box (the `.env`-format one, not the separate "API credentials" header-injection feature, which is for a different mechanism than this script uses).

   **This is the very next thing to do.** Run:
   ```
   uv run python scripts/lead_scraper.py --vertical "hair salon" --raw-sample
   ```
   The `--raw-sample` flag prints the first raw Apify result. Use it to confirm the field names in `lead_scraper.py` (`title`, `website`, `totalScore`, `reviewsCount`, `searchStringsArray`, etc.) actually match what Apify's `apify/google-maps-scraper` actor returns today, since this was built without a live test call (network was blocked at build time) — the plan's own Step 2 flagged this needs confirming, not assuming. If the field names are off, fix them in `lead_scraper.py`'s `run()` function where the raw items get mapped into rows.

   Then spot-check 5-10 rows of the output CSV against the real Google Maps listing and website, confirm the booking-signal detection looks reasonable, and report the real Apify/Firecrawl credit cost back so future runs have an actual number instead of an estimate.

2. **Lexi Voice hasn't been started.** Plan is ready (`plans/2026-09-27-lexi-voice-receptionist.md`), meant for its own fresh session: `/implement plans/2026-09-27-lexi-voice-receptionist.md`. Needs a Retell account (free trial credit available) before any build work.

3. **Firecrawl still needs a fresh check.** Its network fix (from the 25 Sept session, api.firecrawl.dev) carried over correctly (confirmed reachable earlier this session), but hasn't been exercised for real since. Worth a quick `uv run python scripts/firecrawl_tool.py status` early in the next session just to confirm it's still good, especially now that the same environment's settings have been touched again tonight.

## Gotchas for the next session

- **This session's actual work was originally on a different branch.** A previous session (membership tracker, client template, Firecrawl fix) had its PR merged from `claude/make-lexi-2-performance-a31ho0`, but kept getting pushed to after that merge, so 13 real commits never reached main. This session found and merged them in. Worth remembering: always check for stray unmerged branches before assuming a fresh session's branch has everyone's latest work, `git log --oneline origin/main..origin/<suspect-branch>` is the check.
- **The live "Chales Hair Boutique" Make scenario (5043763) is too large to push a full-blueprint edit through the MCP tool in one call** (~230K characters, ~65K tokens, confirmed by actually hitting an output limit trying it tonight). Any future edit to that scenario needs either a human doing it directly in Make's editor (slow but safe, this is how tonight's two number fixes actually landed), or a smarter chunked-push approach worth figuring out before attempting again blind.
- **Make's own scenario search (magnifying glass, inside the scenario editor, distinct from the org-wide "Grid" tool at grid.make.com) is the fastest way to find a module by content**, search for the literal string you're hunting (a stray number, a template name) rather than visually scanning the canvas. Grid can confirm which scenario something lives in but won't let you edit from there.
- **`.env` and `private/` never sync between sessions on this workspace** (by design, git-ignored, machine-local). Every fresh container needs Firecrawl and Apify keys re-added. The environment's own Edit screen (network access + Environment variables) is the right place now, not asking Theo to paste into `.env` by hand each time.
- **Two different "API credential" mechanisms exist in the environment settings**: the plain "Environment variables" box (`.env` format, readable by scripts via `os.environ`/`get_env()`) versus "API credentials" (header-injection into direct HTTP calls to named websites, value never readable by code or Claude). `scripts/lead_scraper.py` and `scripts/firecrawl_tool.py` both need the first kind.

## What to do next, in order

1. Run `uv run python scripts/lead_scraper.py --vertical "hair salon" --raw-sample`, confirm field names match, fix `lead_scraper.py` if they don't.
2. Spot-check the output CSV, report real credit cost to Theo.
3. Quick Firecrawl status check.
4. When Theo's ready: start a fresh session for Lexi Voice (`/implement plans/2026-09-27-lexi-voice-receptionist.md`).
5. Ongoing: Theo using the walk-in pitch script and, once proven, the lead scraper's output for real outreach toward the December target.
