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

## "Get Found" local visibility product (20 Nov 2026)

Idea, not live: sell Google Maps, Google and AI-search visibility (profile, service pages, reviews machine, monthly report) alongside Lexi, using CHALES as the proof. Starts with a free "Found Check" report as the lead magnet. Held back until CHALES shows real numbers (reviews, Maps position, bookings from Google, due end Jan 2027). Plan and pricing suggestions: `outputs/2026-11-20-get-found-offer.md`.
## Lexi Voice, edge and launch plan (3 Nov 2026)

See `plans/2026-11-03-voice-edge-and-launch-plan.md` and `reference/research/2026-11-03-voice-market-and-costs.md`. Voice alone is not a gap (8+ SA providers from R849/m); it works as part of one assistant across chat, voice notes and calls, priced under the market (Lexi + Voice about R1,298/m), aimed first at trades and clinics, and led by a free demo. Lexi Trade (voice note to quote PDF) is an unvalidated idea.

Update 3 Nov 2026: first voice product is now Lexi Talk (two-way voice notes on WhatsApp, tap or talk), see `plans/2026-11-03-lexi-talk-voice-note-conversations.md`. Live calls come after.
## Local visibility (Google + AI) as a paid service

Raised 20 Nov 2026. Theo thinks clients will pay to be found on Google and recommended by AI assistants, and wants CHALES as the proof: if she reaches page one for Bellville searches within 2 to 3 months, that's the case study. Can sell as an upsell to Lexi clients or as a separate service. The process is written up in `docs/local-visibility-playbook.md`; before/after tracking runs on `scripts/visibility_check.py` (CHALES baseline: `outputs/visibility/chales/2026-11-20.json`). Pricing and packaging not decided yet. Wait for CHALES results before selling it hard.
## Lexi for other trades (researched 2026-09-22)

After the 5 salons, not before. The overseas research (`outputs/research/2026-09-22-overseas-features-trades-and-salons.md`) suggests this order:

1. **Cleaning next.** Same booking engine as salons, clients rebook every week, and Nita's Rags to Riches can be the free pilot. Needs prices by rooms and extras, recurring bookings, and access notes (gate codes, security estates).
2. **Plumbers third, the bigger money.** Photo of the problem, rough quote, after-hours emergency triage, "on my way" message, invoice with a Yoco link, yearly geyser service reminder. Cape Town requires a plumbing COC on every property sale.
3. **Electricians fourth.** 90% the same as plumbers. Electrical COCs and yearly inverter checks, now that load shedding has stopped.

Medium salons (3 to 10 staff) get multi-stylist diaries, deposits and rebooking nudges from the Lexi 2.0 roadmap anyway.
