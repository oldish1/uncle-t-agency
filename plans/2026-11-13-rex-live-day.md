# Tomorrow (13 Nov): Rex live on WhatsApp

One goal for the day: Rex answering Theo on WhatsApp from his own number. Everything else waits until that works. No new videos, no new ideas.

## What decides if Rex can go live tomorrow

An unverified Meta business can hold only 2 WhatsApp numbers. Business verification (needs CIPC papers) takes days and can be rejected, so it must not block Rex. Fastest path: free one of the two slots, put Rex's SIM there, verify later.

Check first (Meta, WhatsApp Manager, Phone numbers): which two numbers are counting today. Likely the Meta test number and the "Uncle T Demo" number +27 76 492 4196. The test number is the one to remove or replace. If both are real, move the demo to later and give Rex the slot.

## Run-sheet

Morning, Theo (about 1 hour)
1. Activate the SIM 063 647 6860 (put it in a phone, make sure it can receive an SMS or call for Meta's code).
2. Meta, WhatsApp Manager: add the SIM as a phone number (or replace the test number). Receive the code on the phone, enter it. Send Claude a screenshot of the number's status, never any token.
3. Meta, System users or the app token screen: generate a new access token, put it straight into the Make connection or settings box, not in chat. This also covers the old "Rexbot token" rotation.
4. Tell Claude "number added".

Then Claude (about 1 hour, Theo can be doing step 5 below)
- Import apps/rex/make-blueprint.json v2, fill the four placeholders in Make, point the Meta webhook at it, add the memory and reminder routes from the Telegram scenario, run the test.
- Theo messages Rex on WhatsApp: "who are you", "remind me in 10 minutes to test", "remember my target is five salons", a search, then asks about the memory.
- Keep Telegram running until WhatsApp passes every test, then switch Telegram off.

Parallel, Theo
5. CIPC: register the company at bizportal.gov.za (company name reservation, then registration). Do it in 30 minutes, no perfection. Check the current fee on the site. When the certificate arrives, send it to Claude and then resubmit Meta verification with the website, email and address matching.
6. Business email on the domain (theo@uncletsautomation.co.za) and decide the address that shows on the site.

## Rest of the to-do, in order, after Rex is live

1. Rotate the two remaining keys (Anthropic "Rex", Apify).
2. Google Search Console (plan in plans/2026-11-10-website-traffic-plan.md).
3. WhatsApp Business profile on the main number.
4. Chante's review link, then QR and poster.
5. Prices: confirm website-only and Lexi plus website.
6. Day-10 outreach follow-ups (Outreach desk).

## Sales agent

Not tomorrow. Build it once Rex is live and CIPC is filed. Design in one line: a Make scenario that reads the Pipeline Sheet every morning, lists who is due for a follow-up and who replied, and sends Rex a message so Rex tells Theo exactly who to message. Theo still sends every message himself.

## Rules for the day

- If something is not on this page, it waits.
- Rex's first job once live: ask Theo each evening "what did you finish today?" and write it to memory.
