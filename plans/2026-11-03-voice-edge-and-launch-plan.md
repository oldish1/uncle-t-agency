# Plan: Voice as the edge, the tiers, the demo and the noise

Date: 3 Nov 2026. Status: draft for Theo. Builds on `plans/2026-09-27-lexi-voice-receptionist.md` (the build steps) and `reference/research/2026-11-03-voice-market-and-costs.md` (the numbers).

> Update, same day: Theo's idea of two-way voice note conversations on WhatsApp (Lexi Talk) is cheaper and faster than live calls and looks like a real gap. It becomes the first voice product, with live calls as the later rung. Details in `plans/2026-11-03-lexi-talk-voice-note-conversations.md`.

## The verdict in one paragraph
Voice alone will not make us stand out, because eight or more local providers sell it from R849 to R2,000 a month and some give away a demo line. Voice combined with three other things can. One: one assistant that handles WhatsApp typing, WhatsApp voice notes and live calls on the client's own number. Two: a price that sits under the others (Lexi plus Voice at R1,298 a month against about R2,000). Three: a demo anyone can try in 30 seconds. Four: pointed at the businesses where a missed call costs the most, which is trades and clinics more than hair salons. Voice becomes our edge if we build the demo first, prove the cost and accent quality in a short test, and aim it at the right buyer.

## Step 1: The 5-day proof test (cost under R300)
Goal: know, with real numbers, whether live voice works for Cape Town callers before we put it on a price list.
- Day 1: create the Retell account and claim the free $10. Build the agent from the Chales script (greeting, service, day, time, name, confirm). Use ElevenLabs as the second voice to compare.
- Day 2: connect it to the existing booking steps on a copy pointed at the demo calendar. Use a browser call first (no phone number needed).
- Day 3: Theo and 3 other people call it 15 times in English, Afrikaans and mixed, using real service names and place names. Log each one in `reference/research/2026-11-03-voice-test-log.md`.
- Day 4: try the WhatsApp calling route on the demo number if Meta allows it. If not, buy a SA number and use call divert.
- Day 5: decide.

Go if: at least 12 of 15 calls end in a correct booking, the pause after the caller stops is under about 1.5 seconds most of the time, Afrikaans names are mostly understood, and the cost per booking call is under R12.
No-go or fix: below that, we sell voice notes only and revisit when the platforms improve. Nothing is lost, because voice notes already work.

## Step 2: The demo (the number one priority)
People do not know us and are cautious. The demo has to remove doubt in under a minute. Build three layers, in this order:
1. **A 60 second video, today or tomorrow.** Screen-record the real Chales flow: a voice note in Afrikaans, Lexi books it, the confirmation arrives with the photo. This already works (verified 25 Sept, fix14). No new build.
2. **The demo WhatsApp line.** "Send a voice note to this number and see Lexi reply." Use the demo number (076 492 4196) once its webhook is working. Every demo message gives us a phone number to follow up, with a clear note at the start that it is a demo.
3. **"Talk to Lexi" button on the website.** A browser call to the voice agent, two minutes maximum, with a daily spend cap. At R3 to R4 a minute, 100 demo calls cost about R600 to R800. This is the hook no competitor in the salon space has on its page.

Demo script for the owner: "Send a voice note asking for a Saturday booking. Or press the button and talk to it."

## Step 3: The tiers on the website (next week)
| Tier | What it does | Price (draft) |
|---|---|---|
| Lexi | WhatsApp booking, reminders, cancel and reschedule, voice notes in English and Afrikaans | R1,499 once-off + R499/m |
| Lexi Talk | Lexi replies by voice note, two-way voice conversation on WhatsApp, tap or talk. See `2026-11-03-lexi-talk-voice-note-conversations.md` | + about R299/m (draft) |
| Lexi Call | Everything in Lexi plus Lexi answers live calls. 100 minutes included, then R6 a minute | + R799/m, setup R1,500 |
| Lexi Trade (coming, to validate) | Voice note from the job site becomes a quote PDF. Missed calls answered and the job logged to WhatsApp | to be priced after interviews |

Rules for the page, per the workspace's website skill: Next.js, Tailwind, Framer Motion, light background and dark text. Lead with the problem, not "AI". Put the demo button above the fold. Show the cost of a missed call in rand with a small calculator (jobs missed per week times job value). Keep a clear risk-reversal line (Step 5).

## Step 4: Who to sell voice to
- **Salons:** sell Lexi with voice notes. Offer Lexi Voice as an upgrade for salons that say they miss calls.
- **Trades and clinics:** the best fit for Voice. They get the higher-ticket message set in `outputs/discovery/2026-11-02-higher-ticket-outreach.md`.
- Check each interview against the scorecard (rand per lost slot, calls missed, who answers the phone). Whichever group scores highest becomes the main target.

## Step 5: Getting past "they are not giving their money away"
Ideas, ranked by how much they cut risk for the owner. Theo decides which.
1. **Founding client deal.** Setup waived or halved, R299 a month for the first 3 months, in exchange for a testimonial and a number we can publish (calls answered, bookings made).
2. **Results guarantee.** "If Lexi does not book at least 10 appointments in your first 30 days, you do not pay month two." Only offer it once the cost test is done and Chales numbers show how many bookings Lexi makes.
3. **7 day pilot on their own number**, with the demo line first.
4. **Proof from Chales.** Pull real numbers from the sheet: messages answered, bookings made, after-hours bookings, cancels saved. Chanté on camera for 30 seconds.
5. **In person set-up and a human to call.** This is what the cheap tools cannot offer. Say it plainly.

## Step 6: Getting loud (4 weeks, a rhythm Theo can keep)
Rule: one piece of content a day, 10 to 15 minutes to make, recorded on the phone.
- **Formats (rotate):** (a) the demo in 30 seconds, (b) "what a missed call costs a plumber" in rand, (c) Chanté or a client saying one real thing, (d) a voice note turning into a booking or a quote, (e) one thing learned from a conversation this week, (f) behind the scenes of building it.
- **Where:** TikTok and Facebook Reels first, since both worked for Chales. Share to WhatsApp status and local Facebook groups for salons and trades. Instagram second.
- **Every post ends with the same call to action:** "Send a voice note to this number and see for yourself."
- **Week 1:** record the 60 second demo and 5 short clips. **Week 2:** post daily, answer every comment and DM within the hour. **Week 3:** one video per business type (salon, plumber, clinic, groomer). **Week 4:** review what got replies, drop the rest, double the best.
- **Track:** demo line messages per week, calls to the website button, replies to outreach, conversations booked. If a format gets zero replies in two weeks, drop it.
- **Pair with the outreach:** every conversation Theo has gets a short follow-up clip or the demo link.

## Step 7: Build order
1. Demo video (no build) and the Chales numbers.
2. 5-day voice proof test.
3. Website with the demo button and tiers.
4. Voice notes marketed as a headline feature of Lexi now (already built).
5. Lexi Voice live for the first client that asks for it, on the demo number first.
6. Lexi Trade only after 5 or more trades interviews confirm they would pay.

## What we decide after the test
- Final voice add-on price from real cost per call.
- Whether the guarantee is safe to offer.
- Whether Lexi Trade is worth building.

## Open questions for Theo
1. Is the demo number's Meta verification finished, so we can turn calling on there?
2. Does Theo have the voice-note-to-PDF notes somewhere else (a different file or a video)? If so, send it so we can match what you had in mind.
3. Which offer feels right to Theo: the founding client deal, the results guarantee, or both?
