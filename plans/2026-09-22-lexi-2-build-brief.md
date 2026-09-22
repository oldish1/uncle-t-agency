# Lexi 2.0 build brief (for the Lexi build session)

**Status:** Ready
**From:** the planning session, 22 September 2026. **For:** the Claude session rebuilding Lexi.
**Why this exists:** Theo has locked an offer and a goal. This brief says what Lexi has to do to support them, in what order, and what "done" means for each piece. Keep going with the speed work first. Everything here comes after, or alongside it where it's cheap.

## Read these first

- `context/lexi.md`: what Lexi is, the speed problem, the cancel/reschedule spec
- `context/offer.md`: the Founding 10 offer (R1,000 a month, R0 setup, pay after 10 bookings, month-free if she double-books)
- `plans/2026-09-22-five-clients-by-december.md`: the goal and timeline this build serves
- `outputs/research/2026-09-22-booking-competitors.md`, section 4: the ranked copy list
- `outputs/research/2026-09-22-solo-salon-pains-and-offer.md`, sections 4 and 7: costs per client and the onboarding flow

## The goal this build serves

5 paying salons by 31 December, signed by end of November. Client 1 goes live around 20 to 26 October. So everything in **Stage 1** has to be solid by about **12 October**, the date the demo video gets recorded.

## Don't break

- CHALES Hair Boutique is live on Make scenario **5043763**. It's the proof every sale depends on. Build and test on **7288450 (Lexi 2.0 TEST)** and switch CHALES over only once 2.0 passes every test below.
- Money is always in Rand.
- Lexi introduces herself as the salon's booking assistant. She never claims to be a person.
- Lexi only sends messages to people who messaged the salon first, or reminders for bookings they made. No broadcasts yet.

## Stage 1: must have before client 1 (target 12 October)

| # | Feature | Done means |
|---|---|---|
| 1 | **Under 20 seconds per reply** | 20 test messages in a row, every reply under 20 seconds from the client pressing send. Record the times in the test log. |
| 2 | **Cancel and reschedule by chat** | Spec in `context/lexi.md`. "Can I move Saturday to Sunday?" and "I need to cancel" both work, confirm before changing anything, and update the calendar and sheet. |
| 3 | **Day-before reminder with Confirm / Reschedule / Cancel buttons** | A WhatsApp template with three quick-reply buttons. Reschedule and Cancel feed straight into #2. Confirm marks the booking confirmed in the sheet. |
| 4 | **Replies in the client's language** | A client who writes in Afrikaans gets Afrikaans, a client who writes in English gets English, a mix gets whichever they mostly used. One instruction in the prompt, plus 5 Afrikaans test chats. |
| 5 | **Hand-off to the owner** | For anything outside the price list (custom colour, a complaint, a price she doesn't have), Lexi says the owner will reply and sends the owner an alert on their personal WhatsApp with the client's name and message. She never guesses a price. |
| 6 | **Booking counter** | Each client's sheet counts bookings Lexi made, so Theo can prove the 10 that trigger the first bill. A simple row per booking with a "made by Lexi" flag. |

## Stage 2: onboarding a new salon in 4 days (target 20 October)

The offer promises "live in 4 days". At 5 to 10 clients, copying the whole Make scenario per salon will become impossible to maintain.

- **One Lexi, many salons.** Build 2.0 so one scenario serves every salon, reading each salon's details from a **client settings sheet** matched by the WhatsApp phone number ID: name, services and prices, durations, hours, address, deposit rules, owner's alert number, language, calendar ID, "never quote" list. A new salon means one new row plus a calendar, not a new scenario. If that's too big a change before 12 October, do it straight after client 1.
- **Onboarding checklist.** A one-page list in `docs/` of every step from "salon said yes" to "live", including the Meta number setup. Theo should be able to follow it with Claude in one evening.
- **Check "keep your own number" for +27 numbers.** Meta's coexistence feature (the salon keeps using the WhatsApp Business app on the same number Lexi answers) may or may not be available for South African numbers yet. Test it on the demo number and write down the answer in `context/lexi.md`. It decides what Theo promises in the pitch.

## Stage 3: Sales Lexi on the Uncle T demo number (target 27 October)

This is the agent that talks to prospects. It's Lexi with a different settings row.

- **Who she talks to:** only salon owners who message the Uncle T demo number after Theo sends them the demo video ("WhatsApp my assistant and try it yourself").
- **What she does:**
  - Explains the Founding 10 offer (from `context/offer.md`) and answers the objections in section 8 of the offer research.
  - Lets the owner make a pretend booking at "Demo Salon" so they feel how fast it is.
  - Books a real 15-minute visit with Theo into Theo's Google Calendar, after work or on Saturdays only.
  - Alerts Theo on WhatsApp when a visit is booked or a question needs him.
- **What she never does:** promise anything that isn't in the offer, discount, or message anyone who didn't message her first.

## Stage 4: next, after client 1 (November)

In order, from the research copy list: deposits by Yoco or PayFast payment link (optional per service, braids yes, trims no); a morning WhatsApp summary to the owner ("today: 6 bookings, 1 unconfirmed"); a Google review request after a confirmed visit; a rebooking nudge per service (opt-in only); several stylists each with their own calendar.

## Costs to design for

- **Meta charges per reply from 1 October 2026**, about 12c each, with 1,000 free replies a month per number (per the research, not confirmed on Meta's own page, so check it). A solo salon stays under 1,000; a busy one goes over.
- **Claude API cost per reply** is the biggest running cost for busy salons. Use prompt caching for the salon's settings and price list, and a smaller, cheaper model for simple turns ("yes", "10:30 please"). The offer research estimates R210 to R285 a month to run a solo salon and R640 to R940 for a busy 3-chair salon, which is thin at R1,000. Log real costs for CHALES in October so the numbers can be checked.
- **Make.com operations** add up past about 10 clients. Fewer modules per message helps speed and cost at the same time.

## Report back

When each stage is done, write a ledger row, update `context/lexi.md` with what changed, and tell Theo in plain English what now works and what he can demo. Update the Chief of Staff's watch table in `apps/chief-of-staff/PLAYBOOK.md` whenever a new scenario or client goes live.
