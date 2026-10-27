# Lexi 2.0 — Design Decisions

**Status:** Design locked, Phase 1 build in progress.
**Source:** `plans/lexi2-architecture-map.md` (current live Chales scenario, 340 modules).
**Theo's brief:** mirror Chales for testing, keep Google Sheets as the backend, he tests it himself before any cutover, tap-menus everywhere ("more convenient and easy for the clients").

## The five fixes

1. **Structured AI output, not free text.** The AI brain never writes a menu, slot list, or confirmation as prose again. It outputs one JSON action per turn — `{"action":"show_service_menu"}`, `{"action":"show_slots","service":"...","day":"..."}`, `{"action":"confirm_booking","service":"...","datetime":"...","name":"..."}`, `{"action":"chat","text":"..."}` for genuine conversational replies only. A deterministic step turns the action into the right WhatsApp payload. This removes the stray-quote/broken-JSON crash class entirely, because the AI's text never gets hand-parsed into something structural again.
2. **Tap menus everywhere, no exceptions.** Every action that used to render as typed text (Stage 1/1B greeting menu, the CHECK_AVAILABILITY slot list, the post-cancel re-offer) now routes through one shared interactive-message builder, the same mechanism that already works correctly in module 57 — just reached from every entry point instead of one.
3. **Per-phone locking, not whole-scenario sequential processing.** A `Locked` flag + timestamp on each BookingSession row, checked/set at the top of the flow. Two different clients messaging at the same moment no longer queue behind each other; the same client's own double-sent messages still can't race. This is the real fix for the "badresponder" warnings — they're a symptom of forcing every client through one global queue, not a sign anything is actually broken.
4. **Booking write order: Sheets first, then Calendar.** Chales currently writes the calendar event before the Sheets row, so a failed Sheets write (like the Oct 25 storage incident) leaves a real calendar booking with no record of it anywhere. Lexi 2.0 writes the source-of-truth row first.
5. **One AI gate, not five copies.** Chales reaches the same single AI call from 5 separately-built "no intent, no pending reply" filter branches. Lexi 2.0 collapses this into one shared path.

## What's carried over as-is (already solid)

- Ack-Meta-immediately-then-process pattern (`WebhookRespond` before real work starts).
- `ProcessedMessages` idempotency guard against webhook retries.
- Voice-note transcription via Whisper, self-feeding back into the main flow as if it were typed text.
- The raw conversation-transcript logging sheet (separate spreadsheet) — useful for debugging, kept untouched.
- Single calendar (`herbertchante3@gmail.com`), `Africa/Johannesburg` timezone, the existing slot-duration logic (60/120 min, minus 1 min buffer).

## Phasing

**Phase 1 (building now):** the core booking path — greeting → tap service menu → tap slot picker → name capture → confirm, with all five fixes above applied, built and deactivated in its own Make scenario, tested by me with sample payloads before Theo ever touches it.

**Phase 2 (after Phase 1 is proven):** port cancel/reschedule, membership wash-credit logic, and voice-note handling into the same hardened architecture.

This is deliberately staged rather than a single 340-module rewrite in one pass — proving the hardened core works beats a bigger scenario nobody's tested yet.

## Testing handoff

Once Phase 1 passes my own sanity checks, it gets handed to Theo as a deactivated scenario he can run manually inside Make (no live WhatsApp number touched) using the test matrix in the architecture map, before any cutover decision.

## Phase 1 build — done 2026-10-26

Built directly as a new, isolated Make scenario (id 8179409, "Lexi 2.0 (test core flow)"), created **inactive** — never touches live Chales traffic. Own webhook (3977281), own test Sheets tabs (Lexi2_BookingSession/Sheet1/Memberships/ProcessedMessages). 30 modules, structured AI JSON output, per-phone locking, tap-menus for service list and slot list, Sheets-first-then-Calendar write order.

**Before testing, Theo needs to:**
1. Open the scenario in Make and paste his real WhatsApp bearer token into the 7 HTTP modules currently holding `PASTE_YOUR_WHATSAPP_TOKEN_HERE`, and his Anthropic key into the 2 holding `PASTE_YOUR_ANTHROPIC_KEY_HERE`. Left as placeholders deliberately — never handled the real secrets outside Make.
2. **Calendar decision needed**: the slot-check and booking-write modules point at the real calendar (`herbertchante3@gmail.com`) — same one Chales uses live. Test bookings would create real-looking events on Chanté's actual calendar. Flagging for Theo: either accept that for now and delete test events after, or swap in a second test calendar before running real bookings through it.
3. Test via Make's "Run once" manual test feature (feed it a sample WhatsApp webhook payload) rather than connecting it to any real WhatsApp number yet — fully isolated from live traffic either way.

**Not yet ported (Phase 2):** cancel/reschedule, membership wash-credit logic, voice-note transcription. Core booking path only for this pass.

## Phase 1.5 — reminders compatibility + cancel/reschedule — done 2026-10-27

Found a scenario that was missing from the original architecture map: **"Chales - Appointment Reminders"** (id 7617803), a separate daily cron scenario (17:00 SAST) that scans Chanté's calendar for tomorrow's events and sends a WhatsApp reminder template, parsing the booking's phone/service out of the event description's `Client:X Phone:Y Services:Z` text. Lexi 2.0's calendar event description was fixed to match that exact format (no spaces after colons, "Services:" plural) so this reminder system keeps working for her bookings without any changes to it.

Also found two older, unrelated prototypes already sitting in the Make account — **"Lexi 2.0 TEST"** (id 7288450, built Sept 2026, dormant/unattached webhook, not interfering with anything) and **"Lexi 2.0 TEST (OLD - archived, do not use)"** (id 7226977). Assessed the first one: same free-text/regex plumbing bugs as the live bot (no AI structured output, no tap-menus, fragile date-string parsing), not worth inheriting as code — but its cancel/reschedule **business rules** were sound and were ported cleanly into the new structured-action design:

- A client needs an existing Sheet1 row with Status=Confirmed for their phone to have anything to cancel/reschedule.
- The matching calendar event is found by day + service name, then deleted.
- The original Sheet1 row is never deleted — a new audit row is appended with Status=Cancelled, so there's always a record.
- Reschedule = cancel the old booking, then let the normal booking flow (tap menu) pick a new slot — no separate "move" step.

Implemented as two new AI actions (`cancel_booking`, `reschedule_booking`) added to both AI calls' system prompts, with matching logic chains added to both the "has session" and "fresh conversation" branches of scenario 8179409. Also fixed a structural bug from the Phase 1 build along the way: the "fresh conversation" branch had two sequentially-filtered modules instead of a proper router, meaning a plain "chat" reply from a brand-new conversation would never have sent — now wrapped in a real `builtin:BasicRouter` like the rest of the scenario.

**Still not ported:** voice-note transcription, the double-booking re-check at final confirm (current Lexi 1.0 re-checks the slot is still free in the split-second before booking; 2.0 doesn't yet). "Reminders" specifically turned out not to need porting at all — it already works for any booking on the calendar regardless of which scenario created it, now that the description format matches.

## Phase 1.6 — membership wash-credit logic — done 2026-10-27

Ported the full membership wash-credit system from Chales's live scenario into Lexi 2.0, using the exact business logic read straight out of the live bot's own code (not guessed):

- **Deduction on booking.** When a client confirms a "Wash and Blowdry" booking and has an active, unexpired membership, Lexi 2.0 looks them up in the Memberships sheet, deducts one wash, and updates their remaining balance — same as live. If that was their last wash, it quietly flags staff via WhatsApp so Chanté can follow up about renewing. The booking confirmation message now also tells the client their remaining balance.
- **Balance / renewal query.** A client can ask "how many washes do I have left" or "I want to renew" at any point — handled in both ongoing and brand-new conversations — and gets their real balance, next free-treatment visit, and expiry date, or (if not a member) a short pitch for the R650 membership. A renewal request also quietly pings staff.
- **Refund on cancel.** Cancelling or rescheduling a Wash and Blowdry booking that used a membership wash credits that wash back automatically.

Built as new, self-contained module chains (ids 4000–4003, 4100–4103, 4200–4203, 4300–4302, 4400–4402) inserted into the existing confirm/cancel/reschedule flows in both the "has session" and "fresh conversation" branches — nothing existing was rewired, so Phase 1/1.5 logic is untouched. Every membership lookup has a safe `builtin:Resume` fallback on error, so a Sheets hiccup on the Memberships tab can't crash someone's booking.

Pushed to the live Lexi 2.0 scenario (8179409) via a full blueprint replace — still deactivated, still fully isolated from real WhatsApp traffic.

**Still not ported:** voice-note transcription, the double-booking re-check at final confirm, and an idempotency guard on membership deduction/renewal-alerts specifically (the live bot tags processed messages to stop a webhook retry double-deducting a wash; Lexi 2.0's `Lexi2_ProcessedMessages` sheet exists for this but isn't wired to the membership modules yet — worth doing before any real client's membership money is riding on it).
