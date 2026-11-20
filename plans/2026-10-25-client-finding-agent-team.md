# Plan: Client-finding agent team (Scout, Writer, Reply Helper, Strategist) run through Rex

**Created:** 2026-10-25
**Status:** Draft
**Request:** Build our own version of the "Harvey" sales agent, focused on salons, spas and similar Cape Town businesses, that works without Theo's laptop being on at night.
**Purpose:** Get Theo in front of more local business owners every week, with the boring work (finding, researching, drafting, tracking) done for him, so his only jobs are approving, sending and closing.

---

## Overview

### What This Plan Accomplishes

Builds a small team of single-job agents on top of what already exists: the lead scraper finds the businesses, a Writer agent drafts one personal message per business using one real detail about them, a Reply Helper drafts answers when they reply, and a Strategist reports weekly what is working. Rex on WhatsApp is the front door: Theo asks Rex for today's leads, taps a link to send each message from his own WhatsApp, and tells Rex how it went.

### Why This Matters

Strategy goal: 3 paying recurring clients in 90 days, 5 by December. The bottleneck is conversations, not software. This puts 10 well-aimed conversations a day within reach while Theo works a day job, and it runs in the cloud (Make.com + Claude API), so it doesn't depend on his laptop. It also copies the parts of Harvey that matter (one real detail per message, human approval, stop on opt-out) without installing code nobody has reviewed.

---

## Current State

### Relevant Existing Structure

- `scripts/lead_scraper.py` + `scripts/lead_scraper_verticals.json` + `docs/lead-scraper-agent.md`: Apify Google Maps search plus a Firecrawl booking-system check, ranked A/B/C into a CSV in `outputs/leads/`. Built 27 Sept. Only the "hair salon" vertical is configured. Needs `APIFY_API_TOKEN` and `api.apify.com` allowed in the environment.
- Rex: Make scenario 7638753, live on Meta's test number, answers Theo only. Has no memory, no internet, no Sheets log and no way to call other agents. Prompt in `apps/rex/system-prompt.md`. Never save this scenario in Make's editor (it breaks `max_tokens`); edit via the API.
- `outputs/2026-09-27-lexi-walkin-pitch.md`: the in-person pitch and tone to match.
- `.claude/skills/web-builder`: builds the sites that sell the R1,499 offer.
- `context/offer.md`, `context/strategy.md`, `context/business.md`: offer, pricing (R1,499 + R499/month), priority verticals.
- Warm leads: Zanzibar, Sistergirl, Reeva, JEM, Jason (tattoo artist).

### Gaps or Problems Being Addressed

- Scout output is a CSV that nobody works. No pipeline, no status, no follow-up date.
- Nothing writes the first message, so each approach starts from a blank page.
- Replies land on Theo's personal WhatsApp with nobody tracking them.
- No weekly view of what is working.
- Rex can't read or write any of this (no memory, no Sheet access).
- Harvey itself doesn't fit: it needs a machine that stays on, is built for email (salon owners live on WhatsApp and Instagram), and ships US legal defaults.

---

## Integration Type

**Classification:** Mixed: Script (Scout, existing), Make.com scenarios (Writer, Rex actions, Strategist), prompt files, one Google Sheet.
**Reasoning:** Anything that must run while Theo's laptop is off has to live in Make + Claude API. Prompts live in the repo so they stay versioned and match what's live. The Sheet is the shared pipeline, the same pattern Rex's old log used.
**Location:** `apps/agents/` (prompts, README, blueprint copies), Make scenarios, one Google Sheet "Uncle T Pipeline", docs in `docs/client-finding-agents.md`.
**Auto-discovery:** `docs/_index.md` row: "finding clients, outreach, pipeline, Scout, Writer, Rex leads".

---

## Proposed Changes

### Summary of Changes

- One Google Sheet, "Uncle T Pipeline", is the single source of truth (tabs: Leads, Messages, Replies, Weekly).
- Scout: add verticals (med spa, nail tech, barber, lash and brow, dog groomer), push each run into the Leads tab, and add one "real detail" per lead (review quote, rating, Instagram line, no booking link).
- Writer: a Make scenario that turns each new lead into a short personal WhatsApp message plus a walk-in opener, written in Theo's voice, with an opt-out line.
- Rex becomes the router: understands "leads", "sent <name>", "reply <name>: <text>", "won <name>", "week" and reads/writes the Sheet.
- Reply Helper: drafts a reply to a prospect's message for Theo to send.
- Strategist: weekly summary from the Sheet, delivered when Theo asks Rex "week".
- Rex gets short-term memory (last few messages).
- Optional later: internet search for Rex, Instagram detail via Apify, proactive daily digest after Meta verification.

### New Files to Create

| File Path | Purpose |
|-----------|---------|
| `apps/agents/README.md` | How the team fits together, what runs where, how to change it |
| `apps/agents/writer-prompt.md` | System prompt for the Writer (message rules, banned phrases, one real detail, opt-out line) |
| `apps/agents/reply-helper-prompt.md` | System prompt for the Reply Helper (objections, price, "send me info", "not interested") |
| `apps/agents/strategist-prompt.md` | System prompt for the weekly summary |
| `apps/agents/rex-router-prompt.md` | Intent parser: turns Theo's WhatsApp text into one JSON action |
| `apps/agents/sheet-schema.md` | Exact columns for each tab |
| `docs/client-finding-agents.md` | How to run the team day to day |
| `plans/2026-10-25-client-finding-agent-team.md` | This plan |

### Files to Modify

| File Path | Changes |
|-----------|---------|
| `scripts/lead_scraper_verticals.json` | Add med spa, nail tech, barber, lash and brow, dog groomer with Cape Town suburb lists |
| `scripts/lead_scraper.py` | Add a `real_detail` column (rating, review count, a short public review line, Instagram/website note) and an optional `--sheet` push |
| `apps/rex/system-prompt.md` and Make scenario 7638753 | Add router behaviour and memory via API update |
| `docs/_index.md` | New row for the agent team |
| `CLAUDE.md` | Add `apps/agents/` to the map and tool routing |
| `context/strategy.md` | Note the agent team as the way to the 3-client target |
| `context/tech-stack.md` | Add the Pipeline Sheet and new Make scenarios |

### Files to Delete (if any)

None.

---

## Design Decisions

### Key Decisions Made

1. **Our own build, not Harvey:** Harvey needs an always-on machine, is email-first and uses US legal defaults. Our targets are WhatsApp-first. We copy its good rules instead of running unread code.
2. **Human sends every first message:** Meta bans numbers for cold WhatsApp from a business number, and the same discipline protects Theo's personal number. The team drafts, Theo sends from his own phone with a tap-to-send `wa.me` link carrying the drafted text.
3. **Rex is the front door, the Sheet is the memory:** Theo only ever talks to Rex. Everything else reads and writes the Sheet.
4. **Cloud for the always-on parts:** Make scenarios on a schedule and on triggers. Scout stays a session-run script at first and moves to Make once the weekly routine is proven.
5. **One real detail per message:** the single biggest reason Harvey's messages don't read as spam. Enforced in the Writer prompt and checked before a draft is marked ready.
6. **Cap at 10 new conversations a day:** quality over volume, and it protects Theo's number and time.
7. **Claude API, not the Pro plan:** the Pro plan can't power cloud automations. The API is billed per use. At this volume it should cost very little, but Phase 1 will measure the real figure before anything runs daily.

### Alternatives Considered

- **Install Harvey as is:** rejected (above).
- **Everything inside Claude Code sessions:** fine for building, but nothing runs while Theo sleeps.
- **Cold email as the main channel:** rejected for salons and spas (many have no site or inbox). Email stays an option for businesses with websites needing a rebuild.
- **Fully automatic sending:** rejected until the approach is proven and the legal position is checked.

### Open Questions (if any)

1. **Make plan limits:** how many operations per month does Theo's Make plan allow? The plan assumes a few hundred per day.
2. **POPIA / direct marketing:** one personal message to a business owner is normal practice, but the rules on unsolicited electronic marketing need checking. Theo should confirm with a professional before volume goes up. The Writer prompt will include a clear opt-out line either way.
3. **Which channel first:** WhatsApp from Theo's own number, Instagram DM, or walk-in with the drafted opener? Default: WhatsApp for those with a number, walk-in script for the rest.
4. **Anthropic API budget:** set a monthly cap in Anthropic's console.
5. **Rex's key rotation:** both keys seen in chat get rotated before this goes live.

---

## Step-by-Step Tasks

### Step 1: Create the Pipeline Sheet

Create a Google Sheet "Uncle T Pipeline" in Theo's Drive with four tabs and the columns in `apps/agents/sheet-schema.md`.

**Actions:**

- Leads: id, date_found, vertical, business, suburb, phone, website, instagram, rating, reviews, tier (A/B/C), real_detail, status (new, drafted, sent, replied, call, won, lost, opted_out), next_action_date, notes
- Messages: lead_id, channel, draft, wa_link, created, sent_on
- Replies: lead_id, reply_text, intent, draft_answer, date
- Weekly: week_start, found, sent, replies, calls, won, notes
- Share only with Theo.

**Files affected:**

- `apps/agents/sheet-schema.md`

---

### Step 2: Upgrade Scout

Make Scout produce a `real_detail` and load results into the Leads tab.

**Actions:**

- Add verticals to `scripts/lead_scraper_verticals.json` (med spa, nail tech, barber, lash and brow, dog groomer) with Cape Town suburbs from `context/business.md`.
- Extend `lead_scraper.py` to carry rating, review count and one short public detail per business, with Instagram handle if the listing has one.
- First live run with `--raw-sample` to confirm Apify's real field names (the 27 Sept build never saw a live call).
- Load the CSV into the Leads tab through the Google Sheets connector. Spot-check ranking on 20 rows.
- Needs first: `APIFY_API_TOKEN` in the environment's hidden credentials and `api.apify.com` allowed.

**Files affected:**

- `scripts/lead_scraper.py`, `scripts/lead_scraper_verticals.json`, `docs/lead-scraper-agent.md`

---

### Step 3: Write the agent prompts

Write the four prompts and review them with Theo before anything goes live.

**Actions:**

- `writer-prompt.md`: message under 60 words, one real detail, plain Cape Town voice, one question to end on, no AI phrases, no invented claims, opt-out line, no pricing in the first message. Output: WhatsApp message plus a 2-line walk-in opener.
- `reply-helper-prompt.md`: handle interest, price, "send info", "not now", "not interested", "stop". Any opt-out wording sets status opted_out and is never contacted again.
- `strategist-prompt.md`: weekly numbers, what worked, one recommendation, plain English, Rand.
- `rex-router-prompt.md`: return strict JSON `{action, lead, text}` for leads / sent / reply / won / lost / week / chat.
- Apply `reference/writing-style.md` to all of them.

**Files affected:**

- `apps/agents/*.md`

---

### Step 4: Build the Writer scenario in Make

A scheduled scenario that drafts messages for new leads.

**Actions:**

- Trigger: every hour, read Leads rows where status = new and tier A or B, max 10 per day.
- Claude API call with the Writer prompt and the row's data. Use the API key header and the Data-structure input method (it escapes text safely).
- Write the draft and a `https://wa.me/<number>?text=<url-encoded draft>` link to the Messages tab, set status = drafted.
- Create and edit through the API, not Make's editor.

**Files affected:**

- Make scenario (new), `apps/agents/blueprints/writer.json`

---

### Step 5: Upgrade Rex into the router

**Actions:**

- Add the router prompt and a short memory (last 6 messages from a Rex log tab) to scenario 7638753.
- Router branches: `leads` reads today's drafted rows and replies with up to 5 business names, one-line detail and the tap-to-send link each; `sent <name>` marks the lead sent and sets a follow-up date 3 days out; `reply <name>: <text>` calls the Reply Helper and returns a draft; `won` / `lost` update status; `week` runs the Strategist; anything else is normal chat.
- Keep the owner-number filter. Keep the 24-hour reply window in mind: Rex answers when Theo messages first.
- Re-test the max_tokens number type after every API update.

**Files affected:**

- `apps/rex/system-prompt.md`, scenario 7638753, `apps/agents/rex-router-prompt.md`

---

### Step 6: Strategist and follow-ups

**Actions:**

- Weekly Make scenario (Sunday evening) reads the Sheet, writes a row to the Weekly tab and stores the summary so `week` can return it.
- Follow-up check: leads with status sent and next_action_date reached appear at the top of the next `leads` reply.

**Files affected:**

- Make scenario (new), `apps/agents/strategist-prompt.md`

---

### Step 7: Pilot with 10 real leads

**Actions:**

- Run Scout on hair salons in one suburb and one other vertical, load 20 rows.
- Theo sends 10 messages across two days using Rex's links, with the warm five handled by hand.
- Track sent, replies, calls. Tune the Writer prompt from real reactions.
- Record the Anthropic cost per message.

---

### Step 8: Document and ledger

**Actions:**

- Write `docs/client-finding-agents.md`, add the row to `docs/_index.md`, update `CLAUDE.md`, `context/strategy.md`, `context/tech-stack.md`.
- Ledger row for every Make scenario and file, per the standing rule.

---

## Connections & Dependencies

### Files That Reference This Area

- `docs/lead-scraper-agent.md`, `plans/2026-09-27-lead-scraper-agent.md`, `apps/rex/README.md`, `outputs/2026-09-27-lexi-walkin-pitch.md`, `context/business.md` (vertical priorities).

### Updates Needed for Consistency

- The Rex README gets a router section. The lead scraper doc says its Sheets push is planned: this plan delivers it.

### Impact on Existing Workflows

- Rex gains memory and actions, which changes what he can do. The live Chales scenario (5043763) and Lexi are untouched. The Web Builder is unaffected.

---

## Validation Checklist

- [ ] Sheet exists with the four tabs, shared only with Theo
- [ ] Scout run loads 20+ rows with a real_detail that is true when spot-checked
- [ ] Writer drafts for 5 sample leads: each under 60 words, one real detail, no invented facts, opt-out line present
- [ ] Rex `leads` returns the right names and working tap-to-send links
- [ ] `sent` and `won` update the Sheet correctly
- [ ] An opt-out reply sets status opted_out and that lead never reappears
- [ ] Rex still answers only Theo's number and `max_tokens` is a number after every update
- [ ] No keys written in the repo; Rexbot token and Anthropic key rotated
- [ ] Cost per message measured and under the cap Theo sets

---

## Success Criteria

1. Theo can message Rex "leads" and get up to 5 ready-to-send, personalised messages in under 20 seconds, with the laptop off.
2. 10 messages sent in the pilot, every one with a true personal detail.
3. At least one reply tracked end to end, from message to call booked.
4. The weekly summary shows real numbers and one concrete recommendation.
5. Running cost is known, small and capped.

---

## Notes

- Later: Instagram detail via Apify, internet search for Rex, a proactive daily digest once the business is verified and Rex moves to the real SIM, and email outreach for businesses whose websites need a rebuild (feeds the Web Builder).
- Harvey's good ideas kept: one real detail, short messages, stop on opt-out, human approval, daily cap, pre-send checks.
- Not legal advice: check POPIA direct-marketing rules before increasing volume.
- Order of work: agency website and Meta verification stay first. This team can start at Step 1 to 3 in parallel because they need no Meta access.
