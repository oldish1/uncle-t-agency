# What overseas tools sell to bigger salons, plumbers, electricians and cleaners (and what Lexi should steal)

Research date: 22 September 2026. Companion to `2026-09-22-booking-competitors.md` (SA salon competitors, copy list) and `2026-09-22-solo-salon-pains-and-offer.md` (solo salon pains, founding offer, Theo's running costs). Anything already covered there isn't repeated here.

How this was done: web searches only. Most vendor pricing pages were blocked from this machine, so prices come from search-result summaries of vendor pages and third-party pricing guides. Anything I couldn't confirm is marked **(unverified)**. My own reasoning is marked **(my read)**. Money is converted at about R18 to the US dollar, R11.50 to the Australian dollar, R3.30 to the Brazilian real and R0.21 to the Indian rupee, so every Rand figure is "about".

---

## 1. Bottom line

The American and Australian trade tools (Jobber, Housecall Pro, ServiceTitan, ServiceM8, Tradify, Fergus) all sell the same eight or so things: answer every enquiry fast, quote quickly, schedule and send the right person, text the client "on my way", take photos on the job, invoice and get paid on the spot, ask for a review, and bring the client back for the next service. None of it happens in WhatsApp, because Americans text by SMS and call. The hottest thing in that market right now is the AI receptionist that answers missed calls (Avoca, Rosie, Goodcall, Sameday, Jobber's own), which costs from about R520 to R27,000 a month. Meanwhile Brazil, India, Indonesia and Kenya already do quotes, bookings and payments inside WhatsApp, and small Brazilian plumbers pay about R500 to R1,300 a month for an AI that asks for a photo of the problem, gives a price range and books the visit. Nobody I found sells that as a done-for-you service to Cape Town trades. Lexi's stack (WhatsApp Cloud API, Claude with image understanding, Make.com, Google Calendar and Sheets, Yoco/PayFast links) can copy most of the list. My recommendation: go after **cleaning businesses second**, because it's the same booking engine as salons, recurring every week, and Nita's Rags to Riches is a free pilot sitting right there. Then **plumbers third**, as the bigger-money product, built around photo triage, after-hours emergencies and geyser service reminders.

---

## 2. What overseas tools sell, by vertical

### 2a. Medium salons (3 to 10 staff)

The tools here are Mangomint, Boulevard, Phorest and Fresha (plus AgendaPro in Latin America and Qontak in Indonesia). Bigger salons have a problem solo stylists don't: juggling several people's calendars, services with gaps in them (colour processing), and keeping staff busy and paid correctly.

| # | Feature | Who sells it | Price in Rand | Pain it solves |
|---|---|---|---|---|
| 1 | **Gap-filling "smart" scheduling.** The system books around processing time (colour sitting for 40 minutes) so the stylist can take a quick cut in the gap, and avoids leaving useless 15-minute holes. | Boulevard ("Precision Scheduling") | From about R2,840 to R7,380 a month per location | Dead time in the day that nobody can sell |
| 2 | **Booking by text link.** Staff send a link by text and the client finishes the booking themselves. Mangomint calls it Express Booking. | Mangomint | About R2,160 per location plus R180 per user a month (new pricing from 1 August 2026) | Front desk tied up on the phone |
| 3 | **Smart waitlist.** When someone cancels, the next person who wanted that slot gets offered it. | Mangomint ("Intelligent Waitlist"), Fresha | Included in plans above; Fresha about R90 per team member | Cancelled slots going empty |
| 4 | **Virtual waiting room / self check-in.** Client taps a link when they arrive, the stylist gets pinged. | Mangomint | Included | Reception bottleneck, staff not knowing the client's here |
| 5 | **Rebooking prompts and "reconnect" campaigns** for clients who haven't been in for a while. | Phorest (Reconnect), Fresha, AgendaPro | Phorest quote-only, third parties say from about R1,800 to R2,700 a month **(unverified)** | Clients drifting away |
| 6 | **Loyalty points card.** Phorest's TreatCard claims over 4 million users. | Phorest | Included | Getting clients in more often and spending more |
| 7 | **Deposits and no-show rules per service**, set once and enforced automatically. | Fresha, Boulevard, Mangomint | Included, card fees extra | No-shows on long, expensive services |
| 8 | **Staff commission, targets and pay.** Fresha is adding team target tracking in 2026. | Fresha (Team Pay), Mangomint (payroll add-on), AgendaPro | Fresha included; Mangomint add-on price not found | Arguments about who earned what; owner doing payroll by hand |

Two more worth knowing about. Fresha is rolling out a shared inbox for texts, email and **WhatsApp chats** inside Fresha in 2026, so the "no WhatsApp" gap Lexi exploits against Fresha is closing, at least for reading and replying by hand ([Fresha 2026 roadmap](https://www.fresha.com/blog/Up-Next-2026)). And salons with stylist levels charge different prices for the same service (junior R650, senior R850 for a cut, as an example of the usual 15 to 25% step), which any booking bot for a 5-chair salon has to handle ([Bella Booking](https://bellabooking.com/guides/salon-pricing)).

### 2b. Plumbers

The tools: Jobber, Housecall Pro, ServiceTitan (big US firms), ServiceM8, Tradify, Fergus (Australia and New Zealand, popular with small teams), plus AI receptionists (Avoca, Sameday, Rosie, Goodcall, Smith.ai) and photo-to-quote apps (QuoteIQ, BuildFolio, SimplyWise).

| # | Feature | Who sells it | Price in Rand | Pain it solves |
|---|---|---|---|---|
| 1 | **AI receptionist that answers 24/7**, books the job and spots emergencies. Avoca answers in under 2 seconds, recognises "burst pipe" type language and sends it to the on-call plumber. | Avoca, Sameday, Rosie, Goodcall, Smith.ai, Jobber Receptionist, Housecall Pro CSR AI | Jobber Receptionist about R520 a month for 30 conversations then about R14 each; Rosie from about R880; Goodcall from about R1,420; Smith.ai AI from about R1,760; Sameday from about R8,080; Avoca reported around R27,000 **(unverified)** | The plumber's under a sink and can't answer. US figures say 27% of home service calls go unanswered and most callers phone the next plumber |
| 2 | **Missed-call text-back.** If a call isn't answered, the caller gets a text within seconds: "Sorry we missed you, what's the problem?" | Sold as a standard add-on by most US tools and marketing agencies; Numa does it for car dealers | Numa reported about R3,600 to R7,200 a month **(unverified)** | Caller hangs up and doesn't leave a voicemail (80% don't, per vendor stats) |
| 3 | **Quote from photos.** Client sends photos, the AI builds a priced estimate from the plumber's own price list. | QuoteIQ AI Estimator (up to 5 photos), BuildFolio, SimplyWise, Quotr; Brazilian WhatsApp agents do it in chat | Brazilian WhatsApp estimate agents about R500 to R1,300 a month; US app prices not confirmed | Driving out to look at a job that turns out to be tiny or not worth it |
| 4 | **Flat-rate price book with "good, better, best" options** so the plumber shows the client three prices on the spot. | ServiceTitan Pricebook, Jobber quotes with optional line items | ServiceTitan about R4,400 to R9,000 per technician a month plus R90,000 to R900,000 setup | Haggling, and underquoting because it's done from memory |
| 5 | **"On my way" text with ETA**, sometimes with a live map link. | Jobber, Housecall Pro, ServiceM8 ("On the Way" plus Track My Arrival add-on) | Jobber from about R700 a month; ServiceM8 from about R330 a month | "Where's the plumber?" calls, and nobody home when he arrives |
| 6 | **Job card with before and after photos, notes and client signature**, turned into a report the client gets. | ServiceM8, ServiceTitan, Tradify, Fergus | ServiceM8 A$79 to A$149 plans, about R910 to R1,710; Tradify about R850 to R1,100 per user; Fergus about R950 to R1,350 per user **(currency unverified)** | Disputes ("you didn't fix it"), insurance claims needing proof |
| 7 | **Invoice and payment link sent the moment the job's done**, plus automatic chasing. | Jobber, Housecall Pro, ServiceM8, Tradify | Housecall Pro about R1,060 to R5,380 a month | Waiting weeks to get paid, awkward "please pay" messages |
| 8 | **Service plans and maintenance reminders.** Housecall Pro sends a reminder at the one-year mark and auto-books recurring maintenance; ServiceTitan sells "memberships". | Housecall Pro, ServiceTitan, Sameday (its AI sells the memberships) | Included in plans | One-off customers never come back; quiet months |

Also sold: automatic review request 2 hours after the job (Housecall Pro), and consumer finance for big jobs (Housecall Pro, 3.9% merchant fee). Finance isn't something Theo can offer, so I've left it off.

### 2c. Electricians

Electricians use the same tools as plumbers (Fergus, ServiceM8, Tradify, Jobber, Housecall Pro, ServiceTitan), so most of the list is shared. The differences are paperwork and planned work.

| # | Feature | Who sells it | Price in Rand | Pain it solves |
|---|---|---|---|---|
| 1 | **Digital compliance certificates and test sheets** filled in on site, signed on the phone and sent as a PDF. In the UK these are EIC and EICR forms. | iCertifi, Clik, Joblogic, Pro-Certs (UK); ServiceM8 forms (AU) | Not confirmed | Hours of evening paperwork; lost certificates |
| 2 | **24/7 answering with emergency triage** (power out, sparks, burning smell) | Avoca, Sameday, Rosie, Goodcall | As in the plumbing table | Missing the urgent, high-paying calls |
| 3 | **Photo-based quoting** ("send a photo of your DB board") | QuoteIQ, JobCalc, BuildFolio | Not confirmed | Wasted site visits for small jobs |
| 4 | **Quote follow-up.** Automatic nudges on quotes that haven't been accepted. | Jobber (automated quote follow-ups on Grow), Sameday (AI follows up estimates) | Jobber Grow about R3,580 a month | Quotes sent and forgotten, big jobs lost to silence |
| 5 | **Scheduling and dispatch across a small team** with GPS | Fergus, Tradify, Jobber Connect | Jobber Connect about R2,140 a month; Tradify about R850+ per user | Who's where, who's free for the 14:00 job |
| 6 | **"On my way" text and job photos report** | Jobber, ServiceM8, Housecall Pro | As above | Same as plumbing |
| 7 | **Invoice plus payment link on completion** | All of them | As above | Late payment |
| 8 | **Periodic inspection reminders** (UK landlords need an EICR every 5 years, so tools remind landlords automatically) | UK certificate apps, Housecall Pro service plans | Included | Repeat work that comes back on its own |

### 2d. Cleaning businesses

The tools: ZenMaid, Launch27, BookingKoala, Jobber (cleaning edition), and in Kenya and Nigeria a wave of WhatsApp bots that take M-Pesa deposits.

| # | Feature | Who sells it | Price in Rand | Pain it solves |
|---|---|---|---|---|
| 1 | **Instant price by bedrooms, bathrooms and extras** (oven, fridge, windows, garage), then book the slot. | Launch27, BookingKoala, ZenMaid booking forms | Launch27 about R1,150 to R2,300 a month (billed yearly); BookingKoala about R490 to R3,550 | Endless "how much for a 3-bed?" messages |
| 2 | **Frequency discounts** (weekly cheaper than monthly, monthly cheaper than once-off) | Launch27, BookingKoala | Included | Once-off clients who never become regulars |
| 3 | **Recurring visits that schedule and invoice themselves** | Jobber, ZenMaid | Jobber from about R700; ZenMaid Pro about R700 plus R250 per cleaner | Rebuilding the week by hand; forgetting to invoice |
| 4 | **Cleaner checklists** ticked off on the phone with time stamps (standard, deep, move-in/move-out) | ZenMaid, Jobber | ZenMaid Pro and up | "She didn't do the bathroom" complaints; training new cleaners |
| 5 | **Key and access management** (who has which key, gate codes, alarm codes, pets) | ZenMaid ("key management"), Jobber client notes | ZenMaid | Cleaner stuck at the gate, lost keys, security worries |
| 6 | **Assigning cleaners, availability and leave** | ZenMaid Pro Max, BookingKoala | ZenMaid Pro Max about R880 plus R430 per cleaner | Double-booked cleaners, sick days |
| 7 | **Rating after each clean** (client scores the visit, owner sees problems before they become a bad Google review) | ZenMaid Pro Max, BookingKoala | As above | Quiet unhappy clients who just leave |
| 8 | **Client self-service**: request work, approve quotes, pay invoices, see the next visit | Jobber Client Hub, ZenMaid client schedule view | Jobber plans | "What time is my cleaner coming?" messages |

Also common: referral credits and gift cards (BookingKoala Growing plan), and GPS clock-in so the owner knows the cleaner arrived.

### 2e. What the WhatsApp-heavy countries do differently

This matters more than any single American feature, because it shows what's normal once WhatsApp is the channel.

- **Brazil.** Small Brazilian electricians and plumbers use WhatsApp AI agents that ask about the job, collect a photo or video and the address, send a price range and offer visit times. Reported cost about R500 to R1,300 a month ([NexusAI](https://nexusai.com.br/eletricista-encanador-orcamento-ia-whatsapp/)). Since February 2026 businesses can send payment links inside WhatsApp that take Pix (Brazil's instant bank payment) and boleto ([Chuhaiwa](https://chuhaiwa.app/insights/whatsapp-payment-brazil-2026-multiple-methods-en/), **unverified detail**). Blip Go, a small-business WhatsApp bot from Brazil's biggest WhatsApp provider, starts at about R330 a month ([BossBot](https://bossbot.uk/blog/take-blip-pricing-review-2026)). Kommo (WhatsApp sales CRM) charges about R450 to R810 per user a month, with a six-month minimum.
- **India.** WhatsApp Pay runs on UPI (India's instant bank payment) and businesses can take payment in the chat. WhatsApp added bill payments on 2 September 2026. WhatsApp Flows (forms inside the chat with date pickers and time slots) are standard for clinics and salons. Interakt about R590 a month and WATI about R530 a month, plus message fees.
- **Indonesia.** Mekari Qontak sells salon booking through WhatsApp Flows and an AI agent so clients book "without waiting for admin".
- **Kenya and Nigeria.** Local agencies sell WhatsApp bots to plumbers, electricians and cleaners that quote, book and take an M-Pesa deposit in the chat, in English and Swahili. Setup about R7,000 to R28,000 plus about R1,400 a month hosting in Kenya ([SmartBizSystems](https://www.smartbizsystems.co.ke/services/whatsapp-automation)). That's the closest model to Uncle T Agency I found anywhere: a local operator, done-for-you, WhatsApp-first, local payment method.
- **Mexico.** AgendaWPP sells an AI WhatsApp appointment assistant at about R1,420 to R2,320 a month plus about R3,600 setup. AgendaPro sells salon software pushing WhatsApp reminders.

South Africa doesn't have WhatsApp Pay. The local equivalent is a Yoco or PayFast link sent in the chat, which works fine but opens a browser page. That's the one step that won't feel fully "inside WhatsApp" here.

---

## 3. The steal list

Ranked by value to a small Cape Town business, then by effort on Lexi's stack. Effort assumes the rebuilt Lexi (sub-20-second replies) and the must-haves from the salon copy list (cancel/reschedule, reminder buttons, deposits, handoff) are done first.

Tags: **Build now** = next 2 to 4 weeks, reuses what exists. **Next** = within 2 to 3 months. **Later** = once there are paying clients in that vertical. **Skip** = not worth it for Theo.

| # | Feature | Verticals | Value | Effort | Tag | How on Lexi's stack |
|---|---|---|---|---|---|---|
| 1 | **Photo triage and rough quote.** Client sends a photo of the leak, DB board or dirty oven; Claude reads it, asks two or three questions, gives a price range from the owner's price sheet and offers a slot. | Plumbers, electricians, cleaning | Very high | Low to medium | **Build now** | WhatsApp media download in Make, pass the image to Claude with the price list from Google Sheets. Always say "estimate, final price on site". |
| 2 | **Instant cleaning price by rooms and extras**, with frequency discount | Cleaning | Very high | Low | **Build now** | Price table in Sheets, Claude asks bedrooms, bathrooms, extras, frequency. A WhatsApp Flow form is an option but plain chat works. |
| 3 | **Recurring bookings** (every Tuesday, every second Friday) | Cleaning, salons | Very high | Low | **Build now** | Google Calendar recurring events already exist. Lexi just needs to create them and handle "skip this week". |
| 4 | **After-hours emergency triage.** Lexi asks set questions (is water still running, is the mains off, is there sparking), gives safety steps, quotes the emergency call-out fee, and pings the on-call plumber by WhatsApp with a summary and photos. | Plumbers, electricians | Very high | Medium | **Build now** (plumber pilot) | Keywords plus Claude judgement to flag urgency; Make sends the owner a template message; interactive buttons for "Accept job / Pass". |
| 5 | **Invoice plus payment link straight after the job** | All | Very high | Low | **Build now** | Owner WhatsApps Lexi "done, R1,850"; Make creates a Yoco payment link and sends invoice image and link to the client. Reuses Nita's invoice app. Yoco has payment-link and webhook APIs; PayFast charges 3.2% plus R2. |
| 6 | **"On my way" message with ETA** | Trades, cleaning | High | Very low | **Build now** | Owner taps a button in his own WhatsApp chat with Lexi ("On my way, 20 min"), Lexi messages the client with a utility template. |
| 7 | **Review request 2 hours after the job**, only if the client hasn't complained | All | High | Low | **Next** | Scheduled Make step, Google review link. Already planned for salons. |
| 8 | **Service reminders**: geyser service every 2 to 3 years, annual inverter and battery check, "your plumbing COC is valid 6 months" for sellers, rebooking for salons | Plumbers, electricians, salons | High | Low to medium | **Next** | Store "next due" date per client in Sheets, a daily Make run sends opted-in reminders. Costs a marketing-rate message (about 62c plus VAT) each. |
| 9 | **Before and after photo job report** sent to the client (and useful for insurance claims on burst geysers) | Plumbers, cleaning, electricians | High | Medium | **Next** | Worker sends photos to Lexi's number tagged with the job; Make builds a one-page PDF (same method as Nita's invoices) and sends it. |
| 10 | **Access notes per client**: gate code, estate rules, which key, alarm, dogs, "cleaner must be registered on the estate app" | Cleaning, trades | High | Low | **Next** | A notes column in Sheets, sent to the cleaner or plumber the morning of the job. Keep codes out of the client-facing chat (POPIA, security). |
| 11 | **Assign the worker and send them their day** (which cleaner goes where, checklist included) | Cleaning, small trade teams | High | Medium | **Next** | One Google Calendar per worker; a 06:30 WhatsApp to each worker with jobs, addresses, map pins, access notes and checklist. |
| 12 | **Multi-staff salon booking with stylist levels and processing gaps** | Medium salons | Medium-high | Medium to high | **Next** (salons) | Calendar per stylist, price per level in Sheets. Gap-filling around colour processing is harder; start with "colour blocks 2 hours, stylist free from minute 40". |
| 13 | **Quote follow-up** ("Still keen on the geyser replacement? We can do Thursday") | Plumbers, electricians | Medium-high | Low | **Next** | Log quotes in Sheets with a status; nudge at day 2 and day 7. |
| 14 | **Waitlist / cancellation fill** | Salons, cleaning | Medium-high | Medium | **Next** | Already on the salon copy list. |
| 15 | **Missed-call to WhatsApp.** When the owner can't answer a call, the caller gets a WhatsApp from Lexi. | Plumbers, electricians | Very high | High | **Later** | Needs something to detect the missed call. The owner's cell can't tell Make directly. Options: a virtual number that forwards to his cell and fires a webhook on no-answer, or the WhatsApp Business Calling API (not yet open to small providers, per mid-2026 sources). Cheap interim fix: change his voicemail greeting to "WhatsApp this number for a faster reply" and put "WhatsApp only after hours" on the van and Google profile. |
| 16 | **Cleaner checklist ticked off in WhatsApp** | Cleaning | Medium | Medium | **Later** | Interactive list message or a WhatsApp Flow; results into Sheets. Only worth it for teams with 4+ cleaners. |
| 17 | **Rating after each clean** (1 to 5 buttons) | Cleaning | Medium | Low | **Later** | One interactive button message; low scores ping the owner, high scores get the Google review link. Could merge into #7. |
| 18 | **Good / better / best options on quotes** (patch the pipe R850, replace the section R2,400, replace and add a pressure valve R4,200) | Plumbers | Medium | Low | **Later** | Just a quote format. Needs the plumber to give Theo three-tier prices, which is the hard part. |
| 19 | **Maintenance plans** ("Geyser Care: R99 a month, yearly service and priority call-outs") | Plumbers, electricians | Medium | Medium | **Later** | PayFast subscriptions plus a Sheets list. A business decision for the plumber more than a tech build. |
| 20 | **Digital COC paperwork** | Electricians, plumbers | Medium | High | **Skip** for now | SA COC forms are regulated and the electrician signs as the registered person. Lexi can book COC inspections and chase documents, but shouldn't generate the certificate. |
| 21 | **Voice AI answering phone calls** (the Avoca model) | Trades | High | Very high | **Skip** | Different stack, SA call costs, accents, and a R520 to R27,000 a month market in the US that needs volume. WhatsApp voice notes are the local version: Claude can't hear audio directly, but a transcription step could be added later. |
| 22 | **Live map tracking, GPS clock-in, payroll, consumer finance, price books with thousands of items** | Trades, cleaning | Low for this customer | Very high | **Skip** | That's Jobber and ServiceTitan territory. Firms that need it will buy it. |

One cost note: from 1 October 2026 Meta charges about 12c per reply after the free 1,000 a month, and about 62c plus VAT for marketing messages like service reminders ([MyBroadband](https://mybroadband.co.za/news/business/662921-big-change-coming-for-whatsapp-business-in-south-africa-where-every-reply-will-cost-12-cents.html), [ChatMaxima](https://chatmaxima.com/whatsapp-api-pricing/south-africa/)). "On my way", invoices and job reports are utility messages at the cheaper rate **(my read of the categories, check each template when Meta approves it)**.

---

## 4. "Lexi for Trades": what the chats look like

### 4a. Burst pipe at 22:00 (plumber: "Hendricks Plumbing", one owner and one assistant)

1. **22:04, client:** "Hi there's water pouring from my ceiling!!! Geyser I think. Are you open??" (or in Afrikaans; Lexi answers in the same language).
2. **Lexi, within 20 seconds:** "I'm Lexi, Hendricks Plumbing's assistant. We do after-hours emergencies. First, to stop the damage: turn off the water at the mains (usually near the meter at the front of the property) and switch off the geyser at the DB board. Can you do that now?" Two buttons: **Done** / **I can't find it**.
3. If "I can't find it", Lexi sends a short description and a photo guide of a typical meter and DB board. If still stuck, it goes straight to step 5 and flags it "water still running".
4. **Lexi:** "Can you send a photo of the ceiling and, if you can get to it, the geyser? And your address or a location pin?" Client sends two photos and a pin.
5. **Behind the scenes:** Claude reads the photos (water stain spreading from the ceiling near the geyser, drip tray overflowing), tags it "Emergency, likely burst geyser", and Make sends Hendricks a WhatsApp: "EMERGENCY 22:06, Mitchells Plain (pin), likely burst geyser, water off at mains: yes. 2 photos attached. Client: Mrs Adams, 082..." Buttons: **I'll go** / **Can't tonight**.
6. **Lexi to client:** "Thanks. Our after-hours call-out is R1,200 and that includes the first hour. If it's the geyser, replacing a 150L geyser with the compliance certificate usually runs R10,000 to R13,000, and most home insurance covers burst geysers. Shall I send the plumber?" Buttons: **Yes, send him** / **Call me first**. Prices come from Hendricks's own sheet; these are placeholders based on Cape Town ranges.
7. **22:09, Hendricks taps "I'll go".** Lexi: "Hendricks is on his way, about 35 minutes. He'll WhatsApp when he's 10 minutes out. Keep the water and geyser off." If he taps "Can't tonight", Lexi tells the client honestly and offers the first slot at 07:00, or (if the plumber has agreed a partner) passes it to that partner.
8. **Owner taps "On my way, 10 min"** in his chat with Lexi. Client gets: "Hendricks is 10 minutes away, white Hilux."
9. **On site:** Hendricks sends Lexi 3 "after" photos and a voice-to-text note ("replaced 150L Kwikot, new drip tray and valve, COC to follow"). Lexi turns it into a job report PDF with before and after photos, which the client can forward to her insurer.
10. **Invoice:** Hendricks sends "Done, R11,850". Lexi sends the invoice and a Yoco link, and a message: "Your insurer will want this report and the invoice. Need the claim letter too? Just ask."
11. **Two days later:** review request. **In 2 years:** "Hi Mrs Adams, your geyser's due its first service (anode and valve check). Book a slot?" (only if she opted in).

What makes this land in Cape Town: burst geysers are the classic midnight emergency, insurers want photos and a report, and most small plumbers already live in WhatsApp but can't reply with wet hands.

### 4b. Cleaning booking (Rags to Riches, Nita's business)

1. **Client:** "Hi, how much for a clean? 3 bed 2 bath in Durbanville." (Lexi asks one thing at a time, never a long form.)
2. **Lexi:** "Hi! A basic clean for a 3-bed, 2-bath is usually R420 to R650 depending on size. Do you want anything extra?" List message: **Linen change and wash (R196)**, **Inside oven**, **Inside fridge**, **Inside windows**, **No extras**. Prices from Nita's sheet; the R420 and R196 are her real prices, the range is a placeholder.
3. **Lexi:** "How often?" Buttons: **Once-off** / **Every 2 weeks** / **Weekly (save 10%)**. The discount is an example; Nita sets it.
4. Client picks weekly plus linen. **Lexi:** "That's R556 a visit (R420 clean, R196 linen, less 10%). Which day suits you?" It offers three open slots from the cleaners' calendars: **Tue 08:00** / **Wed 08:00** / **Fri 12:00**.
5. **Lexi:** "Is it a security estate or complex? Anything the cleaner needs to know to get in (gate registration, keys, alarm, pets)?" Client: "Estate, I'll register her on the estate app. Key's under the pot, 1 dog, friendly." Lexi saves this to the private access notes and replies: "Got it. Please register Thandi on the estate app for Tuesdays. I won't repeat your key details in this chat."
6. **Deposit (optional per business):** "To lock in Tuesdays, first visit paid upfront: R556. [Yoco link]" The slot holds for 2 hours; Lexi confirms when the Yoco webhook says paid.
7. **Confirmation:** a recurring Google Calendar event every Tuesday on Thandi's calendar, and a message: "You're booked every Tuesday at 08:00 with Thandi. Reply SKIP any week you don't need us."
8. **Monday 17:00 reminder:** "Thandi's coming tomorrow at 08:00." Buttons: **Confirm** / **Skip this week** / **Change day**.
9. **Tuesday 06:30, Thandi gets her day** in WhatsApp: addresses, pins, access notes, dog note, and the checklist for each house.
10. **After the clean:** "How did Thandi do today?" Buttons **1 to 5**. A 5 gets the Google review link the first time. A 1 or 2 goes straight to Nita. The invoice (from the app Theo already built) goes out with the Yoco link.

---

## 5. Which vertical second, and why

**Cleaning second. Plumbers third, and start a plumber pilot early.**

Cleaning wins second place mostly on how little new building it needs **(my read)**:

- It's the same engine as salons: time slots on a calendar, reminders, reschedule, deposits. The new parts (room-based pricing, recurring bookings, access notes, sending the cleaner her day) are all low effort on the steal list.
- It's recurring. A weekly client means 50 bookings a year, and Lexi's reminders and "skip this week" handling earn their keep every single week. That makes R1,000 a month easy to justify, and hard to cancel.
- There's a free, friendly pilot. Nita juggles up to 20 clients, Theo already built her invoice app, and a Make blueprint for her invoices exists. Rags to Riches can be the "CHALES of cleaning" within weeks, with real numbers for the pitch.
- The local market is big and full of small operators competing with SweepSouth. SweepSouth, the Cape Town-born app, takes bookings through its own app; a small cleaning business with Lexi can offer the same instant price and booking inside WhatsApp, under its own name, with the regular cleaner the client trusts. Cape Town char rates run about R400 to R800 a day ([Procompare](https://www.procompare.co.za/prices/cleaning-services/cleaning-services-prices)), so a small firm with 3 to 6 cleaners doing 60 to 120 visits a month is a normal target.
- Security estates are a real Cape Town pain overseas tools don't handle. Estates use visitor apps (VisitMe, Openitem and others) where residents pre-register workers ([SA Technologies VisitMe](https://www.satechnologies.co.za/visitme-industries/residential-estate-complex-access-control)). A cleaner turned away at the gate is a wasted visit. Lexi reminding the client to register the cleaner the day before is a small feature with a big "oh, that's clever" reaction.

The catch with cleaning: a lot of domestic work in SA is one-on-one between a household and a domestic worker, with no business in between. Lexi's customer is the small cleaning company, not the domestic worker, so the pool is smaller than it looks **(my read)**.

Plumbers are the bigger prize, and I'd pitch them third:

- The money per job is much higher. Cape Town call-outs run R350 to R750, after-hours from about R1,170, and a burst 150L geyser replacement with its certificate about R5,500 to R13,000 ([Click&Done](https://clickndone.co.za/blog/plumber-cape-town), [Smart Plumbing](https://smartplumbing.co.za/geyser-repair-cost-cape-town/)). One extra emergency job a month pays for Lexi several times over.
- Cape Town has a plumbing rule nowhere else in SA has: a plumbing certificate of compliance is needed for every property transfer, issued only by a registered master plumber, valid for 6 months ([DVH Attorneys](https://dvh.law.za/plumbing-certificates-requirement-property-transfers-city-cape-town/), [City of Cape Town form](https://resource.capetown.gov.za/documentcentre/Documents/Forms,%20notices,%20tariffs%20and%20lists/Certificate%20of%20Compliance%20-%20transfer%20of%20ownership.pdf)). Plumbing COCs cost about R450 to R1,500 plus repairs. That's steady, bookable, non-emergency work, and estate agents and conveyancers send it. A "book your plumbing COC" flow is the same as booking a salon appointment.
- Geysers need regular care. Advice varies, but a service and anode check every 2 to 3 years is common, sooner in hard-water areas ([Energybee](https://energybee.co.za/guides/geyser-maintenance-south-africa), [KZN Plumbers](https://www.kznplumbers.co.za/geyser-service-interval-sa)). That's a ready-made reminder feature.
- The harder parts: emergencies come in by phone call, not WhatsApp, so missed-call handling (the US tools' best-seller) is a "later" item for Lexi. Plumbers are on ladders all day and harder to onboard. And emergency triage has to be right, so it needs careful testing before a paying client goes live.

Electricians come fourth. The electrical COC is also required on every property transfer in SA and costs about R850 to R1,900 ([Procompare](https://www.procompare.co.za/prices/electricians/electrical-compliance-certificate)), which is good bookable work. But load shedding, the big electrician driver of 2022 to 2024, has been gone for 476 days and Eskom got through the whole 2026 winter without it ([SAnews](https://www.sanews.gov.za/south-africa/eskom-carries-south-africa-through-load-shedding-free-winter), [The Citizen](https://www.citizen.co.za/news/south-africa/eskom-powers-through-winter-476-days-without-load-shedding/)). The leftover opportunity is the installed base of inverters and batteries that need servicing, which suits a "yearly inverter check" reminder. Pitch "Lexi for Trades" to electricians once the plumber version works; it's 90% the same product.

Medium salons (3 to 10 staff) stay on the salon track, not a new vertical. They need multi-stylist booking, stylist-level prices and processing gaps first, and they're the customers most likely to already be on Fresha, which is adding WhatsApp chat in 2026.

---

## 6. Sources

Vendor and pricing sources (most read via search summaries, not the live page):

- Jobber pricing and plans: [Jobber pricing](https://www.getjobber.com/pricing/), [OneCrew](https://www.getonecrew.com/post/jobber-prices), [Software Advice](https://www.softwareadvice.com/field-service/jobber-profile/)
- Jobber "on my way" texts: [Jobber Help Center](https://help.getjobber.com/hc/en-us/articles/7448087796631-On-My-Way-Text-Messages-in-the-Jobber-App)
- Jobber AI Receptionist ($29 for 30 conversations, $0.79 each after): [Jobber Help Center](https://help.getjobber.com/hc/en-us/articles/25315927533847-Receptionist-powered-by-Jobber-AI), [Morgan Systems](https://morgansystems.org/jobber-ai-receptionist-review/)
- Jobber for cleaning (recurring visits, checklists, Client Hub): [Jobber cleaning](https://www.getjobber.com/industries/cleaning-business-software/)
- Housecall Pro pricing and CSR AI: [Housecall Pro pricing](https://www.housecallpro.com/pricing/), [CSR AI help](https://help.housecallpro.com/en/articles/9740104-csr-ai-overview), [QuoteIQ comparison](https://myquoteiq.com/compare/housecall-pro/)
- Housecall Pro "on my way", review requests, service plans, financing: [Housecall Pro features](https://www.housecallpro.com/features/), [Servically review](https://servically.com/blog/housecall-pro-review/) (financing terms **unverified**)
- ServiceTitan pricing and pricebook: [Projul](https://projul.com/blog/servicetitan-pricing-analysis-2026/), [OneCrew](https://www.getonecrew.com/post/servicetitan-pricing), [ServiceTitan Pricebook docs](https://help.servicetitan.com/docs/pricebook) (all prices third-party estimates, **unverified**)
- ServiceM8 pricing, job cards, On the Way and Track My Arrival: [ServiceM8 pricing](https://www.servicem8.com/us/pricing), [Dupple](https://dupple.com/reviews/servicem8), [Track My Arrival](https://support.servicem8.com/help-center/servicem8-add-ons/servicem8-add-ons/what-is-track-my-arrival)
- Tradify: [SelectHub](https://www.selecthub.com/p/field-service-software/tradify/), [Capterra pricing](https://www.capterra.com/p/152413/Tradify/pricing/)
- Fergus: [SelectHub](https://www.selecthub.com/p/field-service-software/fergus/), [Fergus plumbing](https://fergus.com/us/industries/plumbing/) (currency of the $53/$75 prices **unverified**)
- Avoca: [Avoca](https://www.avoca.ai/), [Contractor ToolStack](https://contractortoolstack.com/software/avoca-ai/), [Solvea](https://solvea.cx/blog/best-ai-receptionist-for-hvac) (the $1,500 a month figure is a third-party example, **unverified**)
- Rosie: [Rosie pricing](https://heyrosie.com/pricing), [CloudTalk](https://www.cloudtalk.io/blog/rosie-ai-answering-service-pricing/)
- Sameday: [Sameday pricing](https://sameday.ai/pricing), [OnCrew](https://oncrew.ai/blog/sameday-pricing-2026)
- Goodcall: [CloudTalk](https://www.cloudtalk.io/blog/goodcall-pricing/)
- Smith.ai: [Smith.ai AI receptionist pricing](https://smith.ai/pricing/ai-receptionist), [Loman](https://loman.ai/blog/smith-ai-pricing)
- Numa: [OnCrew](https://oncrew.ai/blog/numa-pricing-2026), [SkipCalls](https://skipcalls.com/comparison/numa) (price range **unverified**, quote-only)
- Missed-call statistics (vendor-sourced, lean high): [Plumbing & Mechanical](https://www.pmmag.com/articles/107694-the-hidden-cost-of-missed-calls-for-plumbers), [Contractor In Charge](https://contractorincharge.com/blog/missed-call-statistics-for-home-service-companies), [CallJolt](https://calljolt.com/blog/guides/home-service-business-missed-call-statistics)
- Photo-to-quote: [QuoteIQ AI Estimator](https://myquoteiq.com/ai-estimator/), [BuildFolio](https://build-folio.com/features/ai-quote/), [SimplyWise](https://www.simplywise.com/blog/best-estimating-app-plumbing/)
- Electrical certificate apps (UK): [iCertifi](https://icertifi.co.uk/bs-7671-electrical-certificates-app/), [Clik](https://www.cliksoftware.com/electrical-certificate-software/)
- Before/after photo reports: [Blitzz](https://blitzz.co/blog/field-service-photo-reporting-software-in-2026), [Nektyd](https://nektyd.com/before-after-job-photo-documentation)
- ZenMaid: [Capterra pricing](https://www.capterra.com/p/133875/ZenMaid-Software/pricing/), [Connecteam review](https://connecteam.com/reviews/zenmaid/)
- Launch27: [Launch27 maid companies](https://www.launch27.com/maid-companies/), [QuoteIQ cleaning booking](https://myquoteiq.com/best-online-booking-software-cleaning-businesses-2026/) (annual prices **unverified**)
- BookingKoala: [Capterra pricing](https://www.capterra.com/p/162331/BookingKoala/pricing/), [CleanBizSoftware](https://www.cleanbizsoftware.com/bookingkoala-pricing/)
- Mangomint: [Mangomint price changes August 2026](https://www.mangomint.com/learn/price-changes-2026/), [Salon Today](https://www.salontoday.com/articles/mangomint-rolls-out-a-simplified-pricing-model)
- Boulevard: [The Salon Business review](https://thesalonbusiness.com/boulevard-software-review/), [G2 pricing](https://www.g2.com/products/boulevard-labs-inc-boulevard/pricing)
- Phorest: [Phorest features](https://www.phorest.com/features/), [TreatCard](https://www.phorest.com/features/salon-loyalty-program-software/), [Pabau pricing](https://pabau.com/blog/phorest-pricing/) (price **unverified**)
- Fresha 2026 roadmap and features: [Fresha Up Next 2026](https://www.fresha.com/blog/Up-Next-2026), [Fresha features](https://www.fresha.com/for-business/features)
- Stylist-level pricing: [Bella Booking](https://bellabooking.com/guides/salon-pricing)

WhatsApp-first markets:

- WhatsApp Flows for booking: [WA.Expert](https://wa.expert/pages/whatsapp-flows-appointment-booking), [TechCrunch on Flows](https://techcrunch.com/2023/09/19/whatsapp-is-introducing-flows-for-a-richer-in-app-shopping-experience)
- WhatsApp Pay in Brazil and India: [Infobip](https://www.infobip.com/blog/whatsapp-payments), [AeroChat](https://aerochat.ai/blog/whatsapp-pay-for-ecommerce-country-by-country-status), [Chuhaiwa](https://chuhaiwa.app/insights/whatsapp-payment-brazil-2026-multiple-methods-en/), [StartupFeed on India bill pay](https://startupfeed.in/whatsapp-bill-payments-india-launch-bbps/) (Brazil payment-link launch date **unverified**)
- Brazil trade estimate agents: [NexusAI](https://nexusai.com.br/eletricista-encanador-orcamento-ia-whatsapp/), [Zapext](https://www.zapext.com/whatsapp-para/eletricistas)
- Blip / Take Blip: [BossBot](https://bossbot.uk/blog/take-blip-pricing-review-2026), [Blip Go](https://www.blip.ai/en/blip-go/)
- Kommo: [Kommo pricing](https://www.kommo.com/blog/kommo-pricing/), [AI Hub Brasil](https://botaihub.com.br/ferramentas/kommo/)
- Interakt and WATI: [Zoko on Interakt](https://www.zoko.io/post/interakt-pricing-guide), [Xobito](https://xobito.com/blog/wati-vs-interakt-complete-comparison-for-2026)
- Indonesia: [Qontak salon booking](https://qontak.com/blog/aplikasi-booking-salon-terbaik/)
- Kenya: [SmartBizSystems](https://www.smartbizsystems.co.ke/services/whatsapp-automation), [App-ening plumbers Kenya](https://www.app-ening.com/ke/industries/home-services/plumber.html) (setup prices from one vendor, **unverified** as typical)
- Mexico: [AgendaWPP](https://agendawpp.com/), [AgendaPro](https://agendapro.com/blog/agendapro-vs-booksy/)
- WhatsApp Calling API and coexistence for +27: [Hyperleap](https://hyperleap.ai/whatsapp-business-api/calling-api), [ChakraHQ coexistence](https://chakrahq.com/article/whatsapp-coexistence-live-eu-uk-europe-whatsapp-business-for-api-live/) (availability for small providers **unverified**)

South African context:

- Meta WhatsApp pricing from 1 October 2026: [MyBroadband](https://mybroadband.co.za/news/business/662921-big-change-coming-for-whatsapp-business-in-south-africa-where-every-reply-will-cost-12-cents.html), [ChatMaxima](https://chatmaxima.com/whatsapp-api-pricing/south-africa/)
- Cape Town plumber and geyser prices: [Click&Done](https://clickndone.co.za/blog/plumber-cape-town), [FlowLeads](https://flowleads.co.za/plumbing/western-cape/cape-town), [Smart Plumbing](https://smartplumbing.co.za/geyser-repair-cost-cape-town/)
- Plumbing COC for Cape Town transfers: [DVH Attorneys](https://dvh.law.za/plumbing-certificates-requirement-property-transfers-city-cape-town/), [City of Cape Town form](https://resource.capetown.gov.za/documentcentre/Documents/Forms,%20notices,%20tariffs%20and%20lists/Certificate%20of%20Compliance%20-%20transfer%20of%20ownership.pdf), [COC Certificate](https://www.coc-certificate.co.za/plumbing-certificate-of-compliance-cape-town/)
- Electrical COC prices: [Procompare](https://www.procompare.co.za/prices/electricians/electrical-compliance-certificate), [COC Certificate Cape Town prices](https://www.coc-certificate.co.za/coc-prices/)
- Geyser service intervals: [Energybee](https://energybee.co.za/guides/geyser-maintenance-south-africa), [KZN Plumbers](https://www.kznplumbers.co.za/geyser-service-interval-sa), [Absolute Plumbing Cape Town](https://absoluteplumbingcapetown.co.za/geyser-maintenance/)
- Load shedding status: [SAnews](https://www.sanews.gov.za/south-africa/eskom-carries-south-africa-through-load-shedding-free-winter), [The Citizen](https://www.citizen.co.za/news/south-africa/eskom-powers-through-winter-476-days-without-load-shedding/)
- Inverter and solar maintenance: [Computech Solutions](https://www.computech-solutions.co.za/blog/solar-panel-installation-process-maintenance-checklist-for-south-africa-2026/)
- Cleaning rates and SweepSouth: [Procompare cleaning prices](https://www.procompare.co.za/prices/cleaning-services/cleaning-services-prices), [SweepSouth Cape Town](https://sweepsouth.com/locations/western-cape/cape-town/), [Wikipedia on SweepSouth](https://en.wikipedia.org/wiki/Sweepsouth)
- Estate visitor apps: [SA Technologies VisitMe](https://www.satechnologies.co.za/visitme-industries/residential-estate-complex-access-control), [Openitem](https://openitem.co.za/)
- Yoco and PayFast: [Yoco Developer Hub, payment links](https://developer.yoco.com/api-reference/yoco-api/payment-links/fetch-payment-link-v-1-payment-links-payment-link-id-get), [PayFast fees](https://payfast.io/fees/)
