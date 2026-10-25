# Game plan: beat Fresha and Booksy, fix pricing risk, get Chales found on Google

**Created:** 2026-10-25  **Status:** Draft, needs Theo's decisions (marked DECIDE)

## What the evidence says

**Chales results (Chante's "Client Data Base" sheet, counted by hand, so approximate):** about 118 booking rows from 10 June to 23 Oct, roughly 100 real bookings once tests, cancellations and reschedules are removed, about 34 different clients, and many weekly regulars (one client has booked about every week since July). Wash and Blow-dry is about two thirds of bookings, the rest is colour, Nanoplastia, Botox and Glowtox, cuts. Customer names stay in the sheet, never in this repo.

**Cost to run, per booking (from Make's log, plus public prices):**
- One booking conversation uses about 60 to 80 Make credits. Make Core is $9 a month for 10,000 credits, so about R1 per booking.
- Claude Sonnet 5.5 is $2 per million input tokens and $10 per million output. An estimated 5 calls of about 3,000 tokens in and 300 out per booking is about R1.
- WhatsApp's own fees: not confirmed for South Africa. Customer-started chats should be free, reminders are templates that cost a few cents each. Check Meta's rate card.
- Working estimate: R100 to R150 per salon per month at about 30 bookings. One Make Core plan carries about 4 salons. The first free month therefore costs about R100 to R150 per salon, not the large number feared.

**Competitors:** all cheaper per month than Lexi (Fresha about R134, Booksy R399 + R89 per extra staff, Setmore free, Booklink R79). Lexi cannot win on price. See `reference/research/2026-10-25-salon-booking-competitors.md`.

**Chales on Google:** her "Get Directions" link points at a bare address pin (46 Alexandra St, Oakdale), with no reviews, no category, no photos, no hours. A Google Maps search for "Chales Hair Boutique" returns nothing. As far as I can see she has no visible Google Business Profile. That is the number one reason she doesn't rank. Bellville leaders have 70 to 156 reviews at 4.3 to 4.9 stars.

## Positioning
Sell results, not software: "Get found. Get booked. Get remembered." A WhatsApp receptionist (Lexi) + Google visibility + reviews + win-back messages, done for the owner. Fresha and Booksy sell a tool the owner must run.

## Pricing (DECIDE)
- Founding five: first 30 days free, then setup R999 (normal R1,499) and R499 a month. Cancel in the first month and she owes nothing. Cost to us about R150 each.
- After the founders, three bundles: Starter R499 a month (Lexi bookings and reminders); Plus R799 (adds review requests, win-back messages, memberships); Grow R1,299 (adds Google profile care, monthly results report, website).
- Websites stay R1,499 once-off.

## Add-ons to build, in order
1. Review requests: after each appointment, a WhatsApp thank-you with her Google review link (no incentives, no screening of unhappy customers, Google bans both).
2. Win-back: message clients not seen in 6 weeks, from the booking sheet.
3. Memberships and prepaid bundles (already built for Chales: 6 washes for R650).
4. Monthly results report on WhatsApp: bookings taken, no-shows avoided, repeat clients. This keeps clients paying.
5. Deposits and payment links (not built).

## Chales on Google (DECIDE who does it: Chante has to verify)
1. Search her salon on Google Maps on her phone. If there is no profile, create one at business.google.com: category Hair salon, address, hours, phone and WhatsApp, services with prices, 10 or more real photos, booking link. Verify it (video or postcard).
2. Reviews: ask her 34 clients, starting with the weekly regulars, through WhatsApp with the direct review link. Target 30 reviews in 30 days, then 60 to 100.
3. Website: show the street address, embed the map, add LocalBusiness markup, and write a page for "hair salon Bellville".
4. Realistic: months, not days, and no guarantee of page one. Profile plus 60 to 100 real reviews puts her in the contest.

## Funding
Not the bottleneck: first five clients cost about R750 in total. If wanted later: SEFA loans (government page lists from R500 up to R3 million), NYDA grants for ages 18 to 35, NEF for larger amounts. Apply after two paying clients.

## Flags
- Three Chales runs on Sunday 25 Oct morning failed with "403 permission denied" when writing a row to a Google Sheet. Check that nothing in live booking is silently failing.
- The Apify token showed up inside an error message. Script fixed (token now in a header). Rotate the token.
