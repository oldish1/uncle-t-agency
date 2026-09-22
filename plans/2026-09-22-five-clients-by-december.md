# Plan: 5 paying clients by December

**Status:** Ready
**Owner:** Theo. Built with Claude, 22 September 2026.
**Goal:** 5 salons paying R1,000 a month on the Founding 10 offer by 31 December 2026. That's R5,000 a month recurring going into 2027.

## The one rule

Every day, something moves a salon one step closer to paying. Research, polish and new ideas only count if they do that. Everything else goes in `context/ideas.md`.

## The funnel (the maths behind 5)

| Step | Rate (estimate) | Needed for 5 clients |
|---|---|---|
| First WhatsApp sent (one message, asks "can I send the 90-second video?") | 20% say yes | about 210 messages |
| Video watched, they reply | 30% agree to a visit | about 42 yeses |
| 15-minute visit with a live demo on their own phone | 40% sign | about 13 visits |
| Signed, live in 4 days, pays after 10 bookings | | **5 clients** |

That's about **5 messages a day, weekdays, for 8 weeks**. The five warm leads (Zanzibar, Sistergirl, Reeva, JEM, Jason) skip the first step, so they're worth the most. Contact them first.

These rates are guesses. After the first 50 messages, the Chief of Staff swaps in the real numbers and tells you if the daily target needs to change.

**Timing warning:** December is the busiest month of the year for salons. Nobody wants a new system in the middle of the festive rush. So the real deadline for signing is **the end of November**. December is for going live and collecting.

## The agent team

Four agents. Each has one job. None of them ever messages a salon without you pressing send, except Sales Lexi, who only answers salons that message her first.

| Agent | Job | Status | Where |
|---|---|---|---|
| **The Hunter** (lead finder) | Finds Cape Town salons whose own Google reviews show the pain, scores them, and drafts your first message and your one follow-up | Built. Needs the Google key. | `apps/lead-finder/` |
| **The Chief of Staff** | 06:00 weekdays: checks every client's Lexi, lists today's follow-ups and who said yes, runs the Hunter on Mondays, drafts email replies, and names today's one priority | Built. Needs switching on in the Claude app. | `apps/chief-of-staff/PLAYBOOK.md` |
| **Sales Lexi** | Lives on the Uncle T demo number. A salon that says yes gets the video plus "WhatsApp my assistant to try it yourself". She answers questions about the offer in English or Afrikaans, lets them book a pretend appointment so they feel it work, and books a real 15-minute visit into your Google Calendar. | Not built. It's Lexi with a different price list, so it goes in the Lexi build brief. | `plans/2026-09-22-lexi-2-build-brief.md` |
| **The Closer** | When a salon replies to you with a question or objection, paste or forward their message into a Claude session and get a reply back in your voice, using the objection answers from the research. | Works today, just ask. | Any session |

Sales Lexi is the agent that "speaks to the clients". She's legal and safe because every salon she talks to messaged her first, after saying yes to you. She's also the best demo there is: the salon owner experiences Lexi before you've even arrived.

## Week by week

| Week | Dates | What happens | Done when |
|---|---|---|---|
| 1 | 22 to 28 Sep | Get the Google key and run the Hunter. Switch on the Chief of Staff. Test "keep your own number" on the demo number. Re-contact the 5 warm leads with the Founding 10 offer by voice note. | First lead report in `outputs/leads/`. 5 warm leads contacted. |
| 2 | 29 Sep to 5 Oct | Meta starts charging per reply on 1 Oct, so check Lexi's real costs. Start 5 first messages a day from the Hunter's list. | 25 messages sent. |
| 3 | 6 to 12 Oct | Lexi 2.0 fast (under 20 seconds). Record the demo video the same day. | Video recorded. |
| 4 | 13 to 19 Oct | Send the video to everyone who said yes. First visits. | 3 visits booked. |
| 5 | 20 to 26 Oct | **Client 1 signed** (most likely a warm lead). Live in 4 days. | Client 1 live. |
| 6 to 7 | 27 Oct to 9 Nov | Sales Lexi live on the demo number. Keep up 5 messages a day. Ask client 1 for two introductions. | **Client 2 signed.** |
| 8 to 10 | 10 to 30 Nov | Push hard before the festive rush: "Get set up before December so Lexi handles the Christmas bookings." | **Clients 3, 4 and 5 signed** by 30 Nov. |
| 11 to 14 | 1 to 31 Dec | Go live, fix issues fast, count bookings to 10, send first invoices, collect testimonials. | 5 paying. |

## Your daily 20 minutes (Theo)

1. Read the Chief of Staff's brief at 06:00 (2 minutes).
2. Send 5 first messages from the Hunter's list, one tap each (10 minutes).
3. Send the follow-ups and videos the brief lists (5 minutes).
4. Anything a salon asked: paste it into Claude, get the answer, send it (3 minutes).

Visits and live demos happen after work or on Saturdays. The Chief of Staff shows them in the brief.

## What only you can do (this week)

1. Google Places key: steps in `docs/lead-finder.md`, about 10 minutes. The card needs to work first.
2. Switch on the Chief of Staff: steps at the bottom of `apps/chief-of-staff/PLAYBOOK.md`, about 3 minutes.
3. Send the Lexi build brief to the other Claude session.
4. Voice-note the 5 warm leads.

## How we'll know it's working

The Chief of Staff tracks four numbers every Monday: messages sent, yeses, visits, signed. If the yes rate is under 10% after 50 messages, the first message changes. If visits don't convert, the demo changes. If Lexi isn't fast by 12 October, that's the only thing that matters until it is.
