# Deep Research: Gaps in existing booking platforms
**Session:** 2026-09-27-salon-booking-pain-competitor-intel | **Date:** 2026-09-27

## Executive Summary

None of the big booking platforms (Fresha, Booksy, Setmore, Calendly, Square Appointments) lets a client book by chatting on the salon's own WhatsApp number. Checked against each vendor's own help pages this week, their "WhatsApp integration" comes in three flavours: a WhatsApp Business away-message that pastes a booking link (Booksy, Setmore), one-way reminder messages you can't customise and pay per send for (Fresha, Setmore), or a button that opens a WhatsApp chat so the owner can type manually (Booksy, April 2026). Calendly needs Zapier or a third party.

The closest threat is **Fresha's AI Concierge** (USD 99.95 per location per month, about R1,750 to R1,850, on top of the USD 19.95 base plan). It answers calls and chat, and books into the Fresha calendar. Right now its chat runs only inside Fresha's own "Client Connect" inbox. A competitor who checked in August 2026 found that Fresha "says more Meta and Instagram messaging integrations are coming" and "does not document WhatsApp as a current AI Concierge channel." Fresha is valued at over $1bn and just raised from KKR, so WhatsApp support should be treated as likely within 6 to 18 months.

Across the reviews, small operators complain about four things again and again:

1. **Fee creep and marketplace commissions.** Fresha went from free to paid in late 2025 and takes 20% (minimum $6) on "new" marketplace clients, even ones the salon brought in itself. Booksy's Boost takes 30% of a first visit, with the same attribution fights.
2. **Support that is slow, scripted or AI-run**, often just when money or bookings are at stake.
3. **Lock-in and data hostage-taking**: client lists that can't be exported, and notes trapped in the platform.
4. **Notifications that break or can't be answered.** Reminders don't arrive, or a client replies to the reminder and nobody sees it.

**The "one thing":** the platforms want the client to leave the chat. They send her to their link, their app, their account or their marketplace, because that's where they earn commission and collect data. Nobody big is building the reverse: **the booking gets done inside the WhatsApp chat the salon already uses, on the owner's own number, for a flat Rand fee, with no marketplace commission, no client app or account, and nothing to migrate.** For a Bellville or Mitchell's Plain salon whose clients already WhatsApp the owner, that isn't a feature request. It describes a product none of the five sells.

Some small international players already sell this (Happoin, Srileo's "Elily", Engrana, and SA-based MyBusinessApp for pet groomers). The gap is real but not empty. Lexi's edge has to be local: done-for-you setup, Rand pricing, and Cape Flats language and trust.

## Key Findings

### Finding 1: No major platform does WhatsApp-native booking. Their "WhatsApp integration" is a link in an away message.

Booksy's own help article, "How to take bookings from WhatsApp," is a guide to switching on the WhatsApp Business **away message** so every chat gets an automatic reply containing the Booksy link. Its sample script: *"Booking your next cut is super easy online, no more waiting for a reply! Check my availability and book now at [Your Booking Link]."*

Setmore's integration page "WhatsApp is open for bookings" says the same thing: put your Booking Page URL in your WhatsApp profile's "About" field and in your away message. Nothing more.

Booksy's April 22, 2026 changelog adds a "WhatsApp shortcut on client cards" that opens a WhatsApp chat so the **owner** can type a message by hand.

Fresha sends reminders by WhatsApp or SMS at USD 0.04 to 0.11 per WhatsApp message after 100 free per month. Its help centre says: *"Text and WhatsApp message can't be customized and use a standard format."*

Setmore's latest Google Play release notes mention "SMS, WhatsApp, and email reminder status," so it also has outbound WhatsApp reminders now.

For Calendly, the listed WhatsApp routes are Zapier, PickyAssist or TimelinesAI. A Calendly Community thread is titled "I can't connect calendly to whatsapp."

A Happoin comparison table sums it up: Booksy has "limited WhatsApp integration," Fresha has "no automated WhatsApp reminders" from your own number, and Square has "no WhatsApp integration."

**Confidence:** High. These are the vendors' own pages, scraped 2026-09-27.
**Based on:** Booksy help centre, Setmore integration page, Booksy changelog, Fresha help centre and pricing page, Zapier and Calendly community pages, Setmore Play Store listing.

### Finding 2: Fresha's AI Concierge is the real competitive threat. It isn't on WhatsApp yet.

Fresha's AI Concierge (USD 99.95 per location per month; 200 call minutes and 500 messages included, then $0.60 per minute and $0.04 per message) *"answers calls and messages, schedule appointments... Available 24/7 and fully synced with your Fresha account."* A testimonial on the page reads: *"My clients love it. Half of them don't even realize they're not texting a real person."*

Fresha's help doc says the chat side works **"in Client Connect"**: *"Conversations are customer-initiated, and AI Concierge responds on your behalf... When a request falls outside what AI Concierge can handle... it notifies a team member."* Creative HEAD Magazine reported the launch alongside Fresha's KKR raise (valuation over $1bn, 130,000+ businesses). The same launch included "Team Connect," pitched as reducing "reliance on WhatsApp groups." So Fresha is building its own messaging walls rather than living inside WhatsApp.

Srileo (a competitor, so treat as biased, though its claim matches Fresha's own docs) wrote on 9 August 2026: *"The Connect page says additional Meta and Instagram integrations are coming, but it does not document WhatsApp as a current AI Concierge channel."*

What this means for Lexi's pricing: a solo SA salon on Fresha plus AI Concierge pays about USD 120 a month (roughly R2,100 to R2,200) and must move its whole business into Fresha. Lexi at R499 a month is about a quarter of that, and the owner keeps her own number.

**Confidence:** High on current state. Medium on timing (Fresha's WhatsApp roadmap isn't public).
**Based on:** fresha.com AI Concierge page, Fresha help centre, Fresha pricing, Creative HEAD Magazine, srileo.com comparison.

### Finding 3: Booksy has no AI receptionist of its own and is closed to integrations.

Carly AI (July 2026): *"Booksy doesn't sell an AI receptionist... What Booksy actually built is... a Google search deal"* (agentic booking in Google AI Mode, August and November 2025). Booksy's API docs return HTTP 401, you have to contact Booksy to register an app, and there is **no Booksy app on Zapier**. *"Booksy is a closed box for an ordinary barber or solo stylist."*

Square has "Square Assistant," an SMS bot that lets clients confirm, reschedule or cancel. It's on by default, and owners have hated it. A family-run salon on the Square Community forum wrote: *"we still use paper and pencil appointment book... customers were just changing around appointments, showing up out of the blue... now Im getting flooded with messages from clients trying to change/cancel appointments through the bot! ... I DONT WANT TO TALK TO CUSTOMERS THROUGH SQUARE MESSAGING!"* A 2025 Capterra review from a cosmetics owner (2 to 10 staff) says: *"AI assistant lost us lots of clients."*

That's a design lesson for Lexi. Automation that takes control away from the owner, or that she can't see, gets switched off. Lexi should show the owner every booking and hand the chat to her the moment she wants it. (Fresha's Concierge already works this way: it stops replying as soon as a human replies.)

**Confidence:** Medium-high. The Carly claim is a single source, but it's specific and checkable. The Square forum post is from 2021 but was confirmed by the 2025 Capterra review.
**Based on:** usecarly.com, Square Community, Square help centre, Capterra.

### Finding 4: Fee creep and marketplace commissions are the loudest small-operator complaint.

This shows up on Trustpilot, the App Store and Capterra independently.

**Fresha, Apple App Store** (Fresha for Business, 4.8 from 3.8K ratings), review titled "fee here, fee there, fees everywhere!" (developer reply 11/28/2025): *"Why are we paying a monthly fee to STILL have to pay for text reminders once we surpass 100? Why do we ON TOP OF THAT STILL have a 20% fee for clients through Fresha marketplace... which honestly add up to being more like 25% with credit card transaction fee AND a fee for having a card saved on file."*

**Fresha, App Store**, "Gone from bad to worse" (5-year user, March 2025): *"they're now taking a ridiculous 20% commission on new client bookings... continuous price hikes."*

**Fresha, Trustpilot 1-star** (August 30, 2026): charged the new-client fee on a refunded appointment that never happened, and on a gift-voucher client the salon sold in person. *"We are a small business. These charges add up and directly affect our income."*

**Fresha, Trustpilot 1-star** (August 31, 2026), "Predatory fees": *"If a new client accidentally double books, Fresha charges a 20% fee on the initial total... Pure extortion from small businesses."*

**Fresha, Trustpilot 3-star** (October 2025), a solo operator: *"we are now going to have to subscribe £14.95 a month... I already pay £6 a month for SMS reminder messages... a very big difference for a small single person business."*

**Fresha, Trustpilot 2-star** (February 2026), 8-year user: *"collecting a marketing platform fee when the paying user is sending a direct booking link to a customer... Fresha is a platform that tries to hold the proprietor and the business operations ransom."*

**Fresha, Capterra** (hair stylist, October 2024): *"I can't justify paying upwards of £10K per year for a booking system... find one with fixed costs."*

**Booksy, Trustpilot 1-star** (July 5, 2026): paid Boost fees on clients from the owner's own Google Ads, and on a walk-in who scanned the salon's QR code while sitting in the chair. *"Salon owners pay for customers they generated themselves."*

**Booksy, Trustpilot 1-star** (July 21, 2026): *"booksy took 30% off my existing customers... i lost out on £130 and offered £24 off two months subscription."*

**Reddit** (only the search snippets; the full threads couldn't be scraped): r/hairstylist, "Freshna is now $20 a month": *"Jumping from free to $20/month is tough, especially when many of us stylists started using Fresha because it gave us a fair, accessible option."* r/smallbusiness, "Fresha app new charges March 2025": *"Does anyone here feel frustrated by the newly implemented charges that Fresha started this month (1 March 2025)?"* r/AskUK asks whether Fresha's 20% new-client fee is even legal.

The Booksy Biz Play Store listing confirms the terms: *"We charge 30% of the FIRST visit from a Boost client only."*

**Confidence:** High. Triangulated across three platforms and dozens of reviews.
**Based on:** App Store, Trustpilot (Fresha 1 to 3 star, Booksy 1 to 2 star), Capterra, the vendors' own pricing.

### Finding 5: Support is scripted or AI-run, and fails when money is at stake.

**Fresha, Trustpilot 1-star** (September 20, 2026): *"Always get generic AI response telling me 'they can't help'... then closed the case saying 'problem solved'."*

**Fresha, Trustpilot 2-star** (May 2026): subscription payment failed on Fresha's side. *"Our account has been completely blocked for over 24 hours. Staff cannot log in. Clients cannot book... The in-app chat is locked without an active subscription."*

**Setmore, Trustpilot 1-star** (July 2025): *"1 day I lost over 6 clients visits valued at $800... as clients did not receive their reminders... they advised it's the clients phone service problem."*

**Setmore, Trustpilot 1-star** (April 2026): *"they charge about £50 for every minutes your on the phone to them... spent £46 for less than 5 mins."*

**Calendly, Trustpilot 1-star** (July 2026): *"they will only talk via chat... do not provide any customer service number!"*

Even happy Fresha reviewers say so: *"The useless AI was... useless, but after I was connected to a real person... solved my problem in under 5 minutes."* (September 24, 2026)

Fresha now sells "Premium support" (phone, chat, email) as a USD 14.95 per month add-on.

**Confidence:** High.
**Based on:** Trustpilot (Fresha, Setmore, Calendly), Fresha pricing.

### Finding 6: Reminders break, or clients reply and nobody sees it.

**Setmore, Capterra** (massage therapist, September 2024): *"if the customer texts back to that number instead of my personal number I don't get the messages."*

**Setmore, Trustpilot 1-star** (March 2026): *"Messages don't get sent to customers. This happens over and over. You loose hundreds of dollars in business."*

**Setmore, Trustpilot 1-star** (April 2026): all reminders carry *"the exact same information"* and can't be customised.

**Fresha, App Store**: *"Certain verbiage that you added to reminders... they're in there for good... I am constantly having to verbally tell my clients the correct information."*

**Booksy, Trustpilot 2-star** (September 18, 2026): *"merchants aren't receiving notifications that I'm trying to book an appointment for them to confirm. I was left hanging for several days."*

Every platform treats a reminder as the end of the conversation. On WhatsApp, a reminder is where the conversation starts ("Can I come at 3 instead?"). Lexi should sell the fact that a reply to a reminder goes somewhere and gets answered.

**Confidence:** High.
**Based on:** Capterra, Trustpilot, App Store.

### Finding 7: Lock-in and data hostage are an under-used sales angle.

**Booksy, Trustpilot 1-star** (September 22, 2026), a 10-year user: *"Booksy will not export my client list. There is no way to do it... without buying their marketing add-on... It seems they just don't want me to have my own list."*

**Booksy, Trustpilot 1-star** (April 2026): *"The only reason why I haven't left is because I need to make time to transfer everything to another app... paying them 33.00 a month."*

**Fresha, App Store**: *"I feel I'm somewhat locked in because many of my clients notes are in here."*

**Fresha, App Store** (2025): clients and appointments "disappeared." *"We started keeping track on paper & in Fresha and the paper was always right and Fresha had mistakes."*

A Fresha Trustpilot 3-star review (January 2026) says Fresha *"doesn't give access 'API KEY' to get it linked with other AI Platforms, for example AI Receptionist."*

For Lexi: the client list lives in the owner's own WhatsApp and her own calendar. If she leaves Lexi, she keeps everything. That's a promise Fresha and Booksy can't make.

**Confidence:** High.

### Finding 8: Where the platforms get it right (the balance).

Aggregate ratings are high: Fresha 4.8 on Trustpilot (7,143 reviews) and on Capterra (1,447). Setmore 4.9 on Trustpilot (3,255) and 4.6 on Capterra (960). Booksy Biz 4.7 on Google Play (31.4K). Square Appointments 4.5 on Capterra (262). The exceptions are Booksy's Trustpilot at 3.1 (16.5K) and Calendly at 4.0 (685).

Treat those Trustpilot scores with care. Most of Fresha's 5-star reviews are invited, thanking a named support agent ("Butrint," "Erika").

What owners praise:
- **Clients can book themselves at night.** Square, Capterra: reminders *"cut my cancelation rates down significantly."*
- **Ease of use.**
- **Deposits and no-show fees.** Booksy claims "$15.6 million protected from no-shows last year."
- **A free or cheap entry tier.** An App Store reviewer who moved from a big spa system to solo work: *"didn't make sense to be spending sooo much money on monthly subscription."*
- **Real humans when you finally reach one.**

So "good" means: bookings happen without the owner, no-shows get reduced, and she can reach a person. Lexi must match all three. Deposits for no-shows are a feature Lexi may need to answer.

**Confidence:** High.

## Cross-Platform Validation

| Complaint | Trustpilot | App Store / Play | Capterra | Vendor's own docs |
|---|---|---|---|---|
| Marketplace/Boost commission on clients the salon brought in | Fresha, Booksy (many) | Fresha (App Store) | Fresha | Fresha 20% / min $6; Booksy 30% first visit |
| Free-to-paid fee creep | Fresha | Fresha (multiple) | Fresha ("free forever" promise broken) | Fresha $19.95 base since 2025 |
| Scripted/AI/slow support | Fresha, Booksy, Setmore, Calendly | Booksy (Play), Fresha | Fresha | Fresha sells premium support at $14.95 |
| Reminders fail / replies go nowhere | Setmore, Booksy | Fresha (uneditable text) | Setmore | Fresha: WhatsApp/SMS text "can't be customized" |
| Data lock-in / no export | Booksy, Fresha | Fresha | Fresha (no integrations) | Booksy API behind 401 |
| No real WhatsApp booking | n/a | n/a | n/a | Booksy/Setmore away-message guides; Happoin table |

The strongest signals are the ones that show up in three or more independent places: commission complaints, fee creep, support and lock-in.

## Tensions & Contradictions

- **Headline ratings vs complaint depth.** Fresha's 4.8 on Trustpilot sits alongside a steady stream of detailed 1-star fee complaints. Much of the 5-star volume is support-agent thank-yous from invited reviews. Take the complaint content seriously and the headline score lightly.
- **"Booksy is buggy, Fresha is better."** One App Store reviewer: *"Booksy... feels bloated and buggy... using Fresha has been a MUCH better experience."* Others are leaving Fresha for flat-fee tools: *"personally rather just pay a flat rate like booksy."* Owners mostly aren't loyal to either. They're shopping for predictable cost.
- **Owners want automation, and resent automation they didn't ask for.** Square Assistant got switched off. Fresha's Concierge testimonial ("half don't realise it's not a real person") is a selling point to some owners, while clients on Trustpilot complain about AI support. Lexi needs visible human override and honest disclosure. Fresha's Concierge *"always discloses that it's an AI assistant... cannot be turned off."*
- **Niche WhatsApp-first tools already exist** (Happoin, Srileo Elily at $49 a month, Engrana, Panabotics, SleekFlow, and SA's MyBusinessApp). "Nobody's building WhatsApp booking" is false for the long tail. It's true for the platforms salons actually know by name.

## Primary Sources vs Commentary

- **Primary (verified customer reviews):** Trustpilot 1 to 3 star pages for Fresha, Booksy, Setmore, Calendly and Square; Apple App Store (Fresha for Business); Google Play (Booksy Biz, Setmore); Capterra (Fresha, Setmore, Square Appointments); Square Community forum.
- **Primary (vendor documentation):** Fresha pricing, AI Concierge page and help centre; Booksy help centre and changelog; Setmore WhatsApp page; Square Assistant help.
- **Commentary (with a vendor interest, so treat with caution):** Srileo, Happoin, Engrana and Carly all sell competing products. I used them only where vendor docs corroborate them. The Salon Business and Creative HEAD are trade press.

## Gaps & Negative Rejections

- **Apify was unavailable.** The `APIFY_API_TOKEN` in this environment returned "user-or-token-not-found," so no bulk App Store or Play review pulls or star distributions. The Apple iTunes RSS or search API is blocked by the network proxy. Reddit direct access was blocked and Firecrawl returns no text for Reddit or Facebook group posts. App-store evidence therefore rests on the reviews visible on the listing pages (roughly 8 for Fresha iOS, 3 each for Booksy and Setmore on Play). Fix the Apify token to run a proper 500-review pull with star distributions.
- **G2 wasn't scraped.** Capterra covered the same ground.
- **No South Africa-specific reviews** of Fresha or Booksy turned up. Fresha does list SA salons (fresha.com/lp/en/bt/hair-salons/in/south-africa). ZAR pricing for Fresha wasn't confirmed; the Rand figures here are USD at about R17.5 to R18.5.
- **Square Appointments in SA:** Square doesn't process card payments in South Africa as far as I know. I didn't verify this in this run. If it's true, Square is irrelevant for Cape Town salons except as a design lesson.
- **Calendly** is built for meetings, not salons. Its complaints (billing lock-in, chat-only support) are generic SaaS, and I kept them only as support-quality evidence.
- **Rejected:** Square Trustpilot 1-star reviews are almost all about payments, loans and holds, not appointments, so they were dropped as off-topic.

## All Citations

| Source | Platform | Signal Score | URL |
|---|---|---|---|
| Booksy help: "How to take bookings from WhatsApp" (away-message link) | Vendor docs | 7 | https://support.booksy.com/hc/en-us/articles/28874825868690-How-to-take-bookings-from-WhatsApp |
| Setmore: "WhatsApp is open for bookings" | Vendor docs | 7 | https://www.setmore.com/integrations/whatsapp |
| Booksy Biz "What's New", WhatsApp shortcut (Apr 22 2026) | Vendor docs | 7 | https://biz.booksy.com/whats-new |
| Fresha help: Send appointment reminders (WhatsApp, not customisable) | Vendor docs | 7 | https://www.fresha.com/help-center/knowledge-base/calendar/167-send-appointment-reminders |
| Fresha pricing ($19.95, 20% new-client fee, $0.04-0.11/WhatsApp, AI Concierge $99.95) | Vendor docs | 7 | https://www.fresha.com/pricing |
| Fresha AI Concierge product page | Vendor docs | 7 | https://www.fresha.com/for-business/features/ai-concierge |
| Fresha help: AI Concierge in Client Connect | Vendor docs | 7 | https://www.fresha.com/help-center/knowledge-base/ai-concierge/101921-how-ai-concierge-responds-to-messages-in-client-connect |
| Creative HEAD: Fresha launches AI platform / KKR raise | Trade press | 5 | https://creativeheadmag.com/inform-featured/fresha-launches-new-ai-platform-for-salons/ |
| Srileo: Fresha AI Concierge alternative (no WhatsApp channel, 9 Aug 2026) | Competitor commentary | 5 | https://srileo.com/compare/fresha-ai-concierge/ |
| Carly: "Booksy AI: A Google Booking Deal, Not an AI Receptionist" | Competitor commentary | 5 | https://www.usecarly.com/blog/booksy-ai/ |
| Square help: Square Assistant | Vendor docs | 6 | https://squareup.com/help/us/en/article/6731-get-started-with-square-assistant-on-appointments |
| Square Community: "The nightmare that is square assistant" | Owner forum | 7 | https://community.squareup.com/t5/Deposits-Refunds-Account/The-nightmare-that-is-square-assistant/m-p/273830 |
| Trustpilot Fresha (overview, 7,143 reviews, 4.8) | Trustpilot | 5 | https://www.trustpilot.com/review/fresha.com |
| Trustpilot Fresha 1-star (fees, AI support, held money) | Trustpilot | 8 | https://www.trustpilot.com/review/fresha.com?stars=1 |
| Trustpilot Fresha 2-star (account blocked, marketplace "ransom") | Trustpilot | 8 | https://www.trustpilot.com/review/fresha.com?stars=2 |
| Trustpilot Fresha 3-star (£14.95 sub for solo, no API) | Trustpilot | 8 | https://www.trustpilot.com/review/fresha.com?stars=3 |
| Trustpilot Fresha review "Predatory fees" | Trustpilot | 8 | https://www.trustpilot.com/reviews/6a963be390407ccb3e4cfaea |
| Trustpilot Fresha review "0/5 Marketplace Fees" | Trustpilot | 8 | https://www.trustpilot.com/reviews/6a948eae2902c098b43f6d2d |
| Trustpilot Fresha review "Worst app ever" (AI support) | Trustpilot | 7 | https://www.trustpilot.com/reviews/6aafe750410abdbbbb4386f6 |
| Trustpilot Fresha review "Account blocked 24+ hours" | Trustpilot | 8 | https://www.trustpilot.com/reviews/69f71bb6e94c8db03341ee89 |
| Trustpilot Fresha review "Not what it used to be" | Trustpilot | 8 | https://www.trustpilot.com/reviews/698b6361bcf40b34f2d08ddc |
| Trustpilot Fresha review "no API key for AI receptionist" | Trustpilot | 7 | https://www.trustpilot.com/reviews/695e6749f97d9cd3335df528 |
| Trustpilot Booksy 1-star page (3.1, 16,559 reviews) | Trustpilot | 8 | https://www.trustpilot.com/review/booksy.com?stars=1 |
| Trustpilot Booksy "will not export my client list" | Trustpilot | 8 | https://www.trustpilot.com/reviews/6ab29c1aa1bf74be9f4680fd |
| Trustpilot Booksy "Boost" walk-in charged | Trustpilot | 8 | https://www.trustpilot.com/reviews/6a4edb9868488f2bbce1f9f3 |
| Trustpilot Booksy "took 30% off existing customers" | Trustpilot | 8 | https://www.trustpilot.com/reviews/6a5fa20f9a59284fdd465024 |
| Trustpilot Booksy 2-star page (app bugs, notifications) | Trustpilot | 7 | https://www.trustpilot.com/review/booksy.com?stars=2 |
| Trustpilot Setmore 1-star page (reminders fail, phone charges) | Trustpilot | 8 | https://www.trustpilot.com/review/setmore.com?stars=1 |
| Trustpilot Setmore "Unreliable" ($800 lost) | Trustpilot | 8 | https://www.trustpilot.com/reviews/68883f573164d425324b7c59 |
| Trustpilot Calendly 1-star page | Trustpilot | 6 | https://www.trustpilot.com/review/calendly.com?stars=1 |
| Trustpilot Square US 1-star (payments-focused, rejected) | Trustpilot | 2 | https://www.trustpilot.com/review/squareup.com/us?stars=1 |
| Apple App Store: Fresha for Business reviews (4.8, 3.8K) | App Store | 8 | https://apps.apple.com/us/app/fresha-for-business/id1455346253?see-all=reviews |
| Google Play: Booksy Biz (4.7, 31.4K; Boost 30% terms) | Play Store | 6 | https://play.google.com/store/apps/details?id=net.booksy.business |
| Google Play: Setmore (4.8, 6.6K; WhatsApp reminder status) | Play Store | 6 | https://play.google.com/store/apps/details?id=com.adaptavant.setmore |
| Capterra: Fresha reviews (4.8, 1,447) | Capterra | 7 | https://www.capterra.com/p/142138/Shedul-com/reviews/ |
| Capterra: Setmore reviews (4.6, 960; texts-back gap) | Capterra | 7 | https://www.capterra.com/p/122035/SetMore/reviews/ |
| Capterra: Square Appointments reviews (4.5, 262; "AI assistant lost us lots of clients") | Capterra | 7 | https://www.capterra.com/p/170263/Square-Appointments/reviews/ |
| The Salon Business: Fresha Review 2026 | Trade press | 4 | https://thesalonbusiness.com/fresha-review/ |
| Engrana: Fresha vs Booksy vs WhatsApp | Competitor commentary | 4 | https://engrana.es/en/blog/fresha-vs-booksy |
| Happoin: Salon booking software compared | Competitor commentary | 4 | https://happoin.com/en-gb/salon-booking-software |
| Zapier: Calendly + WhatsApp Notifications | Integration docs | 4 | https://zapier.com/apps/calendly/integrations/whatsapp-notifications |
| Calendly Community: "I can't connect calendly to whatsapp" | Owner forum | 5 | https://community.calendly.com/how-do-i-40/i-can-t-connect-calendly-to-whatsapp-1110 |
| MyBusinessApp (SA): Why clients prefer WhatsApp | SA competitor | 4 | https://mybusinessapp.co.za/blog/why-pet-grooming-clients-prefer-whatsapp |
| Reddit r/hairstylist: "Freshna is now $20 a month" (snippet only) | Reddit | 5 | https://www.reddit.com/r/hairstylist/comments/1n5qbrf/freshna_is_now_20_a_month/ |
| Reddit r/smallbusiness: Fresha new charges March 2025 (snippet only) | Reddit | 5 | https://www.reddit.com/r/smallbusiness/comments/1jkyd3a/fresha_app_new_charges_march_2025/ |
| Reddit r/AskUK: legality of Fresha 20% new-client fee (snippet only) | Reddit | 4 | https://www.reddit.com/r/AskUK/comments/1lx5jwv/is_it_legal_for_fresha_to_charge_their_20_new/ |
| Fresha help: Marketplace new client fees | Vendor docs | 6 | https://www.fresha.com/help-center/knowledge-base/billing-and-fees/101357-marketplace-new-client-fees |
| Fresha SA hair salon listings | Vendor | 3 | https://www.fresha.com/lp/en/bt/hair-salons/in/south-africa |
