# Reusable client template: Lexi for the next paying client

Status: **template ready** (2026-09-27). Built from the live, fully-working, membership-and-dedup-proven Chales Hair Boutique scenario. No second client signed yet — this is the prepared groundwork so onboarding one is fast when it happens.

## What this is

`private/lexi-client-template-blueprint.json` — a sanitised copy of Chales' Lexi. Every credential and Chales-specific ID has been stripped and replaced with a clear placeholder:

| Placeholder | What it replaces |
|---|---|
| `{{WHATSAPP_ACCESS_TOKEN}}` | Chanté's live WhatsApp Bearer token |
| `{{ANTHROPIC_API_KEY}}` | The Claude API key Lexi's AI replies use |
| `{{WHATSAPP_PHONE_NUMBER_ID}}` | Chanté's WhatsApp phone number ID |
| `{{GOOGLE_SHEET_ID}}` | The Chales Client Database spreadsheet ID |
| `{{GOOGLE_CALENDAR_EMAIL}}` | Chanté's Google Calendar address |
| `{{CLIENT_NAME}}` | The scenario's own name |

Verified clean: no trace of the real token, key, phone ID, sheet ID, or calendar email remains anywhere in the file. The webhook binding was also stripped (so importing this never accidentally attaches to Chanté's live webhook) — Make will ask for a fresh one on import.

## Theo does, per new client (~30–45 min)

1. Get the client's WhatsApp Business number added in Meta (WhatsApp Manager → Phone Numbers), and note its **Phone Number ID**.
2. Copy the Chales Hair Boutique Google Sheet for the new client (Sheet1, Memberships, ProcessedMessages, BookingSession tabs — keep the same column headers). Note the new **Spreadsheet ID**.
3. Confirm the client's **Google Calendar** email address (their own, or one you set up for them).
4. In Make: add new connections for that client's WhatsApp, Google Sheets, Google Calendar (OpenAI/Anthropic connections can often be shared across clients if you're using your own API keys — confirm with Claude at build time).
5. Send Claude: the new phone number ID, sheet ID, calendar email, client's business name, salon/business address, services list, and any rules specific to how they want Lexi to behave (booking hours, cancellation policy, whether they want a membership/loyalty feature too).

## Claude does, per new client

1. Take `lexi-client-template-blueprint.json`, fill in the six placeholders above with the client's real values.
2. Rewrite the salon-specific copy — the actual business name, address, services list, and staff name — in these 11 modules (mapped once, so this is fast per client):

| Module ID | Type | What's hardcoded there |
|---|---|---|
| 3 | AI reply (Claude) | Business name, staff name, address, full services list |
| 38 | Calendar event | Business name, address |
| 57 | AI reply (Claude) | Business name, staff name, services list |
| 81 | Calendar event | Address |
| 305 | Voice transcription prompt | Business name, services list (helps transcription accuracy) |
| 320 | Code (greeting logic) | Services list |
| 322 | WhatsApp reply | Business name, staff name |
| 330 | Confirmation message + photo | Business name, staff name, address, photo URL, maps link |
| 334 | Membership calc (optional) | Service name check ("Wash and Blowdry") |
| 340, 352 | Membership sheet writes (optional) | Service name check |

3. If the client doesn't want the membership/loyalty feature, remove modules 333, 334, 336, 337 (booking-side) and 338, 340 (cancel-side refund) and the balance/renew branch (341–346, 353–355) — these are Chales-specific add-ons, not part of the core booking bot.
4. Hand back the finished, filled-in blueprint file for Theo to import as a brand-new scenario.

## What's proven and carries over untouched

Everything that isn't salon-specific copy is already battle-tested from today's work and needs no rebuilding per client:
- Fast booking flow (service → day → time → name, 2–5 second replies)
- Real cancel and reschedule, with a "different date instead?" offer
- Voice note handling (transcribe → treat as text)
- Duplicate-message protection (the dedup guard, useful for ANY client, not just membership — worth keeping even if they skip the loyalty feature)
- Appointment reminders (separate scenario, same swap-the-IDs approach applies)

## Not yet decided

- Whether the appointment-reminders scenario also needs its own template version (it's small — 5 modules — so probably a 10-minute job when the time comes, not started tonight).
- Pricing/packaging for what a new client pays for this vs. what Chanté paid, since Chanté was effectively the pilot build.
