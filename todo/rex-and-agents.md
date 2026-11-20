# Rex and the other agents

Org chart: `plans/2026-10-26-agent-team-org-chart.md`. Principle: nothing sends to outsiders without Theo.

## Rex (Theo's assistant)
Live on Telegram as @UncleTRex2bot (Make 8428548): chat with the business brain, web search, reminders as Google Calendar events, memory in the "Rex Memory" sheet. Arsenal fixtures come from the Sky calendar feed. Code and prompts: `apps/rex/`.
- [ ] Test Rex memory ("remember ..." then ask about it) and search plus reply follow-up. Both were untested
- [ ] Activate Rex's SIM (063 647 6860), still not activated
- [ ] Get Rex onto WhatsApp: needs a free Meta number slot or business verification. 13 Nov plan: `plans/2026-11-13-rex-live-day.md`
- [ ] Rotate Rex's keys (security.md)
- [ ] Later: memory, search and handing work to the other agents

## Chief of Staff (daily brief)
Playbook: `apps/chief-of-staff/PLAYBOOK.md`. Reads Make, the Pipeline Sheet, Gmail, Calendar and this repo, writes a brief to `outputs/briefs/`. Read only, never messages anyone.
- [ ] The scheduled brief has no Google Sheets access. Fix the scheduled task
- [ ] Make it read `todo/README.md` (done in this merge) and add Chales' review and booking alert scenarios to its watch list
- [ ] Add each client's scenario ID the day they go live

## Scout and outreach
- [ ] Scout (`scripts/lead_scraper.py`, `apps/lead-finder/`) needs `GOOGLE_PLACES_API_KEY`. Apify's free $5 monthly credit is used up
- [ ] outreach-writer drafts messages from the Pipeline Sheet. Run it daily
- [ ] Rebuild the scheduled lead task with Sheets attached

## Agents not yet built
- [ ] Delivery agent: at client one (use `/lexi-onboarding`)
- [ ] Reply Helper: when the first salon replies
- [ ] Monthly client report, review request, rebooking nudge, website uptime check
- [ ] Host guest assistant and host direct booking (see nita.md)
