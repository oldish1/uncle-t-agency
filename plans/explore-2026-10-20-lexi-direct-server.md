# Explore: Lexi Direct Server (Lexi 2.0 off Make.com)

**Created:** 2026-10-20
**Status:** Explored
**Origin:** Replace Lexi's Make.com chain with our own server on Meta's WhatsApp Cloud API (no Kapso), so she replies in under 20 seconds, we have full control, and adding a salon is easy.

---

## Vision

One small server we own runs the WhatsApp booking conversation for every salon. It does what Lexi does today, but plain code handles the menus and the calendar, and Claude is only called when a client types something free-form. It proves itself on the Uncle T Demo number first. Chales and later clients move over only once it has beaten Make on speed and on a run of real test bookings.

## Problem Statement

Lexi takes about 2.5 minutes per booking on Make.com, because the scenario grew too many modules, routers and filters. `context/lexi.md` sets the rule: no paying client is onboarded until she replies in under 20 seconds. Make's blueprint quirks (router fallbacks stored by position, a ~230K-character scenario that couldn't be pushed through the API) also make every change slow and risky. Kapso (a WhatsApp API middleman, seen on Instagram) was researched and rejected: it adds a monthly fee per client number and a dependency we don't control.

## Proposed Solution

### What It Does
A webhook server on Meta's WhatsApp Cloud API that books, cancels and reschedules appointments for any number of salons, each defined by one config file.

### How It Works
1. Meta sends a message. The server answers "received" at once.
2. Duplicate check on the WhatsApp message ID, so one message can never book twice.
3. Lookup of the salon from the phone number ID, then load of its config file.
4. Tap flow: welcome and rules, service, day, time, typed name, confirm. If the first message names exactly one service, the service menu is skipped.
5. Day and time lists come from the live Google Calendar. Chales' rules: weekdays hourly 8am to 4pm, Saturdays every half hour 8am to 4:30pm.
6. Confirmation is one message: salon photo, bold service, day and time, address and a "Get Directions" button. If the photo fails, plain text still goes out.
7. The server creates the calendar event and writes the tracking sheet row.
8. Cancel and reschedule: find the booking by phone number, confirm before removing, then reuse the day and time lists.
9. Typed free text goes to one Claude call that returns structured JSON (intent, service, day). Code does the rest.
10. A voice note gets a polite "please type or tap" until voice is added.

Expected speed (estimates, to be proven in testing): taps 2 to 4 seconds, free text 3 to 6.

### What It Produces
- WhatsApp replies and confirmations.
- A Google Calendar event and a tracking sheet row per booking.
- A message log, so slow or wrong replies can be traced.

## Scope

### Minimum Viable Version
Phase 1 on the Uncle T Demo number only (+27 76 492 4196): booking, cancel and reschedule, one config file per salon, under 20 seconds, spending cap set. Chales is untouched and keeps running on Make.

### Full Vision
Everything Lexi does today on one server (voice notes, membership tracker, reminders), Chales and the next clients on it, an owner screen to see bookings, Make out of the booking path.

### Components
| # | Piece | Effort |
|---|---|---|
| 1 | Core server: Meta handshake, signature check, duplicate guard, salon lookup, config loader | Small |
| 2 | Conversation memory: small database file on a Railway volume | Small |
| 3 | Tap flow: welcome, service, day, time, name, confirm, service shortcut | Medium |
| 4 | Calendar and sheet via a Google service account | Medium |
| 5 | Free-text with one Claude call returning JSON | Small |
| 6 | Cancel and reschedule | Medium |
| 7 | Photo confirmation with directions button and fallback | Small |
| 8 | Voice-note holding reply | Small |
| 9 | Test kit: fake-message simulator and timing check | Medium |
| 10 | Deploy to Railway, point the demo number, speed test, spending cap | Small |
| 11 | Chales cut-over: side-by-side run, then switch | Small to Medium |
| 12 | Docs and an "add a salon" runbook | Small |

### Phasing
- **Phase 1 (1 to 10):** demo number only. This is the "works 2000%" stage: a long run of real bookings on the demo number, timed.
- **Phase 2 (11):** Chales moves over only after Phase 1 beats Make on speed and holds up on real test bookings. Side by side first, cut over second.
- **Phase 3:** voice notes, membership tracker, reminders, owner screen, second client.

### Out of Scope
Voice calls and the Retell receptionist, the membership tracker, reminders, payments and deposits (all stay on Make or wait), and any change to Chales' live Make scenarios during Phase 1.

## Technical Considerations

- **Host:** Railway Hobby, $5/month (about R90) including $5 of usage, 30-day free trial with $5 credit first. One server serves every salon, so the cost doesn't grow per client. Pricing checked 2026-10-20; usage is billed by actual use, so set a spending cap. Fly.io is about $2 to $4/month with no free tier. Render is $7/month always-on, and its free tier sleeps.
- **Compared with Kapso:** Free is 2,000 messages and 1 number. Pro is $25/month for 3 numbers, then $10 per extra. Meta's fees are charged either way. Rejected for cost growth and dependency.
- **Compared with n8n:** same drag-and-drop chain style as Make. Self-hostable, but the step chain is what made Lexi slow. Fine later if someone non-technical needs to edit boxes.
- **Conversation memory:** small database file on a Railway volume (about $0.15/GB/month). In memory loses the client's place on restart. A Google Sheet adds a slow call per message.
- **Calendar access:** Google service account that the salon owner shares the calendar with once. No personal login stored.
- **Duplicate guard:** keyed on the WhatsApp message ID, like the ProcessedMessages sheet on Make.
- **Router rule carried over:** Make's fallback-by-position bug does not exist in code, but the same conversation rules are tested explicitly.
- **Per-salon config:** services, hours, calendar ID, sheet ID, phone number ID, salon rules, address, photo link, staff alert number.
- **Secrets:** all keys live in Railway environment variables, never in chat or git.
- **Risk:** the real Meta handshake can only be tested with Theo's Meta app and Railway live. Logic gets tested with fake messages first.
- **Unknowns:** actual reply speed until measured on a real number; the exact Railway monthly usage.

## Integration Type

**Classification:** Script/app. It is a standing server, not a skill or a command.
**Reasoning:** it runs on its own host and needs code, tests and deployment, like `apps/tt-engineering/`.
**Location:** `apps/lexi-server/`, with salon config files in `apps/lexi-server/salons/`.
**Trigger keywords:** n/a. An "add a salon" command can follow once it works.

## Connections

- `context/lexi.md`: the current rules, gaps and the under-20-seconds rule this serves.
- `context/tech-stack.md`: gains Railway and the service account once built.
- `plans/client-template.md`: the Make-based onboarding this replaces for new salons.
- `plans/2026-10-14-personal-assistant-agent.md`: same webhook pattern, but fully separate (own number, Meta app, host, keys). Nothing shared with this server.
- `plans/lexi-voice-notes.md` and `plans/2026-09-27-lexi-voice-receptionist.md`: Phase 3 and separate product.

## Next Steps

1. Theo: create the Railway account (free trial first), add the keys as environment variables, add a Claude API key with a spend cap.
2. Theo: add the new webhook in Meta for the Uncle T Demo number, and set up the Google service account (Claude can walk through it).
3. `/create-plan` on this doc to turn Phase 1 into a build plan.
4. `/implement` Phase 1, then `/test` on the demo number against Make's timing.
5. Only after Phase 1 is proven: Chales side by side, then cut over.

## Discovery Notes

- **Decisions (Theo, 2026-10-20):** stay direct on Meta Cloud API, no Kapso; Railway for hosting; demo number first, Chales migrates once it works; Claude does all the building; first version is booking, cancel and reschedule only; one config file per salon; small database file for conversation memory; Google service account for calendar access.
- **Tap-first:** clients book by tapping buttons and lists, typing is a fallback. Taps are why most replies should take a few seconds.
- **Honest note on "2000%":** proof on the demo number means many real, timed test bookings across every path (new booking, shortcut, cancel, reschedule, duplicate delivery, photo failure), not one lucky run.
- **Alternatives considered:** Kapso (rejected), n8n (stays an option for later non-technical editing), Netlify functions (cold starts and time limits make the 20-second promise harder), Fly.io and Render (similar cost, more setup or sleeping on free).
- **Unconfirmed:** Luna (Nita's) is not described anywhere in this workspace. See the session notes before assuming it fits.
