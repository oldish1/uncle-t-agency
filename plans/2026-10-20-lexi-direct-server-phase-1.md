# Plan: Lexi Direct Server, Phase 1 (demo number only)

**Created:** 2026-10-20
**Status:** Draft
**Request:** Build Lexi 2.0 as our own server on Meta's WhatsApp Cloud API, hosted on Railway, proven on the Uncle T Demo number before anything else moves.
**Purpose:** Get Lexi under 20 seconds per booking with full control and no per-client platform fee, so paying clients can be onboarded.

---

## Overview

### What This Plan Accomplishes

Builds `apps/lexi-server/`, a small Node.js server that receives WhatsApp messages from Meta, runs the tap-based booking flow (book, cancel, reschedule), reads and writes a Google Calendar and tracking sheet, and replies. It is deployed on Railway and attached to the Uncle T Demo number (+27 76 492 4196) only. Chales' live Make scenarios are not touched.

### Why This Matters

`context/lexi.md` sets the rule: no paying client is onboarded until Lexi replies in under 20 seconds, and today a booking takes about 2.5 minutes on Make. Strategy puts Lexi first, and the December target is 5 paying clients. This plan removes the blocker and also removes any Kapso-style per-number platform fee, since one server serves every salon from one config file each.

---

## Current State

### Relevant Existing Structure

- `plans/explore-2026-10-20-lexi-direct-server.md`: the approved concept this plan implements (decisions made 2026-10-20).
- `context/lexi.md`: current Lexi behaviour, flow rules, Chales services and hours, the Make router-fallback lesson.
- `plans/client-template.md`: the Make-based per-client onboarding this replaces for new salons.
- `plans/2026-10-14-personal-assistant-agent.md`: same webhook pattern (handshake, signature check, intake). It is a separate system with its own number, Meta app, host and keys. Nothing is shared.
- `scripts/google_auth.py`, `scripts/calendar_tool.py`: existing Google access (personal OAuth, not a service account). Not reused by the server; the server uses a service account.
- `apps/tt-engineering/`: precedent for an app folder with its own `package.json` (Node, ES modules).
- `context/tech-stack.md`: lists WhatsApp, Make, Netlify and the demo number. Needs Railway and the service account added.
- `reference/getting-keys.md`: key-by-key walkthrough format Claude uses with Theo.

### Gaps or Problems Being Addressed

- Booking takes about 2.5 minutes on Make (too many sequential modules).
- Make blueprints are hard to edit safely (router fallback by position, a ~230K-character scenario that could not be pushed through the API).
- No automated tests exist for Lexi's conversation logic.
- Each new salon needs 30 to 45 minutes of manual Make set-up.
- No cancel or reschedule in the original design; it was bolted on later.

---

## Integration Type

**Classification:** Script/app (a standing server).
**Reasoning:** It runs on its own host with code, tests and deployment, so it is neither a skill nor a command.
**Location:** `apps/lexi-server/` (code), `apps/lexi-server/salons/` (one config file per salon).
**Auto-discovery:** n/a. An "add a salon" command can follow once Phase 1 is proven (not in this plan).

---

## Proposed Changes

### Summary of Changes

- New Node.js server `apps/lexi-server/` with webhook, flow engine, calendar/sheet access, Claude intent step, SQLite memory, test kit.
- New demo salon config for the Uncle T Demo number, with its own demo Google Calendar and sheet.
- Railway deployment with spending cap, Meta webhook pointed at it for the demo number.
- Speed and correctness proof on the demo number.
- Context, key-guide and map updates, plus a `/document` page.

### New Files to Create

| File Path | Purpose |
|-----------|---------|
| `apps/lexi-server/package.json` | Node 20, ES modules. Dependencies: `express`, `better-sqlite3`, `googleapis`, `@anthropic-ai/sdk`. Scripts: `start`, `test`, `simulate`. |
| `apps/lexi-server/.env.example` | Names of every variable, no values (see Step 1). |
| `apps/lexi-server/.gitignore` | Ignores `.env`, `data/`, `node_modules/`. |
| `apps/lexi-server/README.md` | What it is, how to run it locally, how to add a salon. |
| `apps/lexi-server/src/server.js` | Express app: GET `/webhook` (Meta handshake), POST `/webhook` (signature check, immediate 200, then process), GET `/health`. |
| `apps/lexi-server/src/whatsapp.js` | Send text, reply buttons, list messages, image with caption and button. Parse inbound messages (text, button/list replies, audio, other). |
| `apps/lexi-server/src/salons.js` | Load all `salons/*.json`, look up by phone number ID, validate required fields at startup. |
| `apps/lexi-server/src/store.js` | SQLite: `processed_messages`, `sessions`, `bookings`, `message_log`. |
| `apps/lexi-server/src/flow.js` | The conversation state machine (see Step 5). Pure functions: given session + message, return the next state and the messages to send. |
| `apps/lexi-server/src/slots.js` | Builds day and time lists from salon hours plus calendar busy times. Handles the 10-row list limit (see Design Decisions). |
| `apps/lexi-server/src/calendar.js` | Google Calendar via service account: free/busy, create, find, delete, move event. |
| `apps/lexi-server/src/sheet.js` | Google Sheets via service account: append and update booking rows. |
| `apps/lexi-server/src/intent.js` | One Claude call returning JSON `{intent, service, day, time}` for typed free text. Strict schema, safe fallback to the menu on any failure. |
| `apps/lexi-server/salons/uncle-t-demo.json` | Demo salon config (see Step 4). |
| `apps/lexi-server/salons/_template.json` | Blank config with every field documented, copied per new salon. |
| `apps/lexi-server/test/*.test.js` | Unit tests for flow, slots, dedupe, signature check, intent fallback (Node's built-in test runner). |
| `apps/lexi-server/test/simulate.js` | Fake-WhatsApp simulator: posts signed webhooks to the server with mock WhatsApp, calendar and Claude, and prints timing. |
| `apps/lexi-server/railway.json` | Start command, health check path, restart policy. |
| `docs/lexi-server.md` | Written by `/document` after it works (architecture, per-salon set-up, runbook). |

### Files to Modify

| File Path | Changes |
|-----------|---------|
| `CLAUDE.md` | Add `apps/lexi-server/` to the map description of `apps/` and note Lexi 2.0 exists. |
| `context/lexi.md` | Add a "Lexi 2.0 direct server" section: status, where it runs, what it does and doesn't cover yet. |
| `context/tech-stack.md` | Add rows for Railway and the Google service account, and note the demo number points at the new server. |
| `reference/getting-keys.md` | Add blocks for Railway, Meta webhook for an existing number, and Google service account, with a verified date and a Changelog line. |
| `docs/_index.md` | Add `docs/lexi-server.md` (done by `/document`). |
| `ledger/theo.md` | Rows as each step completes. |

### Files to Delete (if any)

None.

---

## Design Decisions

### Key Decisions Made

1. **Own server on Meta Cloud API, hosted on Railway.** Decided by Theo. Full control, no Kapso fee or dependency, about R90/month shared across all salons.
2. **Demo number first.** Chales stays on Make until Phase 1 is proven.
3. **One config file per salon.** Services, hours, calendar ID, sheet ID, phone number ID, rules, address, photo link, staff alert number. Adding a salon is filling one file.
4. **SQLite file on a Railway volume for memory.** Survives restarts, no database service to pay for. Holds dedupe IDs, conversation state, bookings and a message log.
5. **Google service account for calendar and sheet.** The salon owner shares the calendar and sheet with it once. No personal login stored.
6. **Taps first, Claude only for typed text.** Menus and slots are built by code, so most replies need no Claude call. One structured Claude call handles free text, with a fallback to the menu if it fails or is unsure.
7. **Respond 200 to Meta immediately, process after.** Meta retries slow webhooks, which would cause duplicate deliveries.
8. **WhatsApp lists are capped at 10 rows.** Chales' Saturdays have 18 half-hour slots. Plan: ask morning or afternoon first when a day has more than 10 open slots, then show that half of the day. The Make flow's current handling must be read first (see Open Questions) so the client experience matches.
9. **Injectable clients.** WhatsApp, Google and Claude are passed into the flow, so tests and the simulator run with fakes and the real run changes nothing in the logic.
10. **Voice notes get a holding reply in Phase 1:** "Please type or tap, I can't listen to voice notes just yet." Real voice support is Phase 3.
11. **Names must be typed**, as in the Make flow (voice-to-text misheard "Theo" as "Siyou").
12. **Spending caps before going live:** a Railway usage limit and a monthly limit on the Claude API key.

### Alternatives Considered

- **Kapso:** rejected (per-number fees past 3, dependency).
- **n8n:** same step-chain style as Make, which is what made Lexi slow. Kept as a later option for non-technical editing.
- **Netlify functions:** cold starts and time limits make a dependable under-20-seconds harder.
- **Fly.io or Render:** similar cost, more setup or sleeping free tier.
- **Google Sheet or in-memory for conversation state:** slower or loses the client's place on restart.
- **Theo's personal Google login for calendar access:** breaks when the login changes and ties every client to one account.

### Open Questions (if any)

1. **Is the demo number currently attached to a live Make scenario** that Theo uses to demo to prospects? A number has one webhook target. Pointing it at Railway switches the demo over. Before the switch Claude records the current Make webhook URL so it can be pointed back in one step.
2. **How does Chales' Make flow handle more than 10 time slots?** Read it before building `slots.js` so the demo matches what clients see today.
3. **Demo calendar and sheet:** Theo creates a separate Google Calendar and a copy of the booking sheet for the demo, so no real client data is touched.
4. **Which Railway region?** Claude will choose a European region for the first test and measure the real round trip from South Africa.
5. **Nita's Luna / cleaning bot:** not described in this workspace or in session memory (searched `context/`, `ideas.md`, `team.md`, `strategy.md`, ledger and the session history). Theo needs to explain it before any plan covers it. Out of scope for Phase 1.

---

## Step-by-Step Tasks

Execute in order. Steps marked **Theo** need his account or action, Claude cannot do them.

### Step 1: Scaffold the app

Create the folder and project files.

**Actions:**

- Create `apps/lexi-server/` with `package.json` (Node 20, `"type": "module"`), `.gitignore`, `README.md` stub.
- Create `.env.example` listing only names: `PORT`, `META_VERIFY_TOKEN`, `META_APP_SECRET`, `SALONS_DIR`, `DATA_DIR`, `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, `GOOGLE_SERVICE_ACCOUNT_JSON` (base64), and per-salon WhatsApp tokens as `WA_TOKEN_<SLUG>`.
- Install dependencies, confirm `npm test` runs an empty suite.

**Files affected:**

- `apps/lexi-server/package.json`, `.env.example`, `.gitignore`, `README.md`

---

### Step 2: Core webhook server

**Actions:**

- `server.js`: GET `/webhook` returns the challenge when `hub.verify_token` matches. POST `/webhook` verifies `X-Hub-Signature-256` against the raw body using the app secret, returns 200 immediately, then processes each message asynchronously. GET `/health` returns ok.
- `salons.js`: load and validate every `salons/*.json` at startup (fail loudly on a missing field), look up by the `phone_number_id` in the webhook metadata. Unknown number: log and ignore.
- `store.js`: create tables `processed_messages(message_id PRIMARY KEY, received_at)`, `sessions(salon, phone, state, data, updated_at)`, `bookings(id, salon, phone, name, service, start, end, event_id, status)`, `message_log(id, salon, phone, direction, kind, started_at, finished_at, ms)`.
- Dedupe: insert the message ID first; if it already exists, stop.
- Tests: bad signature rejected, handshake works, duplicate message processed once, unknown number ignored.

**Files affected:**

- `src/server.js`, `src/salons.js`, `src/store.js`, `test/`

---

### Step 3: WhatsApp sending and parsing

**Actions:**

- `whatsapp.js`: functions for text, reply buttons (max 3), list message (max 10 rows total), and image with caption plus a call-to-action URL button ("Get Directions"). Parse inbound types: text, interactive button reply, interactive list reply, audio, image/other.
- Image failure must not fail the booking: wrap and fall back to plain text.
- Log send time per message into `message_log`.
- Tests: payload shapes match Meta's Cloud API format (checked against Meta's current docs at build time, fetched with Firecrawl).

**Files affected:**

- `src/whatsapp.js`, `test/whatsapp.test.js`

---

### Step 4: Salon config and the demo salon

**Actions:**

- Write `salons/_template.json` with every field commented in the README: `slug`, `name`, `phone_number_id`, `staff_alert_number`, `address`, `maps_url`, `photo_url`, `timezone`, `services[{id,name,minutes}]`, `hours` (per weekday: open, close, step minutes), `rules_text`, `welcome_text`, `calendar_id`, `sheet_id`, `cancel_cutoff_hours`.
- Write `salons/uncle-t-demo.json` for +27 76 492 4196 using the Chales service list and hours (from `context/lexi.md`) but demo calendar and sheet IDs. The phone number ID is read from Theo's Meta dashboard (**Theo** provides it).
- Salon rules text and welcome copy follow `reference/writing-style.md`.

**Files affected:**

- `salons/_template.json`, `salons/uncle-t-demo.json`

---

### Step 5: The conversation flow engine

**Actions:**

- `flow.js` as pure functions: `handle(session, inbound, salon, deps) -> { session, outbound[] }`.
- States: `new`, `service`, `day`, `daypart` (only when more than 10 slots), `time`, `name`, `confirm`, `done`, plus `cancel_pick`, `cancel_confirm`, `resched_day`, `resched_time`.
- New client: welcome and rules, then service list. If the first message (typed) names exactly one service, say "Lovely, a <service>!" and jump to the day list.
- Day list: next open days from the calendar, tapped. Time list: real open slots for that day, tapped.
- Name: typed only. A voice note or tap at this step gets "Please type your full name so I get the spelling right."
- Confirm: write calendar event, sheet row and `bookings` row, then send the photo confirmation (Step 7).
- Keywords: `CANCEL` and `RESCHEDULE` start those branches from any state. The server finds the client's upcoming booking by phone number, asks for confirmation before removing anything, and for a reschedule reuses the day and time steps.
- Anything unrecognised: one `intent.js` call (Step 6). If that fails or is unsure, resend the current menu. Never go silent.
- Voice notes (audio inbound): holding reply (Design Decision 10).
- Tests: every path in the Validation Checklist, with fake clients.

**Files affected:**

- `src/flow.js`, `src/slots.js`, `test/flow.test.js`, `test/slots.test.js`

---

### Step 6: Claude intent step

**Actions:**

- `intent.js`: one Anthropic call with a short system prompt (salon name, service list, today's date) asking for strict JSON `{intent: book|cancel|reschedule|question|unknown, service, day, time}`. Validate against the salon's real service list and open days; discard anything that doesn't match.
- Timeout of 6 seconds; on timeout, error, or invalid JSON, return `unknown` so the flow resends the menu.
- Model name from `ANTHROPIC_MODEL` (default chosen at build time from the current model list), never hard-coded in logic.
- Tests with a fake client: valid JSON, invalid JSON, timeout, hallucinated service name.

**Files affected:**

- `src/intent.js`, `test/intent.test.js`

---

### Step 7: Calendar, sheet and photo confirmation

**Actions:**

- `calendar.js`: service-account auth; free/busy for a day; create event (title "<service> - <name>", description with phone number, address); find by phone via the `bookings` table then verify the event still exists; delete; move.
- `sheet.js`: append a booking row, update status on cancel or reschedule. Column headers copied from the Chales sheet layout in `plans/client-template.md` (BookingSession, ProcessedMessages and Memberships tabs are not used in Phase 1).
- Confirmation message: salon photo with caption (service, day and time in bold, address) and a "Get Directions" button. Photo failure falls back to plain text, and the calendar and sheet writes still happen.
- Calendar or sheet failure after the client confirmed: tell the client plainly, alert the staff number on the salon config, and keep the booking row marked `needs_attention`.

**Files affected:**

- `src/calendar.js`, `src/sheet.js`, `src/whatsapp.js`

---

### Step 8: Test kit and local proof

**Actions:**

- `simulate.js`: boots the server in-process with fake WhatsApp, calendar and Claude, then replays scripted conversations as signed webhooks: new booking, service shortcut, typed free text, voice note, cancel, reschedule, duplicate delivery, photo failure, calendar failure, Saturday with more than 10 slots.
- Print per-message processing time and a pass/fail line per scenario.
- Run the full suite with `npm test` and the simulator, both clean, before any deploy.

**Files affected:**

- `test/simulate.js`, `test/*.test.js`

---

### Step 9: Accounts and keys (Theo)

Claude walks Theo through each block one at a time, following `reference/getting-keys.md` (sign-up link first, wait, then key page; keys go straight into Railway variables, never into chat or git).

**Actions (Theo):**

- Railway: sign up (free trial), create a project, add a volume for `DATA_DIR`, set a usage limit.
- Claude API: create a key for this server with a monthly spend limit.
- Google: create a service account, download its JSON key, create the demo calendar and demo sheet, share both with the service account's email.
- Meta: from the existing app, note the demo number's phone number ID, the app secret, and a permanent access token for the demo WABA. Record the current webhook URL for the demo number before changing it (Open Question 1).

**Actions (Claude):**

- Update `reference/getting-keys.md` with the Railway, service account and webhook blocks and a `verified` date.
- Test each key without echoing it.

**Files affected:**

- `reference/getting-keys.md`

---

### Step 10: Deploy and connect

**Actions:**

- Add `railway.json`, connect the repo, set the root to `apps/lexi-server`, set environment variables in Railway.
- Confirm `/health` answers from the Railway URL.
- **Theo:** in Meta, set the webhook callback URL to `https://<railway-url>/webhook` with the verify token, and subscribe to messages. Meta does the handshake.
- Send a "hello" from Theo's phone to the demo number and confirm a reply.

**Files affected:**

- `apps/lexi-server/railway.json`

---

### Step 11: Prove it on the demo number

This is the "works 2000%" step. The bar is many timed real runs, not one.

**Actions:**

- Run each path at least 10 times from a real phone: new booking by taps, service shortcut, typed free text, cancel, reschedule, duplicate (resend quickly), a Saturday with many slots, voice note, name with unusual spelling.
- Read the `message_log` and record median and worst times for taps and for free text.
- Check calendar and sheet rows match every booking; nothing doubled, nothing missing.
- Compare against Make's 2.5 minutes in the report.
- Fix anything found, re-run the failing paths.

**Files affected:**

- `apps/lexi-server/` (fixes), `outputs/2026-10-xx-lexi-server-proof-report.md` (results)

---

### Step 12: Documentation and context updates

**Actions:**

- Run `/document` for `docs/lexi-server.md` (architecture, how to add a salon, how to point a number back to Make, where logs are, how to read the message log).
- Update `CLAUDE.md`, `context/lexi.md`, `context/tech-stack.md`, `docs/_index.md`.
- Write ledger rows for each completed step as it happens, then run `/log`.

**Files affected:**

- `docs/lexi-server.md`, `docs/_index.md`, `CLAUDE.md`, `context/lexi.md`, `context/tech-stack.md`, `ledger/theo.md`

---

## Connections & Dependencies

### Files That Reference This Area

- `context/lexi.md` (rebuild target and the under-20-seconds rule)
- `plans/client-template.md` (Make-based per-client onboarding; becomes the fallback path)
- `plans/2026-10-14-personal-assistant-agent.md` (same webhook pattern, separate system)
- `context/tech-stack.md`, `CLAUDE.md` (map and stack)

### Updates Needed for Consistency

- `context/lexi.md`, `context/tech-stack.md`, `CLAUDE.md` and `reference/getting-keys.md` as listed in Step 12 and Step 9.

### Impact on Existing Workflows

- Chales' live Lexi, reminders and membership tracker are not touched in Phase 1.
- The demo number's webhook moves from whatever it points at today to Railway. This changes how Theo's prospect demos behave, so it is done deliberately and can be reversed in one step.
- Phase 2 (moving Chales) is a separate plan written after this one passes.

---

## Validation Checklist

- [ ] `npm test` passes with no failures.
- [ ] Simulator runs every scenario and all pass.
- [ ] Bad signature is rejected; handshake works; duplicate message handled once.
- [ ] `/health` answers on the Railway URL.
- [ ] Meta webhook handshake succeeds for the demo number.
- [ ] A real booking by taps reaches the demo calendar and the demo sheet with the right details.
- [ ] The service shortcut skips the service menu when exactly one service is named.
- [ ] Cancel asks for confirmation, then removes the event and updates the sheet.
- [ ] Reschedule moves the event and updates the sheet.
- [ ] Saturday with more than 10 open slots shows morning/afternoon first, then the times.
- [ ] A voice note gets the holding reply, never silence.
- [ ] A failed photo still produces a plain-text confirmation.
- [ ] A forced calendar failure alerts the staff number and tells the client plainly.
- [ ] Railway usage limit and Claude monthly limit are both set.
- [ ] No key appears in git (`git grep` for token and secret patterns is clean).
- [ ] Chales' live Make scenarios are unchanged.

---

## Success Criteria

The implementation is complete when:

1. At least 10 real timed runs of each path on the demo number are logged, with taps typically 2 to 4 seconds and every run, including typed free text, under 20 seconds.
2. Every booking, cancel and reschedule matches in the demo calendar, the demo sheet and the `bookings` table, with zero doubles or misses across the run.
3. The proof report is written with median and worst times next to Make's 2.5 minutes, and Theo has seen it.
4. Adding another salon takes only a new config file and a Meta phone number ID, shown by a dry run with a second dummy config.
5. Docs and context files are updated and the work is logged.

---

## Notes

- **Phase 2 (Chales)** gets its own plan after Phase 1 passes: side-by-side run, comparison, then cut-over with the Make webhook URL kept for a one-step rollback.
- **Phase 3:** voice notes into bookings, membership tracker, reminders, owner screen, second client.
- **Nita's cleaning business** keeps its own invoicing and next-in-queue plans in `context/rags-to-riches.md`. A booking bot for it would reuse this server's core but needs its own flow (addresses, longer visits, recurring jobs). Needs Theo's description of the "cleaning bot" before planning.
- **Cost estimate:** Railway Hobby $5/month (about R90) including $5 usage, checked 2026-10-20, usage-billed so the cap matters. Claude API cost per booking is small because taps need no Claude call, but it is not yet measured.
- **Time estimate:** core build and local proof is several focused sessions. Real-number proof depends on how fast Theo's accounts and keys are ready.
