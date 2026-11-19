# CHALES in ChatGPT, Gemini and Claude: the AI search plan

> AEO (answer engine optimisation) and GEO (generative engine optimisation) are two names for the same thing: getting AI tools to name your business when someone asks "who does nanoplastia in Bellville?". Method from the claude-seo repo (`seo-geo`, `local-search-behavior`), checked against a live search of what the web shows for CHALES on 19 Nov 2026.

## The honest version first

- Nobody can pay or trick ChatGPT into recommending a salon. Google's own guidance says optimising for AI answers is "still SEO". The salons that show up have a verified listing, many recent reviews, and the same name, address and phone on many websites.
- It's a smaller door than Google Maps for now. One 2026 study put ChatGPT at about 2% of local traffic compared with Google. But AI use for "find me a salon" is growing fast, and almost all the work overlaps with the Google profile plan. So it's worth doing, as the second layer, not instead of the Google profile.
- Very few Bellville salons are doing this on purpose. That's the real opening. It isn't a secret, it's just not done locally.
- Nobody can promise a date or a position. What we can do is make her the easiest salon for an AI to be sure about.

## Where each AI looks (so we know what to feed)

| AI | Where it gets salon answers | What that means for Chanté |
|---|---|---|
| Google AI Overviews, AI Mode, Gemini | Google's own index and Google Business Profile | The verified profile with reviews is the main lever |
| ChatGPT | Bing's index, plus sites like Yelp, Fresha, Booksy, directories and Reddit. It does not read Google Business Profile directly | Bing Places, booking-site and directory listings |
| Claude, Perplexity | Live web search, favouring pages that answer the question clearly | A clear website with prices and answers |
| Siri | Apple Business listing | Claim Apple Business |

## What the live search showed on 19 Nov

I searched the way a customer or an AI would.
- Searching her name: her **TikTok videos and Instagram appear, her own website doesn't**. Her TikTok captions work well (for example "Nanoplastia Hair Treatment in Oakdale Bellville | Prices & Contact"), so the TikTok habit is already helping.
- Searching "best hair salons in Bellville": the results are Fresha and Booksy list pages and rival salons. Chales isn't on those lists.
- Searching "nanoplastia Bellville / Cape Town": her TikTok shows, but a Brazilian Bar salon page and a Facebook group thread rank above her.
- Her robots.txt already allows every AI crawler, and the site is plain HTML, so AI crawlers can read it. That's fine and needs no change.
- The sitemap I added is live.

I couldn't re-check Google Maps today: Apify's free monthly credit has run out (see below).

## What to do, in order

**1. Finish the Google profile (this is the foundation).** Verified, 15+ photos, services with prices, reviews coming in weekly. Everything below leans on it. Status check needed from Chanté.

**2. Claim Bing Places (30 minutes, free).** This is the one that feeds ChatGPT and Copilot. bing.com/forbusiness, sign in, import from Google Business Profile once verified. Same name, address and phone.

**3. Get listed where AI looks for "best salons".** Create free profiles on Fresha and Booksy (they dominate the Bellville results), plus Apple Business, Facebook business page, and two or three South African directories (Yellow Pages SA, Hotfrog, Cylex). Rule for every one: name **CHALES Hair Boutique**, address 46 Alexandra Street, Oakdale, Bellville 7530, phone 081 433 2756, website link, same description. Mismatches are the biggest problem. Note: Fresha and Booksy let clients book there, which clashes with Lexi. Say Lexi's WhatsApp link is the booking method in the description, or skip booking and just list.

**4. Rewrite the website so a machine can quote it.** The page has one long scroll. AI tools quote self-contained answers, usually from the top of a page. Add short, plain blocks:
- "Where is CHALES? 46 Alexandra Street, Oakdale, Bellville. Tuesday to Saturday, 08:00 to 17:00."
- "How much is nanoplastia in Bellville? From R___ for short hair, R___ for long. Takes about ___ hours."
- Same for Brazilian blowout, keratin, colour and highlights, Botox and Glowtox, the R650 membership.
Each as its own page eventually (one page per service), with real price, how long, who it suits, and a photo. Use Chanté's real numbers, not guesses. Update dates on the page and refresh every few months, because AI tools prefer recently updated pages.

**5. Be where people ask.** There's a Facebook group thread right now ("Nanoplastia hair treatment salons in Durbanville?") where salons get named. Chanté, or you for her, answers real questions in Bellville and Cape Town hair groups: helpful first, name and area mentioned honestly, never spam. YouTube and Reddit mentions correlate with AI visibility more than links do. Cross-post her best TikToks to YouTube Shorts with the same caption style (service, Oakdale Bellville, price).

**6. Reviews, again.** AI tools quote what reviewers say ("great nanoplastia, ladies at CHALES in Oakdale"). When asking clients for reviews, ask them to mention what they had done. Don't script it or reward it, just ask "what did you come in for?" in the review message.

**7. Things that don't work, skip them.** Fake reviews, buying "AI ranking" packages, stuffing the site with keywords, a file called llms.txt (no proven effect, Google says it ignores it), or spamming comment sections with her name. These get listings removed.

## How we check if it's working

Every month, on the same day, ask each AI the same 8 questions and write what comes back in a simple sheet (date, tool, question, was CHALES named, who else was):
1. Best hair salon in Oakdale, Bellville
2. Where can I get nanoplastia in Bellville?
3. Affordable hair salon in Bellville for Brazilian blowout
4. Hair salon in Bellville open on Saturday
5. Who does keratin treatment near Bellville Cape Town?
6. CHALES Hair Boutique, is it good?
7. Hair salon with membership in Bellville
8. Botox hair treatment Cape Town northern suburbs

Baseline today: I expect her to be named for question 6 only, and that probably only through TikTok. The first goal is being named for 1 or 2 within three months. I can run the check with web search and add the results to the sheet.

## Who does what

| Task | Who | Time |
|---|---|---|
| Google profile verified | Chanté | 20 min (still open) |
| Bing Places, Apple Business, directories, Fresha/Booksy | Theo, using Chanté's details | 2 to 3 hours total |
| Real price list from Chanté (per service, per hair length) | Chanté | 15 min, send it to Theo |
| Website answer blocks, then service pages | Claude and Theo | Answer blocks one session, pages later |
| Monthly AI check | Claude | 20 min a month |

## Selling this to the next salon

"We get your salon found in Google Maps and by AI tools" is a real offer almost nobody in Bellville has. Once Chanté's numbers move (reviews, calls, Lexi bookings from Google), that's the case study for Zanzibar and Sistergirl.

## Open items

- Apify's free plan is used up for the month (the $5 limit can't be raised). It blocks the Google Maps rank scan and the lead scraper until the cycle resets, or until it's upgraded. For a monthly rank check this is cheap, a small paid plan covers it.
- Need Chanté's real prices to write the answer blocks.
- Need to know whether she's verified yet.
