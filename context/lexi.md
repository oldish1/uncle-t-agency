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
