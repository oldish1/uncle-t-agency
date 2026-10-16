# Plan: Personal assistant agent on its own WhatsApp number

**Created:** 2026-10-14
**Status:** Draft, partly superseded by Rex (see note below)
**Request:** A personal assistant agent Theo can WhatsApp from anywhere, on a dedicated Vodacom number, fully separate from Lexi.
**Purpose:** Let Theo run research, price checks, status checks and build requests from his phone between day-job shifts and client visits, without opening a laptop.

> **Update 2026-10-14:** Rex already exists from earlier sessions. Branch `claude/rex-commander-agent-d2ak3z` holds `apps/rex/` (system prompt, Make blueprint) and a Make scenario "Rex - Commander Agent" (7638753, OFF). The handoff is `outputs/handoffs/2026-10-01-rex-meta-setup.md`. Decisions made there override this plan where they differ: Rex is the only agent with a WhatsApp number, he runs on **Make** (not a new Node service), the other agents are separate Make scenarios he calls, and the Meta app is one general "Uncle T Agents" app under the existing Business Portfolio. This plan's safety rules (whitelist to Theo, read/draft/act tiers, YES codes, spend caps) still apply to Rex. The SIM Theo bought replaces Meta's free test number. The Node build in Steps 3 to 8 is only a fallback if Make proves too limited.

---

## Overview

### What This Plan Accomplishes

A private WhatsApp number that only answers Theo. He sends a text (voice notes in phase 2), the agent does the work using Claude plus a set of tools (web scraping, Gmail, Calendar, Sheets, the ledger and context files), and replies on WhatsApp. Lookups run automatically. Anything that sends, spends or changes a client site waits for Theo's "yes". Long jobs get an instant "on it" and a message when finished.

### Why This Matters

Theo's day job eats the hours he'd spend selling and building. A phone-first assistant turns dead time (driving to clients, breaks) into progress, and answers "how far are you with the build?" without a laptop. It also doubles as a showcase: a working personal agent is a stronger pitch for the agency than any demo deck.

---

## Current State

### Relevant Existing Structure

- `context/tech-stack.md`: WhatsApp Business / Cloud API already used for Lexi. Two numbers exist: Chales' live number (0714296057) and the demo number "Uncle T Demo" (+27 76 492 4196). Neither may be reused here.
- Make.com holds Lexi's scenarios (5043763 booking bot, 7617803 reminders). Lexi's Meta app, WhatsApp Business Account and OpenAI connection ("OpenAI Lexi") belong to Lexi.
- `plans/lexi-voice-notes.md`: the voice-note transcription pattern (download Meta audio, send to a transcription model) is proven and can be copied in shape, but not shared in accounts.
- Tools already available to this workspace: Firecrawl, Apify, Supadata, Gmail, Google Calendar, Drive, Sheets connectors.
- `scripts/` and `apps/` (empty): `apps/` is where something that outgrew a chat lives.
- `ledger/theo.md`: the work diary the agent will read to report status.
- `reference/research/2026-09-25-lexi-voice.md`: earlier research into WhatsApp Calling.

### Gaps or Problems Being Addressed

- No way to reach Claude from a phone except this app.
- No always-on process: cloud sessions are temporary, so something must stay running to receive WhatsApp messages.
- No approval pattern for actions with side effects.
- No separation yet between Lexi (client-facing, billable) and Theo's personal tooling.

---

## Integration Type

**Classification:** Script / small app (new), with a Skill added afterwards for talking to it.
**Reasoning:** This is a running service, not a slash command. It outgrew a chat from day one, which is what `apps/` is for.
**Location:** `apps/assistant/` (code), `docs/personal-assistant.md` (documentation via `/document`), `context/tech-stack.md` (new row).
**Auto-discovery:** N/A for the service. Documentation indexed in `docs/_index.md`.

---

## Proposed Changes

### Summary of Changes

- Buy a new Vodacom prepaid SIM and register it as a WhatsApp Business number on a **new** WhatsApp Business Account, not Lexi's.
- Create a **new** Meta app for it, so a Lexi problem can never take it down and vice versa.
- Build a small Node.js service in `apps/assistant/` that receives WhatsApp messages by webhook, checks the sender is Theo, runs a Claude tool-use loop, and replies.
- Deploy it to a small always-on host (own account, own keys).
- Tools in three tiers: read (auto), draft (auto, nothing sent), act (needs approval).
- Status tool that reads `ledger/theo.md` and any running job state.
- Phase 2: voice notes in via transcription. Phase 3 (optional): voice replies.

### New Files to Create

| File Path | Purpose |
|-----------|---------|
| `apps/assistant/package.json` | Node project, dependencies, start script |
| `apps/assistant/src/server.js` | Webhook endpoint: Meta verification handshake, message intake, signature check |
| `apps/assistant/src/whitelist.js` | Allow only Theo's number; silently ignore everyone else |
| `apps/assistant/src/agent.js` | Claude tool-use loop, system prompt, tier rules |
| `apps/assistant/src/tools/` | One file per tool: `web.js` (Firecrawl search/scrape), `status.js`, `gmail.js`, `calendar.js`, `sheets.js` |
| `apps/assistant/src/approvals.js` | Pending-action store; "YES 4821" / "NO 4821" handling; 30 minute expiry |
| `apps/assistant/src/jobs.js` | Long-job runner: instant "on it", then result message |
| `apps/assistant/src/whatsapp.js` | Send text, mark read, (phase 2) fetch media |
| `apps/assistant/.env.example` | Names of keys only, no values |
| `apps/assistant/README.md` | Plain-English: what it is, how to restart it, where keys live |
| `docs/personal-assistant.md` | Documentation filed via `/document` |

### Files to Modify

| File Path | Changes |
|-----------|---------|
| `context/tech-stack.md` | New row: "Personal assistant WhatsApp number" with number, host, and "separate from Lexi" |
| `CLAUDE.md` | Add `apps/assistant/` to the map once it exists |
| `docs/_index.md` | Index the new doc |
| `reference/getting-keys.md` | Add Meta app, hosting and transcription key steps |
| `ledger/theo.md` | Rows written as each step completes |

### Files to Delete (if any)

None.

---

## Design Decisions

### Key Decisions Made

1. **Fully separate from Lexi.** New SIM, new WhatsApp Business Account, new Meta app, new host, new API keys, new Claude API key. If Lexi breaks during a client onboarding, this keeps working, and the reverse. Nothing here touches Make scenarios 5043763 or 7617803.
2. **Node service, not a Make scenario.** Make is great for fixed flows but clumsy for an agent that decides which tool to call. A small Node app keeps the tool loop in one readable place. Trade-off: Theo can't click through it in Make. Mitigated by the README and a one-word restart instruction.
3. **Official WhatsApp Cloud API, not an unofficial linked-device library.** Unofficial libraries risk the number being banned and break without warning. The official route needs a bit more setup but is stable.
4. **Whitelist first.** The very first check on every incoming message is the sender's number. Anything else gets no reply and no processing, so strangers can't spend Claude credits or reach tools.
5. **Three tiers.** Read (search, scrape, read ledger, read calendar/email): automatic. Draft (write an email or caption): automatic, but only shown to Theo. Act (send email, create calendar event, edit a client site, spend money, post anything): shown as "I'm about to do X. Reply YES 4821 to confirm", expires in 30 minutes. A voice-note mishearing therefore can't cause damage.
6. **Long jobs are asynchronous.** Reply "On it, back shortly" within seconds, run the job, message the result. Meta's 24 hour window means Theo's message opens a free reply window; the agent should finish inside it or ask Theo to say hi again.
7. **Text first.** Voice notes in are phase 2, and voice replies phase 3, because the text version already delivers most of the value.
8. **Money.** Claude usage per message plus WhatsApp fees. Replies within 24 hours of Theo's message are expected to be free or near-free, but current Meta pricing must be checked before launch (open question 3).

### Alternatives Considered

- **Make.com scenario with Claude HTTP module:** simplest for Theo to see, but weak for multi-tool reasoning and long jobs. Rejected for the core, still useful later for scheduled pings.
- **Twilio WhatsApp sender:** easier signup, but adds a per-message fee layered on Meta's and a second vendor. Kept as a fallback if Meta onboarding stalls.
- **Phone call agent (Vapi/Retell):** costs about R2 to R3 a minute and drops on bad signal. Deferred. See earlier discussion; WhatsApp voice notes cover the driving case.
- **Unofficial WhatsApp Web libraries:** cheapest, but ban risk. Rejected.
- **Reusing the demo number:** it is attached to Lexi and used for prospect demos. Rejected.

### Open Questions

1. **Hosting.** Railway, Fly.io or a small VPS? Recommend Railway or Fly: a few dollars a month, simple restart. Needs Theo's card and an account, which Claude cannot create.
2. **Who owns the Meta Business account?** Create the new WhatsApp Business Account under the existing Meta Business Manager (simplest) or a fresh one (cleaner separation)? Recommend same Business Manager, new WABA and new app.
3. **Meta pricing check.** Confirm what Meta charges for service replies versus business-initiated messages right now, in Rand, before launch.
4. **Voice-note transcription provider** (phase 2): Groq, OpenAI or Deepgram. Needs a key separate from Lexi's "OpenAI Lexi" connection.
5. **Which accounts may it act on?** Start with Theo's Gmail and Calendar read-only, or include draft creation from day one? Recommend read plus drafts, no sending.
6. **The "taste skill" mentioned earlier is not installed here.** Not needed for this build. Ask Theo where it lives before the next client site.

---

## Step-by-Step Tasks

Execute in order. Steps marked **Theo** need him; everything else Claude does.

### Step 1: Number and Meta setup (Theo, with Claude guiding)

**Actions:**

- **Theo:** buy a Vodacom prepaid SIM. Keep it in a phone that can receive an SMS or call for the one-time verification code. The number must not already be on regular WhatsApp.
- **Theo:** in Meta Business Manager, create a new WhatsApp Business Account and a new Meta developer app for the assistant. Add the SIM number and verify it.
- **Theo:** generate a permanent access token for the app and note the Phone Number ID.
- Claude gives click-by-click steps in plain English and checks the result with a test message.

**Files affected:**

- `reference/getting-keys.md`

---

### Step 2: Accounts and keys (Theo)

**Actions:**

- **Theo:** create a new Claude API key dedicated to the assistant (not shared with Lexi).
- **Theo:** create the hosting account (Railway or Fly) and add the keys as environment variables there. Keys never go into chat or git.
- Add Firecrawl key (already in workspace `.env`) to the host environment.

**Files affected:**

- `apps/assistant/.env.example`

---

### Step 3: Skeleton service and whitelist

**Actions:**

- Create the Node project with a `/webhook` GET (Meta handshake) and POST (messages).
- Verify Meta's request signature on every POST.
- Whitelist check as the first line of message handling. Store Theo's number as an environment variable, never in code.
- Echo reply "Assistant online" to confirm the round trip.

**Files affected:**

- `apps/assistant/package.json`, `src/server.js`, `src/whitelist.js`, `src/whatsapp.js`

---

### Step 4: Agent loop with read tools

**Actions:**

- Build the Claude tool-use loop with a short system prompt: Theo's context, plain-English replies, Rand, South African context, keep WhatsApp messages short, no jargon.
- Add read tools: web search and scrape (Firecrawl), read ledger, read calendar.
- Add a `status` tool that reads the latest rows of `ledger/theo.md` and any running job.
- Keep conversation memory short (last 20 messages) so costs stay low.

**Files affected:**

- `apps/assistant/src/agent.js`, `src/tools/web.js`, `src/tools/status.js`, `src/tools/calendar.js`

---

### Step 5: Approvals and long jobs

**Actions:**

- Implement the pending-action store with a 4-digit code and 30 minute expiry.
- Wrap every act-tier tool so it never runs directly: it creates a pending action and messages Theo the plan.
- Add the job runner: instant "On it" reply, background run, result message. If a job outlives the 24 hour window, tell Theo to say hi to reopen it.
- Add draft-only Gmail (create draft, never send).

**Files affected:**

- `apps/assistant/src/approvals.js`, `src/jobs.js`, `src/tools/gmail.js`

---

### Step 6: Deploy and test with `/test`

**Actions:**

- Deploy to the host, point Meta's webhook at it, confirm the handshake.
- Run through real scenarios from Theo's phone: price check on a product, "what did we do yesterday", "draft an email to X", "send it" (must demand a YES), a message from a different number (must be ignored).
- Time the replies. Target: simple answers under 20 seconds, matching the workspace's responsiveness standard.
- Pull the SIM's WhatsApp number from the whitelist test to prove the ignore rule works.

**Files affected:**

- `apps/assistant/` (fixes only)

---

### Step 7: Documentation and housekeeping

**Actions:**

- Run `/document` to write `docs/personal-assistant.md` and update `docs/_index.md`.
- Add the number and host to `context/tech-stack.md` and `apps/assistant/` to the map in `CLAUDE.md`.
- Write a restart and key-rotation note in plain English in `apps/assistant/README.md`.
- Ledger rows for each step, as completed.

**Files affected:**

- `docs/personal-assistant.md`, `docs/_index.md`, `context/tech-stack.md`, `CLAUDE.md`, `apps/assistant/README.md`

---

### Step 8 (phase 2): Voice notes in

**Actions:**

- On an incoming `audio` message, fetch the file via the Graph API, transcribe it, and feed the text into the same agent loop.
- Echo the transcript back first ("I heard: ...") so mishearings are caught before anything runs.
- Test with Cape Town English, Afrikaans, and mixed speech, and with road noise.

**Files affected:**

- `apps/assistant/src/whatsapp.js`, `src/transcribe.js`

---

## Connections & Dependencies

### Files That Reference This Area

- `context/tech-stack.md` (WhatsApp rows)
- `context/lexi.md` (must keep stating Lexi's numbers are separate)
- `reference/getting-keys.md`

### Updates Needed for Consistency

- Tech-stack table, `CLAUDE.md` map, `docs/_index.md`.
- Ledger rows written as work happens.

### Impact on Existing Workflows

None for Lexi: no shared number, app, scenario, key or host. The only shared thing is Theo's attention, which is why the plan keeps the build small and ships the text version first.

---

## Validation Checklist

- [ ] A message from Theo's number gets a sensible reply in under 20 seconds for a simple question.
- [ ] A message from any other number gets no reply and no tool calls.
- [ ] A price-check request returns a sourced answer.
- [ ] Asking it to send an email produces a draft and a YES prompt, and sends nothing until Theo replies YES with the right code.
- [ ] A wrong or expired code does nothing.
- [ ] A long job replies "On it" first and delivers the result afterwards.
- [ ] "How far are you with the build?" returns the latest ledger rows.
- [ ] Stopping or breaking the assistant does not affect Lexi, and vice versa.
- [ ] No keys appear in git or chat.

---

## Success Criteria

The implementation is complete when:

1. Theo can WhatsApp the dedicated number from his phone and get a useful answer to a price or research question within 20 seconds.
2. Only Theo's number is answered, proven by a test from a second number.
3. No action with side effects happens without Theo's explicit YES.
4. The assistant runs on its own number, Meta app, host and keys, with nothing shared with Lexi.
5. Theo can restart it from the README without help.

---

## Notes

- Driving: voice notes must be recorded hands-free (CarPlay, Android Auto, Bluetooth) or from a parked car.
- Prompt-injection risk: pages the agent scrapes may contain instructions aimed at it. The approval tier is the safety net, so act-tier tools must never be callable straight from scraped content.
- Spend cap: set a monthly limit on the Claude API key and the host so a loop can't run up a bill.
- Future ideas, after launch: a morning briefing pushed at a set time, forwarding a prospect's WhatsApp to it for a quick reply draft, and a "new client site" command that kicks off the build flow from a message.
- Priority reminder: Lexi's under-20-seconds response target and first paying client still come first. This plan is sized to be built in short evening sessions.
