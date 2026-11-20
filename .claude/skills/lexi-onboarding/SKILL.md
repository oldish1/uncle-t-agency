---
name: lexi-onboarding
description: >
  Onboard a new paying client onto Lexi, the WhatsApp booking assistant (and the website that goes with it).
  Use when the user says a client signed, "onboard", "set up Lexi for", "second client", "new client",
  "go live for <business>", "clone the Chales scenario", or asks what's needed to start a client. Walks intake,
  accounts, the build from the sanitised Chales template, safe testing, go-live, and the first week.
user-invocable: true
---

# Lexi onboarding

How to take a signed client from "yes" to live and booking, without repeating the mistakes made on CHALES (Aug to Nov 2026). Source material: `plans/client-template.md`, `context/lexi.md`, `scripts/lexi/`, `outputs/handoffs/`, the ledger rows tagged `lexi/` and `security/`, and `outputs/2026-11-08-chales-review-machine-setup.md`.

Working rule from `CLAUDE.md`: done is deployed and making money, not polished. But no paying client goes live until Lexi replies in under 20 seconds, which CHALES now does (greeting about 2 s, each tap 2 to 7 s).

## Before anything: look first

1. Check whether this client already has files: `outputs/clients/`, `outputs/`, `plans/`, other branches (`git branch -r`), the ledger.
2. Confirm the deal in `context/numbers.md` and the ledger (price, setup fee, free period, founding-five terms, whether the website is included). As of 16 Nov 2026: Lexi or website R1,499 setup + R499 a month, both for R899 a month, founding five at R999 setup, R499, 30 days free. Verify, prices change.
3. Make the client file: `outputs/clients/<slug>/onboarding.md` (copy the table from `references/intake.md`). Keep all client facts there, never tokens.

## The six phases

### 1. Intake (Theo with the owner, 20 minutes)

Use `references/intake.md`. The answers become the fill-in values for the template. The questions people forget: the address detail that gets customers to the door ("inside the Vodacom building" for CHALES), the **real WhatsApp number the owner checks** for staff alerts (on CHALES the alerts first pointed at Lexi's own number and never reached Chanté), real hours, which services take how long, cancellation rules, and whether they speak Afrikaans with clients.

### 2. Accounts and access (Theo, 30 to 45 minutes)

From `plans/client-template.md`:
1. WhatsApp Business number added in Meta (WhatsApp Manager, Phone Numbers). Note the Phone Number ID. Confirm in WhatsApp Manager what Meta currently requires for a number already used on the regular WhatsApp app, don't assume.
2. Copy the CHALES Google Sheet for the client (tabs: Sheet1, Memberships, ProcessedMessages, BookingSession, keep the same column headers). Note the Spreadsheet ID.
3. The client's Google Calendar email (theirs or one made for them).
4. New Make connections for that client's WhatsApp, Sheets, Calendar. Anthropic and OpenAI connections can be shared if using Uncle T's keys (confirm).
5. Tokens and keys go straight into Make connections. Never into chat, the repo, or a client folder.

### 3. Build (Claude)

1. Template: `private/lexi-client-template-blueprint.json` (on Theo's machine, `private/` doesn't sync). If it's missing in this session, ask Theo to export the current CHALES scenario (5043763) from Make or fetch it with the Make tools, then sanitise it again: replace the token, API key, phone number ID, sheet ID, calendar email and scenario name with `{{PLACEHOLDERS}}` and strip the webhook binding.
2. Fill the six placeholders. Rewrite the client-specific copy in the 11 modules listed in `plans/client-template.md` (business name, staff name, address, services, photo, maps link). Services must be the client's real list. Do not reuse CHALES examples (Chanté does not do braids).
3. Membership modules (333 to 346, 353 to 355) only if the client wants a loyalty feature. Otherwise remove them. Keep the dedup guard (ProcessedMessages) either way.
4. Reminders are a separate scenario (CHALES: 7617803, daily 17:00, template `appointment_reminder`). No sanitised template yet, build the client's copy from the live one.
5. Edit rules learned the hard way: see `references/lessons.md`. The short version: never insert Make routes before existing ones, code-module output is under `.result.`, Make has no `or()`, and test any new formula in a throwaway scenario then delete it.
6. A blueprint of this size (about 230K characters) can't be pushed through the Make tool in one call without risking a broken live scenario. Produce the import file for Theo to import in the Make editor, or make small field-level edits.
7. Fresh webhook for this client. Import as a **new** scenario so it can never attach to another client's webhook.

### 4. Test safely (Theo and Claude)

Order matters because of the cross-contamination incident (19 Sept): a test call once subscribed Chanté's live app to the demo account, so test messages triggered her real scenario.
1. Test on the demo number or the client's own number with the **scenario switched on only for that webhook**. Before testing, check the client's WhatsApp Business account has its own webhook, with no leftover per-number override pointing at another client's callback URL.
2. Run `references/go-live-checklist.md` section "Test flow". Measure response times and write them down. Under 20 seconds end to end or it doesn't ship.
3. Check CHALES (or any other live client) did not receive anything during the tests.

### 5. Go live (Claude and Theo, same day)

Use `references/go-live-checklist.md`. Key items: reminder template created and approved in the client's WhatsApp Manager, test-mode gates removed (CHALES reminders ran in test mode for four days before anyone noticed), staff alert number is the owner's real WhatsApp, Lexi's number added to every place customers book from (Google profile appointment link, social bios, website buttons, QR on the counter), the owner briefed in plain words on what Lexi does and how to take over a chat.

### 6. First week and after

- Day 1, 3, 7: check the scenario's execution log for errors and look at real conversations. Fix, don't wait.
- Ask the owner what customers said.
- Founding-five clients: agree the one trackable metric at signing (bookings through Lexi per week, no-shows, or similar) and collect the testimonial at day 30.
- Offer the next thing only when it's proven: review machine, win-back messages (see `/seo` and `outputs/2026-11-20-get-found-offer.md`).
- Update the client file, `context/numbers.md` (paying clients), `context/lexi.md` (anything learned), write ledger rows as you go.

## Hard rules

- No secrets in chat, repo, outputs or ledger. If one shows up in a screenshot, say so and rotate it.
- Never edit a live client's scenario without a fresh fetch first and a plan to roll back.
- Don't give one client's webhook, number ID or sheet to another client's scenario.
- Say what wasn't tested. Never report "live" for something that wasn't run with a real message.
- The repo `oldish1/chales-assets` holds public images only. Client photos for confirmations go in a public images repo, nothing private in there.

## References

- `references/intake.md`: the questions and the fill-in table.
- `references/go-live-checklist.md`: test flow and go-live list.
- `references/lessons.md`: every Lexi mistake worth not repeating.
