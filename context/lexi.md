# Lexi (the flagship product)

> The WhatsApp AI booking assistant behind The Lexi System. This file tracks what Lexi does, where the current build falls short, and what the 2.0 rebuild needs to fix. See `context/offer.md` and `context/strategy.md` for pricing and the priority order.

## What it does today

Greets the customer on WhatsApp, lists services, takes date and time, checks live calendar availability, confirms the booking, and sends reminders to cut no-shows. Runs on Make.com, one Claude API call per step, with Google Calendar as the booking backend.

## The known problem

Too slow. Around 2.5 minutes per booking, because the scenario accumulated too many modules, routers, and filters during testing. The rebuild target: under 20 seconds, via one Claude API call returning structured JSON, a router with no more than four branches, one stored calendar-availability check, and webhook-triggered execution. No paying client gets onboarded until this is solved.

## Gaps to close in the 2.0 rebuild

**No cancel or reschedule flow.** Right now Lexi can only take a new booking. A client who wants to cancel or move an existing appointment has no way to do that through her, they'd have to fall back to messaging Chante directly, which defeats the point of the split-contact setup. The rebuild needs:

1. Recognize cancel/reschedule intent in the incoming message, not just new-booking intent.
2. Pull up the client's existing booking (by phone number or name match against the calendar/sheet).
3. For reschedule: offer new available times, same flow as a fresh booking from there.
4. For cancel: confirm with the client before removing anything.
5. Update Google Calendar and the tracking sheet automatically either way, no manual cleanup after.

Worth building this into the 2.0 architecture from the start rather than bolting it on after, since it's a second conversation branch off the same router.


## Membership tracker (built and proven live, 27 Sept)

Chanté's 6 Wash & Blowdry membership (R650, 3-month expiry from payment date) is live on scenario 5043763. Booking a wash deducts one, cancelling refunds one, BALANCE and RENEW are keyword replies, the calendar event is labelled with the visit number, and basin treatment flags automatically on wash 4 (every 2nd visit). A ProcessedMessages sheet-backed guard keys on WhatsApp's message ID so a duplicate delivery can't double-deduct or double-refund. All confirmed correct live, sheet reset to a clean baseline (Used=2, Remaining=4).

**Still open:** the RENEW/final-wash staff alert (modules 337, 346) is hardcoded to `27714296057`, which is Lexi's own WhatsApp number, not one Chanté actually checks. Needs her real number before the alert reaches anyone.

## Appointment reminders (live for all clients, 27 Sept)

Scenario `Chales - Appointment Reminders` (7617803) runs daily at 17:00, finds tomorrow's bookings on Chanté's calendar, and sends the WhatsApp `appointment_reminder` template. Built 23 Sept, shipped in test mode (only Theo's own number), left that way through the membership work, and switched on for real clients 27 Sept.

## Reusable client template (built, not yet used)

A sanitised copy of Chales' live Lexi scenario, credentials and salon-specific IDs replaced with placeholders, documented step by step in `plans/client-template.md`. Ready for whenever a second paying client signs; the reminders scenario doesn't have its own template version yet (small, 5 modules, quick to do when needed).

## Voice notes (planned)

Voice notes are currently ignored: only text and taps get past the first filter, so a client who sends one gets no reply. Plan to fix that and turn voice notes into bookings: `plans/lexi-voice-notes.md`.

## Chales services (as listed in Lexi's service menu)

Wash and Blowdry · Trim · Precision Cut · Root Touch Up · Full Color · Hair Colour & Highlights · Brazilian & Keratin · Nanoplastia · Botox & Glowtox · Basin Treatment.

**Chanté does not do braids.** Never use braids (or relaxers) as an example for Chales.

## Service shortcut (fix13, 25 Sept)

If a client's first message (typed or voice note) names exactly one service, Lexi skips the service menu. She sends her welcome and the salon rules with "Lovely, a <service>!", then "taps" that service for them, so the normal day list follows. If no service or more than one is named, the usual menu shows. Builder: `scripts/lexi/build_service_shortcut.py`.

## Photo confirmation (fix14, built 25 Sept)

The booking confirmation becomes one WhatsApp message: salon photo on top, service, day and time in bold, the address, and a "Get Directions" button (Google Maps: https://maps.app.goo.gl/Stvh3qfxGtiYpoLS9). No Meta template approval is needed, because it's sent while the client is chatting (inside the 24-hour window). If the photo fails, Lexi falls back to the old plain-text confirmation, and the sheet steps still run. Builder: `scripts/lexi/build_photo_confirmation.py`. Stacks on fix13.
Photo: https://raw.githubusercontent.com/oldish1/chales-assets/main/chales-salon.jpg (public repo oldish1/chales-assets, holds only public images).

## Spoken or typed day and time (fix15, 25 Sept)

While Lexi is waiting on the day list or the time list, a voice note or typed reply is matched to a day ("Saturday", "saterdag", "tomorrow", "the 30th") or a time ("10 o'clock", "half past two", "half tien", "2pm", "14:00", "noon") and tapped for the client. Only days on the list and real slots count (weekdays hourly 8am to 4pm, Saturdays every half hour 8am to 4:30pm). Anything else goes to Lexi's AI conversation as before. Builder: `scripts/lexi/build_spoken_taps.py`, tests: `scripts/lexi/test_spoken_taps.js` (23 cases). Stacks on fix14.

## Lesson: Make router fallbacks are stored by position (25 Sept)

A Make router's fallback route ("else" in the blueprint) is saved as a route **index**, not a route. Fix15 first inserted a new route at position 0 of router 40, which silently made the name-capture route the fallback, so typed and spoken names stopped confirming (the AI replied instead). Fixed in fix15b: new routes are appended at the end, and the builders assert every router's fallback still points at the same route as before. **Rule for any future edit: never insert routes before existing ones; append, then check "else".**

Also since fix15b: names must be typed. A voice note at the name step gets "Please type your full name so I get the spelling right". Voice-to-text heard "Theo" as "Siyou".

## Decision (25 Sept, late): Lexi frozen at fix14

Theo and Claude agreed: Lexi runs fix14 (voice notes understood, service shortcut, photo confirmation) and gets **no more features**. Fix15/15b (spoken day and time) is shelved: taps already do that well and it caused the name-step bug. Voice replies inside WhatsApp are dropped. The next voice work is a separate product, a real-time voice receptionist (Vapi or Retell) built next to Lexi on the demo number, sharing her calendar and sheet. A clean-up pass to shrink the scenario comes after the first paying client.
