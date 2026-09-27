# CHALES membership tracker: spec and review

Status: **answers in, building now** (2026-09-25). Photo pick still outstanding but doesn't block this build.

## Chanté's answers (2026-09-25)

1. **No-shows do NOT count** — client keeps their wash. (Overrides the spec's default assumption.)
2. **Cancelling with notice gives the wash back** — yes.
3. **Alerts to Chanté** — WhatsApp (needs the alert template, see review note 6).
4. **Expiry** — 3 months from the moment they pay, i.e. the activation date.
5. **Member books a non-qualifying service** — Lexi mentions it won't use up a wash.
6. **Photo** — not yet confirmed which version, or if changes are wanted.

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

Sent to Theo on 2026-09-24 to forward to Chanté:

1. **No-shows.** Spec default: the wash counts once the booking is confirmed, so a no-show uses a wash. Does she agree, or should a no-show not count?
2. **Cancellations.** If a member cancels with notice (not a no-show), do they get the wash back? (Recommended: yes.)
3. **Alerts.** Does she want alerts (last wash, renew requests) on WhatsApp or by email?
4. **Expiry.** 3 months from the date she activates the card, or from the first wash?
5. **Member warning.** When a member books something other than Wash and Blowdry, should Lexi mention it won't come off their card, or stay quiet?
6. **Salon photo.** She also asked for a photo of the salon on the booking confirmation, Fresha-style (photo header, bold booking details, a button). Chales has no separate booking site, so the button becomes "Get Directions" → Google Maps, not Fresha's "Manage appointment". Needs: the photo, plus a new WhatsApp template approval (same process as `appointment_reminder`). Can be built as soon as the photo arrives, independent of the membership answers.
   - Draft layout: photo header; body "Hi {{1}}, your appointment with Chales Hair Boutique is confirmed! ✨" + Date/time, Service, Address; button "Get Directions" linking to the salon's Google Maps location.
   - Photo needs a professional edit pass (better lighting/colour, tighter crop) before use, not the raw phone photo as-is. Claude to produce 2-3 edited versions from the photo Chanté sent for Theo/Chanté to pick from.
7. **Calendar visit tracking.** Chanté wants to see the membership count in Google Calendar itself, the way she already manually writes "Suzaan week4" on repeat clients. Plan: when the membership tracker books a member, the GCal event title includes "(Visit X of 6)", e.g. "Booking-Wash and Blowdry-Sarah (Visit 4 of 6)". No extra tool for her to check, same place she already looks.

## Reusable client template (separate track, not blocked on the above)

Theo asked how to turn Chanté's Lexi into a template for the next client. Claude can't create WhatsApp numbers or sign into a new client's Google account (browser-only steps), so the split is:

**Theo does, per new client (~30-45 min):**
1. Get the client's WhatsApp Business number added in Meta (WhatsApp Manager → Phone Numbers).
2. Copy the Chales Hair Boutique Google Sheet for the new client.
3. Add that client's Google Sheets/Calendar/WhatsApp as new connections in Make.
4. Send Claude: the new phone number ID, sheet ID, services list, salon rules text.

**Claude does:** clones Chales Hair Boutique's blueprint, swaps in the new client's number/sheet/calendar/services, hands back the file to import as a new scenario.
