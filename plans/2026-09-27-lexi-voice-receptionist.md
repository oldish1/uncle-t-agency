# Plan: Lexi Voice, an AI voice receptionist on the same WhatsApp number

**Created:** 2026-09-27
**Status:** Draft
**Request:** Build a voice AI receptionist for Chales Hair Boutique that answers calls and talks back and forth in real time, as a separate Make scenario from the main Lexi booking bot.
**Purpose:** Give clients who'd rather call than type a way to book with Lexi over voice, reusing the same calendar, booking sheet and cancel/reschedule logic already proven on WhatsApp, without adding more weight to the already-large main Lexi scenario.

---

## Overview

### What This Plan Accomplishes

A second, standalone Make scenario that connects an AI voice platform (Retell) to Chales Hair Boutique's WhatsApp number over the WhatsApp Business Calling API. A client taps the call button in their WhatsApp chat with Lexi, talks to a voice agent that greets them, offers open slots, takes their name and service, and books the same way a WhatsApp booking does, calendar event, tracking sheet row, the lot. Tested first on the demo number, never on Chanté's live number.

### Why This Matters

Theo's target is 5 paying clients by December, and a working voice demo is a strong differentiator, no local competitor pairs WhatsApp chat and phone-quality voice on one number for one price. It also catches the calls a salon misses while a stylist's hands are busy, which WhatsApp text alone can't. Keeping it a separate scenario means it doesn't add to the 146-module main Lexi scenario, which is already large enough that a full-blueprint edit is starting to hit real size limits.

---

## Current State

### Relevant Existing Structure

- `context/lexi.md`, what Lexi does today (booking, cancel/reschedule, membership tracker, reminders, voice notes over WhatsApp text).
- `context/ideas.md`, "Lexi Voice (queued behind Lexi 2.0)", the original idea, parked pending the first paying client.
- `reference/research/2026-09-25-lexi-voice.md`, the research: WhatsApp Business Calling API confirmed available and free for client-initiated calls, SIP set up already visible on Chales' number, per-call cost comparison across Bland/Vapi/Retell, and BizAI as the local competitor to beat (R999/month, ~200 minutes).
- Make scenario `Chales Hair Boutique` (id `5043763`), the live booking bot this voice build reuses logic from (calendar check module patterns like `google-calendar:searchEvents` and `google-calendar:createAnEvent`, the booking sheet write pattern, cancel/reschedule flow).
- Make scenario `Chales - Appointment Reminders` (id `7617803`), a small, separate scenario, proof that splitting Lexi's jobs into standalone scenarios already works cleanly.
- Chales' WhatsApp number, confirmed 25 Sept in WhatsApp Manager: "Allow voice calls" is OFF (must stay off until the AI is wired up), SIP set-up button is present, "Display call buttons" is on.

### Gaps or Problems Being Addressed

- No voice channel exists yet, only WhatsApp text and voice notes (which are transcribed and handled as text, not a live conversation).
- The main Lexi scenario is large enough that further edits to it are risky and slow to push; this build must not add modules there.
- No Retell (or other voice platform) account exists yet for this workspace.
- No demo-number test has been run to confirm accent handling, latency, or whether the pauses feel natural for a Cape Town caller.

---

## Integration Type

**Classification:** Script/Automation build (new Make scenario), not a Skill or Command in this workspace's own sense.
**Reasoning:** This is infrastructure in Make and Retell, not a Claude Code skill or slash command. It's tracked the way `context/lexi.md` and the two existing Lexi scenarios are tracked, as a documented build with its own plan and ledger trail.
**Location:** A new Make scenario (name suggested: `Chales - Lexi Voice (DEMO)`), a Retell account and agent, connected to the demo WhatsApp number. Documentation lives in `context/lexi.md` (a new "Lexi Voice" section) once live, matching how the membership tracker and reminders were documented.
**Auto-discovery:** N/A, this isn't a skill.

---

## Proposed Changes

### Summary of Changes

- Sign up for Retell, use the $10 free trial credit for the first tests.
- Turn on "Allow voice calls" on the **demo number only**, and set up SIP so Retell can receive calls through WhatsApp Calling.
- Build a Retell agent with a scripted conversation: greeting, offer 3 open slots, collect name and service, confirm, hand off to the booking write.
- Build a small, separate Make scenario that Retell's webhook calls into, reusing the existing calendar-check and booking-write patterns from scenario 5043763, writing to the **demo number's own calendar and sheet**, never Chanté's live ones, until this is proven.
- Test by calling it ourselves in Cape Town accents, using the real service names, timing every pause.
- Only after that passes, plan a second phase (not part of this build) to connect it to a real client's number.

### New Files to Create

| File Path | Purpose |
|-----------|---------|
| `reference/research/2026-09-27-lexi-voice-test-log.md` | Running log of test calls: what was said, what Lexi Voice understood, latency, anything that broke. Created once the first test call happens. |

### Files to Modify

| File Path | Changes |
|-----------|---------|
| `context/lexi.md` | Add a "Lexi Voice" section once the demo scenario is live and passing tests, matching the style of the existing Membership/Reminders/Client template sections. |
| `context/ideas.md` | Update the "Lexi Voice (queued behind Lexi 2.0)" entry to reflect that the trigger has changed from "first paying client" to "in progress, demo number" and link this plan. |
| `context/numbers.md` | Add a line once Retell has a real monthly cost figure from testing, so the team-safe snapshot stays current. |
| `ledger/theo.md` | Row per meaningful step, per the workspace's standing ledger rule, not batched at the end. |

### Files to Delete (if any)

None.

---

## Design Decisions

### Key Decisions Made

1. **Separate Make scenario, not added to scenario 5043763**: the main Lexi scenario is already 146 modules and hit a real size wall this session (a full-blueprint push became too large to send safely). Voice needs its own home so it can be edited without that risk, and so it can be torn down or rebuilt without touching the live booking bot.
2. **Retell over Vapi to start**: Retell has a $10 free credit (roughly 70-90 test minutes) and fewer moving parts to wire up than Vapi. Vapi is cheaper per-minute once at volume, worth revisiting after the first real cost numbers come in.
3. **WhatsApp Business Calling API, not a phone number**: it's free for calls the client makes, reuses the number and Meta app Lexi already has, and Chales' number already shows calling and SIP as available. A dedicated phone number (Route 2 from the research) stays parked for clients whose customers prefer dialling over WhatsApp.
4. **Demo number first, always**: same rule the workspace already follows for any untested Lexi change. Chanté's live number and calendar are never touched until a full test pass on the demo number succeeds.
5. **Reuse, don't rebuild, the booking logic**: the calendar-check and calendar-write modules already proven in scenario 5043763 get copied into the new voice scenario's flow, not reinvented from scratch.

### Alternatives Considered

- **Bland AI**: similar pricing to Retell, was the platform in the original inspiration reel, but the research found no meaningful edge over Retell for this use case, and Retell's free trial credit makes it cheaper to start testing with.
- **Adding voice directly into scenario 5043763**: rejected because of the size problem already hit this session, and because it would mean any future voice-only edit risks breaking the live booking flow.
- **A dedicated phone number from day one**: rejected for now, WhatsApp Calling is free and already available, a phone number adds monthly cost and setup time (SA number registration needs a real Cape Town address and ID documents) for no benefit until there's a client whose customers specifically want to dial a number.

### Open Questions

- Retell account: does Theo already have one, or does this session need to create it? (Needed before any build work starts.)
- Who calls the test line first, Theo, or does Claude need a way to trigger a test call too? Retell's dashboard usually supports both.
- Pricing for the voice add-on isn't decided yet (the research suggested R500-R900/month once real cost-per-call numbers exist), out of scope for this build, revisit once tests are done.

---

## Step-by-Step Tasks

### Step 1: Set up the Retell account

**Actions:**
- Sign up at Retell (or confirm an existing account) and claim the $10 free trial credit.
- Store the Retell API key the same way other keys are stored in this workspace, in `.env`, never committed.

**Files affected:**
- `.env` (not committed, key added locally per the existing pattern in `.env.example`)

---

### Step 2: Turn on calling for the demo number only

**Actions:**
- In WhatsApp Manager, open the **demo number** (not Chales' live number).
- Switch "Allow voice calls" ON.
- Open the SIP set-up flow and note the connection details Retell will need (SIP URI, credentials).
- Leave Chanté's live number's "Allow voice calls" switch exactly as it is (OFF) until this whole build is proven.

**Files affected:**
- None (this is a WhatsApp Manager configuration change, not a repo change).

---

### Step 3: Build the Retell agent's conversation script

**Actions:**
- Write the greeting, slot-offer, name/service capture, and confirmation script, following the same stages already proven in Lexi's WhatsApp AI prompt (module 3 of scenario 5043763): stage-based, one thing asked at a time, exact service names, no jargon.
- Include a global "AI disclosure" response (tells the truth if asked "am I talking to a bot?").
- Keep the script short enough to test quickly, refine after the first real test call rather than over-writing it blind.

**Files affected:**
- None yet (lives inside Retell's own agent configuration until scoped for export/documentation).

---

### Step 4: Build the connecting Make scenario

**Actions:**
- Create a new scenario, name it `Chales - Lexi Voice (DEMO)`.
- Add a webhook trigger that Retell calls (Retell supports function/tool calls mid-conversation and an end-of-call webhook).
- Reuse the calendar-check pattern from scenario 5043763 (module 129/138-style `google-calendar:searchEvents`) to check real availability during the call.
- Reuse the booking-write pattern (module 81-style `google-calendar:createAnEvent`, plus a sheet row) to write the confirmed booking, pointed at the **demo number's calendar and sheet**.
- Confirm the WhatsApp confirmation message still fires after a voice booking, the same photo-confirmation pattern Lexi already uses for WhatsApp bookings, so the client gets the same experience either way.

**Files affected:**
- None in the repo (Make scenario built directly in Make, documented afterward).

---

### Step 5: Test end to end

**Actions:**
- Call the demo number from a real phone, speaking in a Cape Town accent, using real service names (Nanoplastia, Botox & Glowtox, Brazilian & Keratin, Wash and Blowdry).
- Time every pause between the caller finishing a sentence and Lexi Voice replying.
- Confirm the booking actually lands correctly in the demo calendar and sheet, with the right day, time, service and name.
- Try a cancel/reschedule request mid-call if the script supports it yet; if not, note it as a gap for a later pass, don't block the first test on it.
- Log every test call's outcome in `reference/research/2026-09-27-lexi-voice-test-log.md`.

**Files affected:**
- `reference/research/2026-09-27-lexi-voice-test-log.md` (created)

---

### Step 6: Document and log

**Actions:**
- Once a full test pass succeeds, add the "Lexi Voice" section to `context/lexi.md`.
- Update `context/ideas.md`'s Lexi Voice entry to reflect real status.
- Add a real monthly cost estimate to `context/numbers.md` once there's actual per-call spend to point to.
- Write ledger rows as each step above completes, not batched at the end.

**Files affected:**
- `context/lexi.md`, `context/ideas.md`, `context/numbers.md`, `ledger/theo.md`

---

## Connections & Dependencies

### Files That Reference This Area

- `context/ideas.md` already has a "Lexi Voice" entry pointing at this work.
- `context/business.md` mentions BizAI's "Voice Valet" as a competitor, this build is the direct answer to that.
- `context/strategy.md` doesn't yet mention voice as a priority; if this becomes urgent for the December target, it should get a line there too.

### Updates Needed for Consistency

- `docs/_index.md` currently has nothing logged, once this is built and documented, it may be worth a `/document` pass so future sessions find it without re-reading all of `context/lexi.md`.

### Impact on Existing Workflows

- None on the live booking scenario (5043763) or reminders (7617803), this is additive and isolated by design.
- Adds a new account (Retell) and a new cost line to track once past the free trial.

---

## Validation Checklist

- [ ] Retell account created, API key stored in `.env`
- [ ] Demo number's "Allow voice calls" is ON, Chanté's live number's is untouched (still OFF)
- [ ] Retell agent script written and testable
- [ ] New Make scenario built, connected to Retell, pointed at the demo calendar/sheet only
- [ ] At least 3 real test calls made, in Cape Town accents, using real service names
- [ ] A booking made by voice appears correctly in the demo calendar and sheet
- [ ] Latency/pauses are timed and judged acceptable (or flagged as a blocker if not)
- [ ] `context/lexi.md`, `context/ideas.md` updated to reflect real status
- [ ] Chanté's live number and data were never touched during testing

---

## Success Criteria

The implementation is complete when:

1. A real phone call to the demo number results in a correctly booked appointment in the demo calendar and sheet, entirely by voice, no typing.
2. The conversation holds up in a Cape Town accent with real salon service names, without the caller needing to repeat themselves more than once or twice.
3. Chanté's live number, calendar and sheet remain completely untouched by any part of this testing.
4. The build and its cost-per-call are documented well enough that a pricing decision (the R500-R900/month range from the research) can be made with real numbers, not estimates.

---

## Notes

- This plan assumes Theo starts a fresh session to run `/implement plans/2026-09-27-lexi-voice-receptionist.md`, keeping voice work off the `lexi-membership-tooling` branch this session is on.
- The bigger priority right now is landing paying clients by December. This build is worth doing because a working voice demo can help close a deal, not instead of outreach, alongside it. If time is tight, Steps 1-3 (account, calling switch, script) can happen in small pieces between other work rather than needing one long session.
- Once a second paying client is close, revisit whether Lexi Voice needs its own reusable client template too, the same way `plans/client-template.md` covers the WhatsApp side.
