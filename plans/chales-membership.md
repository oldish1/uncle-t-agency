# CHALES membership tracker: spec and review

Status: **waiting on Chanté's answers** (Theo is asking her on 2026-09-24). Nothing built yet.

## The package (as confirmed by Chanté, via Theo's spec)

- One package: **6 Wash & Blowdry for R650**. In Lexi the service is called "Wash and Blowdry".
- A basin treatment is included on visits 2, 4 and 6.
- It only covers Wash and Blowdry. Any other service is a normal booking.
- It expires 3 months after the start date, even if washes are left.
- It's sold in the salon only (card machine or EFT). Chanté or Theo activates a member by adding a row to the sheet.

## Planned flow

1. **New "Memberships" tab** in the Client Database sheet. Columns: Phone | Name | Package | Total Washes | Used | Remaining | Start Date | Expiry Date | Status. All columns are plain text. Status is Active, Depleted or Expired.
2. **When a booking is confirmed** (the name-capture route in "Chales Hair Boutique"), Lexi looks the client up by phone. If they're an active, unexpired member and the service is Wash and Blowdry, she adds 1 to Used and takes 1 off Remaining. The confirmation then says how many washes are left, and whether this visit includes the basin treatment.
3. **Final wash:** Lexi tells the client "This is your final wash… reply RENEW" and alerts Chanté.
4. **Balance question** ("how many washes do I have left"): Lexi replies with what's remaining, the expiry date and the next treatment visit. Non-members get the R650 package explained.
5. **RENEW:** Lexi alerts Chanté with the client's name and number.
6. **Failsafe:** if the membership check ever breaks, the booking still goes through as normal.

## Review notes (Claude, 2026-09-23): fix before building

1. **Wrong Phone Number ID in the spec.** 1170555039465381 is the ID that caused the "Object does not exist" Bad Request errors today. The live, working ID is **1197696726762690**. Use that one.
2. **Which scenario.** The spec says to build on "Lexi 2.0 lean, NOT the old 1.0". The Lexi on Chanté's real number is the scenario **"Chales Hair Boutique" (5043763)**, the one sped up and tested today. "Lexi 2.0 TEST" isn't connected to her clients. The membership has to go into Chales Hair Boutique, or her clients will never see it.
3. **Chat Memory Sheet ID typo.** The spec has `...t91luUjZY` (lower-case L). The real ID is `...t91IuUjZY` (capital i).
4. **Code blocks vs speed.** The spec says to use code modules for all logic. Today's timings showed each Make code module adds about 2–3 seconds. That's why fix10 and fix11 replaced them with formulas, which were tested before going live. Plan: formulas for simple lookups and maths, one code module only where the logic is genuinely complex.
5. **Cancel and reschedule must give the wash back.** The wash is deducted when the booking is confirmed. So if a member cancels through Lexi, the wash needs to go back on the card. A reschedule re-books, so without a refund it would deduct twice. This isn't in the spec, but it's needed.
6. **Alerts to Chanté need a WhatsApp template.** Lexi can only message Chanté freely if Chanté messaged the Lexi number in the last 24 hours. Options: a second approved template (e.g. `staff_alert`), or email alerts to Chanté instead, which need no template.
7. **Balance and RENEW as keywords, not AI.** Plain keyword checks answer in about 2 seconds. Routing through the AI adds about 10. Proposal: catch "RENEW", "balance", "washes left" and similar with the same instant keyword formula Lexi already uses for cancel.
8. **wa_id vs messages[].from.** These are the same number in practice. New modules will use contacts[].wa_id as the spec asks. The existing modules keep working either way.

## Open questions for Chanté

- **No-show policy.** Spec default: the wash counts once the booking is confirmed, so a no-show uses a wash. Built to be switchable. Does she agree?
- **Cancellations.** If a member cancels with notice, do they get the wash back? (Recommended: yes, if they cancel before the day.)
- **Alerts.** Does she want them on WhatsApp (needs a second template) or by email?
- **Expiry.** 3 months from the date she activates the card, or from the first wash?
- **Member warning.** When a member books something other than Wash and Blowdry, should Lexi mention it won't come off their card?
