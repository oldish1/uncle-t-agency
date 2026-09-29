# Lexi video outreach: script, message, first batch

> Cold WhatsApp outreach for salons too far to walk into. Send a real screen recording of Lexi replying, not a pitch deck, not a sales script. The video does the convincing, the message just gets it opened.

## What to record (30-40 seconds, on your phone)

Screen-record your own WhatsApp while you message the demo number live. Don't narrate over it, don't edit it, raw and real is the point.

1. Open a chat with the demo number, 076 492 4196.
2. Type "Hi". Show the greeting and service list land instantly, no waiting.
3. Tap a service, tap a day, tap a time. Let the taps show on screen, this is what proves it's fast, not a claim about it.
4. Show the confirmation message land: the salon photo, the day and time in bold, the Get Directions button.
5. Stop there. Under 40 seconds beats a polished 2 minutes, nobody watches a stranger's video that long.

Do this once, keep the file, reuse it for every salon on the list. You don't need a new recording per lead.

## The message (send video + this, nothing else)

Keep it short. No "hope this finds you well," no pitch, no price unless she asks. Updated 29 Sept: tightened all three down to one real question, since a question gets a reply and a statement gets ignored.

**Version C, pure discovery (start here, this is the sharpest one):**
> Hi, quick one, what's the most annoying part of handling bookings on WhatsApp for you? This 30-second clip is something I built that might help 👇

**Version A, straight to it:**
> Hi, noticed [salon name] has no booking link. Built this for a salon in Bellville, replies in seconds so nothing gets missed mid-cut or after hours. Not selling anything, just thought it'd be useful. 👇

**Version B, leads with the pain:**
> Hi, how many bookings do you reckon you've lost to a message you only saw hours later? This fixed that for a salon like yours in Bellville. 👇

Version C works best because it's a question about her, not a statement about you, she has to answer it or ignore it, and either way you learn something real about her actual frustration for the follow-up conversation. Split-test if you want, but if you only send one version to start, send C.

**If she replies at all, don't launch into the pitch.** Whatever she names as her frustration, that's your opening for the follow-up, not a script. Let her ask the next question. The walk-in script's pushback answers (`outputs/2026-09-27-lexi-walkin-pitch.md`) cover price, setup, and "what if it gets something wrong" the same way here.

## First batch to send (15 real mobile numbers, no website, sorted by reviews)

Pulled from `outputs/leads/2026-09-27-hair-salon-all.csv`, filtered to mobile numbers only (landlines can't get WhatsApp, more on that below).

| Salon | Number | Reviews |
|---|---|---|
| Avyary Beauty Salon Bellville | 082 764 5803 | 189, 4.6★ |
| Hair Republic Ct | 072 851 5278 | 72, 4.9★ |
| REEVA Hair & Beauty Salon | 084 375 9214 | 61, 5★ (already a warm lead) |
| Ravaina Rain Hair Studio | 083 650 4578 | 52, 5★ |
| Tanganyika Hair Salon | 068 410 9871 | 49, 4.9★ |
| LAVISH A (Hair & Beauty Studio) | 067 647 8964 | 48, 3.9★ |
| Excellence Beauty Studio | 065 994 2117 | 41, 4.9★ |
| The Lab Hair and Beauty Boutique | 073 681 3784 | 35, 4.9★ |
| Naz Unisex Hairsalon | 071 035 4864 | 32, 4.9★ |
| Kings Pride hair studio | 078 328 4637 | 32, 4.8★ |
| The RITZ Hair Design | 082 623 8588 | 31, 4.9★ |
| LOOK ITS ME HAIR DESIGN | 081 309 8337 | 29, 4.9★ |
| Denises Place salon/ Tomblack | 065 004 8557 | 28, 4.9★ |
| Mari's Hair Studio | 073 914 2451 | 25, 5★ |
| 5Star Hair and Beauty | 081 534 1165 | 21, 5★ |

REEVA's already in your warm-lead pipeline, worth sending the video there too since it's a stronger nudge than a text-only follow-up.

## One catch worth knowing

Of the 54 no-website salons in last night's scrape, only 34 have a real mobile number, the rest listed landlines (021 numbers) on Google, dead ends for WhatsApp. That's the full mobile list this batch of 15 is drawn from, the other 19 are there if this first round gets good replies.

## Send from your own number, not Lexi's

Send these from your personal WhatsApp, not through the Business Platform number. A cold first message to someone who hasn't messaged you needs to be a real person reaching out, and Meta's rules on business-initiated messages to non-opted-in numbers don't apply to a normal 1-to-1 chat from your own phone.

## Out-of-town expansion (29 Sept, blocked)

Plan: 10 leads each from Langebaan, Caledon, Paarl, Worcester, Ceres, and Somerset West, same video-first approach, since it works the same whether you're standing in front of someone or not. If 3+ bite, sell them the website too, same offer already covers it.

Suggested order: send Version C to the 15-number Cape Town batch above first, since it's cheap and fast to learn what actually gets replies before spending Apify credits on 60 more cold numbers in towns you can't easily follow up in person.

**Blocked for now:** Apify rejected the token again this session (`user-or-token-not-found`), the same error as before, even though it should have been saved correctly in the environment box. Needs Theo to check the saved value or generate a fresh token. Will pull all six towns the moment it's working, config just needs the suburb list extended in `scripts/lead_scraper_verticals.json`.
