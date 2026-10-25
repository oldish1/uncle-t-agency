# Plan: WhatsApp guest assistant for Airbnb and Booking.com hosts

**Created:** 2026-10-20
**Status:** Draft
**Request:** A WhatsApp guest assistant for Nita's host clients ("Luna for guests"): pick a pilot host, write the questions, plan the build.
**Purpose:** Stop hosts drowning in small guest messages (fan, broom, blanket, towel, wifi, check-in), turn extras into paid jobs for Rags to Riches, and later win repeat guests as direct bookings that skip the 15% commission.

---

## Overview

### What This Plan Accomplishes

One WhatsApp assistant per host, on that host's own number, answering guests 24/7 from a sheet of facts about the apartment. When a guest asks for an extra, it takes the request, tells the guest what happens next, and sends the host (and optionally Nita's team) one list. Guests reach it through a QR code inside the apartment and a link in Booking.com's scheduled check-in message.

### Why This Matters

Booking.com's message API is closed to anyone but certified partners (`reference/research/2026-10-20-booking-com-guest-messaging.md`), and the overseas tools need a PMS and bill in dollars or euros. A WhatsApp assistant sidesteps both. It also feeds Nita's business: every towel set, blanket or mid-stay clean a guest asks for is a job, and it gives the agency a second product with recurring fees beyond salons.

---

## Current State

### Relevant Existing Structure

- **Luna** (Rags to Riches booking bot), Make scenario 7645932, live on +27 77 382 8532. Source in `apps/rags-to-riches-bot/` **on branch `claude/charming-tesla-j7vsii`, not yet on main**. It is the pattern to copy: own Meta app, own number, own Make folder, own Google Sheet, own Claude key, blueprint built by `build_blueprint.py`, Make Code steps tested with `node`.
- Luna's `ClientDatabase` sheet already lists the likely hosts: Fancy (Bree 2910, 9 dates booked Oct to Nov, the busiest), Kobie (Bree, books a month ahead, 7 to 11 Nov), Megan (took over Nick Burn's two Airbnb units 210 and 409).
- `plans/client-template.md` and Lexi's template approach: sanitised blueprint with placeholders, reused per client.
- `context/rags-to-riches.md`: Nita's family price R699/month, list price R999/month.
- `reference/research/2026-10-20-booking-com-guest-messaging.md`: now copied onto this branch.

### Gaps or Problems Being Addressed

- No product exists for guests, only for cleaning clients booking Nita.
- We don't know which hosts use Booking.com versus Airbnb, how many messages they get, or what extras they can supply. The questions file answers that.
- No price for the host product yet.

---

## Pilot host: recommendation

**Fancy.** Reasons, from Luna's own client data:

1. Highest booking volume: 9 dates booked across Oct and Nov at Bree 2910, so more guests and more messages than anyone else. That's where the pain is and where a pilot shows results fastest.
2. A regular of Nita's, so trust exists and feedback will be honest.
3. One known building (Bree Street), so the sheet of house facts is small and easy to get right.

**Second: Kobie** (same Bree area, books a month ahead, probably several apartments). **Third: Megan** (two Airbnb units, so a good test that the same product works on Airbnb). Order is a guess until Fancy and Nita answer questions 1 and 3 in the questions file, which show where each host books and how many messages they get. If Fancy is Airbnb only, or gets fewer than 5 messages a day, swap to whoever has the most Booking.com traffic.

Each host is a stand-alone product. Shared building facts (Bree Street parking, for instance) get copied into each host's sheet, never linked.

---

## Integration Type

**Classification:** App (Make scenario plus source folder), same shape as Luna.
**Reasoning:** Luna already proves Make plus Meta Cloud API plus Claude plus Google Sheets in production. A Node service would be faster to extend but breaks the "Theo can open it in Make" habit and adds hosting. Reuse wins for a pilot.
**Location:** `apps/host-assistant/` (source, with a `template/` for stamping out the next host), `plans/` (this file), `docs/host-assistant.md` (via `/document` after it works), `context/` (new satellite page).

---

## Proposed Changes

### Summary of Changes

- Per host: new SIM and WhatsApp number, new Meta app, new Make scenario in its own folder, new Google Sheet, new Claude API key. Nothing shared with Luna, Lexi or another host.
- A guest conversation with three paths: **ask** (Claude answers from the sheet), **extras** (tap a button, confirm, logged and sent on), **host** (anything the assistant must not decide goes to the host).
- A daily extras list to the host, with urgent items sent straight away.
- QR code and wording for the Booking.com scheduled message.
- Phase 3: direct bookings through the same number for repeat guests.

### New Files to Create

| File Path | Purpose |
|-----------|---------|
| `apps/host-assistant/README.md` | Plain-English source notes, same style as Luna's README |
| `apps/host-assistant/system-prompt.txt` | Claude instructions: answer only from the sheet, never invent, route the rest to the host |
| `apps/host-assistant/template/` | Sanitised blueprint with `PASTE_...` placeholders for number, token, sheet ID, key |
| `apps/host-assistant/build_blueprint.py` | Builds the blueprint from parts, as Luna does |
| `apps/host-assistant/code/` | Make Code steps plus `node` tests |
| `outputs/rags-to-riches/host-assistant-questions.txt` | The questions to send (written today) |
| `outputs/host-assistant/fancy-guest-qr-and-message.md` | QR instructions and the Booking.com scheduled message text |
| `docs/host-assistant.md` | Documentation, filed with `/document` |
| `context/host-assistant.md` | Satellite page for the product, price, hosts, status |

### Files to Modify

| File Path | Changes |
|-----------|---------|
| `CLAUDE.md` | Add the satellite and the `apps/host-assistant/` folder once they exist |
| `context/rags-to-riches.md` | One paragraph linking the host product and the extras-as-jobs tie-in |
| `context/tech-stack.md` | Row for each host number once bought |
| `docs/_index.md` | Index the new doc |
| `ledger/theo.md` | Rows as each step completes |

### Files to Delete

None.

---

## The sheet (one per host)

Three tabs. Row 1 is headers, exactly as written, because the scenario maps by column letter.

- **House**: two columns, `topic` and `answer`. Wifi name and password, parking, bins, how the TV, aircon and stove work, check-out time, house rules, nearby food and shops. This is the only thing Claude may answer from.
- **Extras**: `item`, `free_or_paid`, `price_zar`, `who_delivers`, `available` (yes/no). The extras buttons are built from this tab.
- **Requests**: `timestamp`, `guest_wa_id`, `guest_name_if_given`, `item`, `note`, `urgent`, `status` (new, sent, done), `sent_at`.
- Plus **ChatMemory** (last messages per guest, for context), same as Luna.

Door and lockbox codes do **not** go in the sheet. The pilot default is that the assistant says "your check-in details are in your Booking.com message". Revisit only if the host wants it.

---

## Design Decisions

### Key Decisions Made

1. **Stand-alone per host.** Own number, Meta app, scenario, sheet and Claude key. A problem at one host can't touch another, and a host who leaves takes nothing of anyone else's. Cost: setup per host. Mitigation: the `template/` folder, so host two is a copy and a paste of placeholders.
2. **The guest starts the chat.** A guest scanning the QR or tapping the link opens the conversation, so replies fall inside WhatsApp's 24-hour window. No template approval needed for the guest side.
3. **Only confirmed guests get the link.** The QR sits inside the apartment and the link goes in Booking.com's post-booking scheduled message. Nothing is posted on the public listing.
4. **Claude answers only from the House tab.** If the answer isn't there, it says "I'll check with your host" and logs it as a request. No guessing wifi passwords or inventing rules.
5. **Never decides money or exceptions.** Late check-out, refunds, price changes, damage, complaints go to the host. The assistant tells the guest the host has been told.
6. **Urgent goes straight through.** Water, power, lockout, safety: instant message to the host. Everything else waits for the daily list.
7. **Host alerts need a Meta template.** A message to the host outside their own 24-hour window must be a pre-approved template. Luna's booking alert to Nita is parked on exactly this. Easiest fix: host messages the number once a day (a "hi"), or we get one utility template approved per number. Decide in Step 4.
8. **Direct bookings are their own plan.** A host-owned booking page plus the assistant, see `plans/2026-10-25-host-direct-booking-channel.md`. It builds on this plan and runs after the messaging half works.
9. **Pilot is free for one month.** In return: weekly feedback and a testimonial if earned. No invoice until it has saved the host real time.

### Alternatives Considered

- **Overseas tools (HostBuddy, Hospitable, Nowistay, others):** work through a PMS the hosts don't have, dollar or euro billing, no link to Nita's team. Kept as the comparison in the pitch.
- **Booking.com's own auto-replies and scheduled messages:** free and under-used. We set these up for every host as a quick win, and they carry our link. Not a replacement, since they can't answer free-form questions.
- **One shared number for all hosts:** cheaper, but breaks the stand-alone rule and a guest of host A could see host B's name. Rejected.
- **Node service:** more flexible, more to host. Revisit only if Make gets too heavy, as it did with Lexi.

### Open Questions

1. **Price.** Nothing set. Overseas tools start around EUR 12 per property per month (about R240 at current rates, to be checked). Directional suggestion: R199 to R299 per apartment per month for the assistant, with the extras revenue going to Nita. Decide after the free month.
2. **Does Booking.com allow an external WhatsApp link in scheduled messages?** Check partner.booking.com's messaging rules before printing anything. Fallback: put the QR in the apartment and a plain "message us on WhatsApp +27..." line.
3. **Meta pricing in Rand** for host-alert templates (utility). Check before promising a monthly fee.
4. **Persona name.** Luna is Nita's. Do hosts get their own name, or one product name with the host's apartment name in the greeting? Suggest the apartment's name, so it feels like their place.
5. **Does the host or Nita's team get the list?** Question 9 to the host and question 1 to Nita decide it.
6. **Branch merge.** Luna's source is on `claude/charming-tesla-j7vsii`. Merge it into main before copying its code, or the new app has nothing to copy from.

---

## Step-by-Step Tasks

Steps marked **Theo** need him. Everything else Claude does.

### Step 1: Send the questions

**Theo:** send `outputs/rags-to-riches/host-assistant-questions.txt` Message 1 to Fancy and Message 2 to Nita. Message 3 is spare for Kobie or Megan.

**Actions:**

- Save answers into a new `context/host-assistant.md` (no codes, no passwords, those go in the host's sheet only).
- Confirm the pilot host from questions 1 and 3. If Fancy is not on Booking.com, switch to the next host.

**Files affected:** `context/host-assistant.md`

---

### Step 2: Quick win for the pilot host (no build)

**Actions:**

- Write the Booking.com scheduled check-in message and an auto-reply for common questions, in the host's voice, using their answers.
- Walk the host through Property > Messaging Preferences in the extranet.

**Files affected:** `outputs/host-assistant/fancy-guest-qr-and-message.md`

---

### Step 3: Accounts and number (Theo, Claude guides)

**Actions:**

- **Theo:** buy a SIM for the host's number, create a Meta app and WhatsApp Business Account, generate a permanent token (system user), note the Phone Number ID.
- **Theo:** create a new Claude API key for this host only.
- **Theo:** create the host's Google Sheet in his Drive and share it with the host as viewer.
- Claude gives click-by-click steps and checks with a test message.

**Files affected:** `reference/getting-keys.md`, `context/tech-stack.md`

---

### Step 4: Decide how the host is alerted

**Actions:**

- Check Meta's current Rand price for a utility template.
- Choose between a daily "hi" from the host, a pre-approved template, or Nita's team receiving the list inside a window they keep open.
- Write the choice in the plan's decision log.

---

### Step 5: Merge Luna's source and create `apps/host-assistant/`

**Actions:**

- Merge `claude/charming-tesla-j7vsii` into main (or copy `apps/rags-to-riches-bot/` across) so the Luna pattern is on this branch.
- Create the folder layout above. Copy the webhook, config, session-lookup, ChatMemory and send steps from Luna.
- Remove all booking and calendar steps. Add the three paths.

**Files affected:** `apps/host-assistant/*`

---

### Step 6: Build the three paths

**Actions:**

- **Ask:** Claude gets the House tab and the guest's message, returns structured JSON (`answer`, `needs_host`, `urgent`). Temperature 0, thinking off for speed, `max_tokens` as a number (Lexi's bug from 23 Sept).
- **Extras:** buttons built from the Extras tab, a confirm step ("One extra towel set, free, I'll let your host know"), a write to Requests, and a reply with what happens next.
- **Host:** anything with `needs_host` or `urgent` writes a Requests row and sends the alert.
- Reply speed target: under 20 seconds, same rule as Lexi.
- Node tests for each Code step, as Luna does.

**Files affected:** `apps/host-assistant/code/*`, `system-prompt.txt`

---

### Step 7: Daily list

**Actions:**

- Scheduled scenario at the host's chosen time: collect Requests where `status = new`, group by item, send one message, mark `sent`.
- Quiet when there is nothing to send.

---

### Step 8: Test

**Actions:**

- Fake guests from 3 test numbers, in English, Afrikaans, and one foreign-language message.
- Tricky cases: a guest asks for the wifi password of another apartment, asks for a refund, claims to have no water, asks for something not on the Extras tab, sends a voice note, sends the same message twice.
- Verify Claude never invents an answer that isn't in House.
- Run `/test` before calling it done.

---

### Step 9: Go live with the pilot

**Actions:**

- **Theo:** print the QR (links to `wa.me/<number>?text=Hi`) and put it in the apartment; **host** adds the link to the scheduled message.
- Watch the first three real guest chats read-only. Fix wording the same day.
- Ledger row for every fix.

---

### Step 10: Review after the free month

**Actions:**

- Count: guest messages handled without the host, extras requested, extras that became paid jobs for Nita, host hours saved (host's own estimate).
- Decide price and whether to roll to Kobie and Megan using `template/`.

---

### Step 11: Direct booking channel

See `plans/2026-10-25-host-direct-booking-channel.md`: a booking page per host, the assistant takes the booking, holds dates, EFT payment, iCal checks against Booking.com and Airbnb to avoid double bookings.

---

## Connections & Dependencies

### Files That Reference This Area

- `reference/research/2026-10-20-booking-com-guest-messaging.md`
- `context/rags-to-riches.md`
- `apps/rags-to-riches-bot/` (on the other branch)

### Updates Needed for Consistency

- `CLAUDE.md` map and satellite list, once the folder exists.
- `docs/_index.md`, through `/document`.

### Impact on Existing Workflows

None on Lexi or Luna. The host assistant shares nothing with them except the pattern. Merging Luna's branch into main is the only touch point.

---

## Validation Checklist

- [ ] Questions answered by the host and Nita
- [ ] Pilot host confirmed on Booking.com or Airbnb with enough messages to matter
- [ ] Own number, Meta app, scenario, sheet and Claude key, none shared
- [ ] Assistant replies in under 20 seconds
- [ ] It only answers from the House tab
- [ ] Extras reach the host as one list
- [ ] Urgent items reach the host immediately
- [ ] No door codes or passwords in the repo or in Claude's prompt

## Success Criteria

1. A real guest at the pilot apartment gets a correct answer to a wifi or check-in question from the assistant, with the host doing nothing.
2. At least one extras request reaches the host in the daily list and gets delivered.
3. After one month, the host says it saves time and wants to keep it.
4. At least one extra becomes a paid job for Rags to Riches.

---

## Notes

- Quick free wins before any build: set up Booking.com auto-replies for every host.
- Never put wifi passwords, lockbox codes or phone numbers into this repo. They live in each host's own sheet.
- Compare against the overseas tools in the pitch, but lead with the pain (messages at 11pm for a fan), not the tech.
- Source for the commission figures and tool list: the research file above.
