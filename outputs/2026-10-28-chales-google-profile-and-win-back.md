# CHALES on Google: profile, reviews and win-back plan

> For Theo and Chanté. Findings first, then the steps in the order to do them, then copy-paste messages. Scan run 28 Oct 2026 with Apify's Google Maps scraper. Method borrowed from the claude-seo repo (`seo-local` skill, Whitespark 2026 ranking factors).

## What the scan found

Searching "Chales Hair Boutique Bellville" on Google Maps returns three other salons and nothing for Chanté. The "Get Directions" link Lexi sends (maps.app.goo.gl/Stvh3qfxGtiYpoLS9) opens a pin at **46 Alexandra St, Oakdale** with no business name, no rating, no photos, no category. That's a street address, not a business listing.

So either Chanté has no Google Business Profile, or she has one that was never verified and Google isn't showing it. Both need the same first step: log into business.google.com with her Google account and see what's there. Nothing below works until that's settled.

Salons around her that she's competing with on the map:

| Salon | Reviews | Rating |
|---|---|---|
| Crown and Glory (Welgemoed) | 141 | 4.9 |
| Opalé Beauty Studio (Oakglen) | 128 | 4.4 |
| Lynne Hair Beauty (Bloemhof) | 111 | 4.7 |
| Mish Beauty Bar (Belair) | 103 | 4.7 |
| The Style Bay (Bellair) | 73 | 4.5 |
| Erica's Hair Boutique (Blomtuin) | 65 | 4.6 |
| Irenes Salon (Oakdale, same suburb) | 29 | 4.7 |
| Salon Nina (Oakdale, same suburb) | 16 | 4.9 |
| Irene's Unisex Hair Boutique (Oakdale) | 5 | 5.0 |
| Timeless Hair by Colette (Oakdale) | 2 | 3.0 |

Good news: in Oakdale itself nobody is far ahead. Irenes Salon has 29 reviews. Getting Chanté to 30 reviews at 4.8 or better puts her at the top of her own suburb. Page one for "hair salon Oakdale" is realistic. "Hair salon Bellville" is a bigger fight (Naturarose has 110, Crown and Glory 141), that comes second.

## How Google ranks a salon on the map (short version)

Proximity is about half of it and nobody can change that. The rest Chanté controls: the right category, a complete profile, review count and how recent the reviews are, and her website saying the same name, address and phone as the profile. Review recency matters a lot. A salon that gets two reviews a week beats one that got 40 last year and nothing since.

## Step 1: Claim and verify the profile (Chanté, 20 minutes, today)

1. On her phone, open Google Maps, search her name. If a listing exists, tap "Claim this business". If not, go to business.google.com and tap "Add your business".
2. Name: **CHALES Hair Boutique**. Exactly that, no keywords stuffed in.
3. Address: 46 Alexandra Street, Oakdale, Bellville, 7530. Tick that customers visit her at this address.
4. Primary category: **Hair salon**. Secondary categories: Hairdresser, Beauty salon, Hair treatment service (add whichever Google offers; pick up to 4).
5. Phone: **081 433 2756** (Chanté's business number) goes on the profile as the main phone. Lexi (071 429 6057) is the booking assistant and goes in the "Appointment link" field as https://wa.me/27714296057. The profile, the website and the schema then all show 081 as the phone, which is what Google checks for consistency. Customers call or WhatsApp Chanté for questions, and tap Book to talk to Lexi. TikTok bio can say "Book: tap link" with the Lexi link and list 081 as the number to call.
6. Website: https://chaleshairboutique.co.za
7. Hours: Tuesday to Saturday, 08:00 to 17:00 (matches the site). Fix if the real hours differ, and make the site match.
8. Verification: Google will offer video, phone, or postcard. Video is fastest: she films the street outside, the salon sign, the inside, her chair and tools, then the shop key or something showing she works there. Takes under a day when it's accepted. Don't use a postcard unless video fails, it takes a week and gets lost.

## Step 2: Fill every section (Chanté and Theo, 1 hour)

- **Description** (750 characters max, paste this, edit if anything's wrong):
  > Hair salon in Oakdale, Bellville. Chanté and her team do colour, highlights, Brazilian blowouts, keratin, nanoplastia, Botox and Glowtox treatments, blow-dries and styling. Book on WhatsApp any time and get a reply straight away. Membership available: R650 for 6 wash and blow-dries with a flat iron finish. Open Tuesday to Saturday, 08:00 to 17:00.
- **Services**: add each with a price from her real price list. Hair Colour and Highlights, Full Colour, Brazilian and Keratin, Nanoplastia, Botox and Glowtox, Wash and Blow-dry, Membership.
- **Booking link**: https://wa.me/27714296057 (opens a chat with Lexi). Put it in the "Appointment link" field.
- **Photos**: at least 15 real ones. Her work (before and after), the inside, the sign, the outside so people can find the door, and her at work. Phone photos are fine. Add 2 or 3 new ones every week, it counts as activity.
- **Posts**: one a week using her TikTok offers (membership, specials). Same copy, same photo.
- **Attributes**: tick everything that's true (wheelchair access, accepts card, appointment required, women-owned if she wants).

## Step 3: Fix the map pin (Theo, 10 minutes)

Once the profile is verified, open it, tap Share, and copy the short link. Replace the old pin link in Lexi's booking confirmation (see `context/lexi.md`, "Get Directions" button) so every booking confirmation points at the real listing. Also use this link as the review link below.

## Review shield: what to do and what not to

If you mean a tool that sends happy clients to Google and unhappy ones to a private form, don't build that. Google calls it review gating, it breaks their policy, and they can delete the reviews or suspend the profile. That would hurt Chanté more than a bad review does.

The safe version gets most of the benefit:
- Send the same review request to every client, same link, no filtering.
- Add a line under it for everyone: "If anything wasn't right, tell me straight on WhatsApp so I can fix it." That's open to everyone and doesn't steer anyone away from Google.
- Reply to every review within a day or two. For a bad one: thank them, apologise once, offer to fix it offline, no arguing.
- Report fake or abusive reviews to Google from the profile for removal.
- Later, Lexi can send the request automatically after each appointment. Same message for everyone, so it stays within the rules.

If you meant a different product, tell me what it's called and I'll look at it.

## Step 4: Get the review link and start collecting

In the profile, tap "Get more reviews" and copy the link (looks like g.page/r/XXXX/review). That's the link every message below uses.

Rules that keep her safe (Google removes reviews and can suspend the profile for these):
- Ask **every** client for a review. Never ask only the happy ones and send unhappy ones somewhere else.
- No discounts, freebies or entries into a draw in return for a review.
- Reply to every review within a day or two, good or bad. Short and warm.

**Review request** (send within a few hours of the appointment, same day):
> Hi [Name], thanks for coming in today, it was lovely having you. If you've got a minute, a quick Google review helps my little salon a lot: [review link]. Thank you! Chanté, CHALES Hair Boutique

Target: **4 to 5 new reviews a week** for the first six weeks. At her usual client volume that's about one in three clients saying yes, which is normal when you ask in person and then message.

In person works better than any message. Chanté shows the QR code on her phone at the till. Print the review link as a QR code on a card for the mirror (free QR generators work, or ask me).

## Step 5: Win back the old clients

She was busy before, so there's a real list. Pull it from her WhatsApp chats and the booking sheet Lexi has been writing since September. Anyone who booked in the last 18 months and hasn't been in for 8 weeks or more.

Three messages, sent a few days apart. **Don't send all of them to everyone.** If someone replies or books, they stop getting the rest. Send them one by one from Chanté's own WhatsApp (not a mass broadcast), each with the person's name in.

**Message 1, personal check-in:**
> Hi [Name], it's Chanté from CHALES. I was thinking of you the other day and realised it's been a while. Everything okay? I'd love to know what made you stop coming, honest feedback helps me get better. And if your hair's due, I've got space this week.

**Message 2, the offer, 3 or 4 days later if no reply:**
> Hi [Name], Chanté again. I'm opening a few spots this week and I'd love to see you. Our membership is R650 for 6 wash and blow-dries with a flat iron finish, and your first one can be booked right now: wa.me/27714296057 (that's our booking assistant, replies straight away, any time).

**Message 3, last one, a week later:**
> Hi [Name], last message from me, I promise. If something I did didn't work for you, I'd really like to hear it, you can tell me straight. If you're just busy, my door's open any time. Chanté x

Anyone who says "stop" or doesn't want messages: remove them from the list straight away (POPIA). These are people who've been in her chair, so one to three personal messages is fine, but don't keep going after a no.

The replies to Message 1 are gold. If three people say "your prices went up" or "I couldn't get a slot", that tells Chanté what to fix. Write them down and tell me, I'll fold them into the plan.

After they've been back and had a good visit, they get the review request like everyone else.

## Step 6: Website tidy-up so Google trusts it (Theo, 30 minutes)

The site's schema already has name, address, hours and phone, which is good. Fix these:
- The site's phone is already 081 433 2756. Keep it, and keep the booking buttons pointing at Lexi. Match this on the profile and every listing.
- Add `geo` coordinates and `aggregateRating` once she has 10 or more reviews.
- Add a Google Maps embed of the real listing to the contact section.
- Title tag and H1 already say Bellville. Add "Oakdale" to the H1, since Oakdale is where she's competing hardest.
- The `sameAs` links point to a Facebook page and an Instagram that are dead or unverified. Keep the TikTok, point the others at real pages or remove them.

## Step 7: Also claim Apple Maps and Bing Places

30 minutes each, free. Bing Places feeds ChatGPT and Copilot answers for "good hair salon in Bellville". Apple Business Connect covers iPhone users. Same name, address, phone as the Google profile.

## Timeline and what to expect

| When | What happens |
|---|---|
| Today | Profile claimed, verification started |
| Within a week | Verified, 15 photos, services and booking link added, first win-back messages out |
| 2 to 4 weeks | 10+ reviews, "Chales Hair Boutique" search shows her on the map with a rating |
| 6 to 8 weeks | 25 to 30 reviews, appearing for "hair salon Oakdale" and nearby searches |
| 3 months | Competing for "hair salon Bellville", with a steady stream of reviews |

Nobody can promise page one by a date. Google decides, and proximity matters. But the reviews and a complete profile are the two things she can control, and her competitors in Oakdale are weak.

## Selling this to the next client

This is the product you've been calling "review requests" and "reactivation campaigns" in `context/offer.md`. Once it works for Chanté, you have a real before and after (reviews, map ranking, bookings through Lexi) to show Zanzibar, Sistergirl and the others. The automated version, Lexi sending the review request after each appointment, is a small build on the reminders scenario. Not yet, prove it by hand first.

## Next steps

1. Chanté logs in to business.google.com and tells Theo what she sees (no listing, unverified listing, or verified and showing).
2. Theo: after verification, swap the pin link in Lexi.
3. Chanté sends the win-back messages to her top 10 old clients first, as a test.
4. Re-run the Maps scrape in 2 weeks to check whether she's showing up. The scan took one command, so it's cheap to repeat.
