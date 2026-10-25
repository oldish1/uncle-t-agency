# Client-finding agents

Plan: `plans/2026-10-25-client-finding-agent-team.md`. Pipeline sheet schema: `apps/agents/sheet-schema.md`.

## What exists (25 Oct 2026)
- **Scout** (`scripts/lead_scraper.py`): runs live. Fixed on 25 Oct: the Apify actor is `compass~crawler-google-places` (the old name did not exist). Adds suburb, mobile/landline channel, WhatsApp number, a real detail line. Verticals: hair salon, barber, nail tech, lash and brow, beauty spa, dog groomer, across 10 suburbs.
- **Uncle T Pipeline** sheet with Leads, Messages, Replies, Weekly tabs. 24 Parow hair salons loaded (17 with no website, 11 with a mobile number).
- Not built yet: Writer, Reply Helper, Strategist, Rex router (see plan).

## Run Scout
```bash
uv run python scripts/lead_scraper.py --vertical "hair salon" --suburbs Parow --limit 30
```
Add `--skip-booking-check` to save Firecrawl credits. Then ask Claude to load the CSV into the Leads tab (new ids, status new).

## Daily routine (manual for now)
1. Pick 5 leads: tier A, channel whatsapp, highest reviews, status new.
2. Send the Lexi demo video with a short personal message that uses that lead's real_detail and an opt-out line.
3. Mark the lead sent with a next_action_date three days out. Log replies.

## Rules
- Theo sends every first message from his own phone. Never from a business API number.
- Anyone who says no, stop or similar: status opted_out, never contacted again.
- One true detail per message, nothing invented. Not legal advice: check POPIA direct-marketing rules before raising volume.
