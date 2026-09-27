# Ideas, parked

> Someday/maybe. Not active, not scoped, not forgotten. Revisit when the current priority (Lexi rebuild, founding clients) has room to spare.

## AI email assistant for the day-job receptionist

An assistant to sort supplier emails and draft purchase orders at the boilermaking day job. Separate from anything Uncle T Agency sells, this is internal tooling for Theo's own workplace, not a client product.

## The Turkish businesswoman lead (via Nita)

Referred in through Nita. Runs a tour company, restaurants, and rentals. Two separate needs surfaced: her businesses could use the same booking/WhatsApp automation Uncle T Agency sells, and she also wants an honest bookkeeper, which isn't something the agency currently offers. Worth a conversation to find out which one she actually wants solved first.

## AIOS-as-a-service

Once this context/ledger workspace system is proven on Uncle T Agency itself, package the same setup for other small business owners, starting with Nita's cleaning business as the first real test case beyond Theo's own. A second product line sitting alongside Lexi, not a replacement for it.

## Lead scraper agent, built (27 Sept 2026)

No longer an idea, it's a real tool now: `scripts/lead_scraper.py`, see `docs/lead-scraper-agent.md`. Needs `APIFY_API_TOKEN` and `api.apify.com` added to the environment's network settings before its first live run.

## Lexi Voice, moved to active (27 Sept 2026)

No longer parked. Theo wants to build this now rather than wait for the first paying client, on the theory that a working voice demo helps close deals before the December target (5 paying clients), not just after. Full plan: `plans/2026-09-27-lexi-voice-receptionist.md`.

Shape of it: a separate Make scenario (not added to the main 146-module Lexi scenario), Retell as the voice platform, connected over the WhatsApp Business Calling API on Chales' existing number (free for calls the client makes, SIP already available). Reuses Lexi's proven calendar-check and booking-write logic. Tested on the demo number first, Chanté's live number never touched until proven.

Research from 25 Sept 2026 still holds: `reference/research/2026-09-25-lexi-voice.md`. BizAI already sells a SA voice receptionist at R999/month, so this positions as a Lexi upgrade, not a standalone product.
