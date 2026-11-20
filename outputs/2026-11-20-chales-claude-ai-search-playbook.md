# Playbook: getting CHALES named by Claude and other AI tools

> Builds on `plans/2026-11-04-chales-google-page-one.md` (the master plan, on branch ccr-4af36452-pzwamr) and does not repeat it. Baseline taken 20 Nov 2026 with a live web search. Method from the claude-seo repo (`seo-geo`).

## Corrections first

Earlier this week I told you Chanté wasn't on Google Maps and that the service pages weren't built. Both were wrong. A 4 Nov check found her Google listing (46 Alexandra St, Oakdale, zero reviews at the time) and other sessions built the treatment pages, price page, review machine and QR cards. My name search missed her listing and I hadn't read the other branches. My earlier checklist for claiming and verifying the profile is mostly not needed: the open job is confirming Chanté can sign in and adding Theo as manager. I also suggested Fresha and Booksy; you ruled that out on 19 Nov, and that stands (see the open question at the end).

## What "ranking on Claude" means

Claude doesn't have a list of salons with positions. When someone asks Claude for a salon in Bellville and web search is on, Claude searches the web, reads a few pages and answers from them. So being named by Claude means three things:
1. Her pages appear in the search results Claude gets.
2. Her pages are easy to quote (price, place, hours, answer in the first lines).
3. What other sites say about her matches what her own site says.

Claude's search crawler is `Claude-SearchBot`, and her robots.txt allows everything, so access is fine. Which search index sits behind Claude's search isn't something I can confirm from here, so don't promise anyone a specific engine.

## Baseline, 20 Nov 2026

Four searches through a web search tool (US-based, so only an approximation of what a Cape Town user sees):

| Search | Result |
|---|---|
| best hair salon Oakdale Bellville | Fresha directory pages only. Named salons: XCO MAN, Kallos House of Beauty, Love Hair & Beauty, My Hair Department, Salon Elmarie. CHALES absent. |
| nanoplastia Bellville Cape Town salon | **No salon found at all.** Results were facials and microneedling. Nobody is winning this search. |
| keratin treatment Bellville salon prices | Fresha again, almost no real prices. CHALES absent. |
| CHALES Hair Boutique Oakdale Bellville | Not found. Returned Erica's Hair Boutique and Zita Hair Boutique. |

Two readings. Bad: she isn't in the results even by name. Good: "nanoplastia Bellville" is an empty lane, and her page already answers it better than anything that exists (price R1 800 and R2 200, 2 to 3 hours, lasts 3 to 5 months, formaldehyde-free, FAQ markup). The job is to get that page found.

## What the live pages already do right

The Nanoplastia page has a clear title, a description with prices, an opening answer, a key facts table, FAQs ("How much is Nanoplastia in Cape Town?") with matching FAQPage and Service markup, map coordinates and a sitemap. That's what AI tools quote. Don't rebuild it.

## The playbook

**1. Get the pages into search (this week, Theo, 30 minutes).** Add the site to Google Search Console and Bing Webmaster Tools, submit `sitemap.xml`, and use "request indexing" on the five pages. The sitemap shows last-modified 4 Nov and nothing in the baseline shows the pages are indexed, so check this first. Until it's confirmed, everything else is guessing. Needs Chanté's Google login or a manager invite.

**2. Win "nanoplastia Bellville" first.** Open lane, strongest page. Add one more thing to the page: 3 real before/after photos with descriptive captions ("Nanoplastia on 4c hair, Oakdale Bellville") and a "Updated November 2026" line. Then get 3 things pointing at it: the TikTok nanoplastia video descriptions link to the page, a Google Business post, and 2 or 3 genuine answers in Bellville and Cape Town hair Facebook groups where people ask. Repeat the same method for keratin and Brazilian once nanoplastia shows.

**3. Same facts everywhere.** AI tools distrust a business whose details change by site. One name (CHALES Hair Boutique), one address with "inside the Vodacom building", one phone, one set of hours (Tue to Fri 08:00 to 16:30, Sat 09:00 to 15:00, Sun and Mon closed) on Google, the website, Facebook, TikTok, Instagram, Bing Places, Apple Business. The TikTok bio still carries the old number. Fix that first.

**4. Reviews that say what she did.** Claude and others quote review wording. The review machine already exists. Chanté's in-person line should end with "what did you have done?" so reviews say "nanoplastia" and "Bellville". No scripts, no rewards.

**5. Bing Places and Apple Business (free, 30 minutes each).** These feed ChatGPT, Copilot and Siri. They're not Fresha or Booksy, so they fit your rule.

**6. Local mentions that aren't directories.** Brabys, Cylex, a collab with a nail tech or makeup artist who links to her, a school fundraiser voucher listed on the school's page. Each is a real third-party page naming her.

**7. Keep pages fresh.** Update the "prices updated" line and `lastmod` every month. Pages untouched for 6 months lose citations. One new helpful page a month: "Nanoplastia vs keratin on 4c hair", "How to wash after a Brazilian", "How much does hair colour cost in Bellville".

**8. Never.** Fake reviews, paid "AI visibility" packages, hidden text, llms.txt (no proven effect, Google says it ignores it), spamming groups.

## How we measure it

First Monday of each month, same 8 searches as the master plan, now asked in four places: Google, ChatGPT, Claude with web search on, and Perplexity or Gemini. Log date, tool, question, was CHALES named, who was named instead. First target: named for "nanoplastia Bellville" by end of January, and for her own name everywhere. Baseline today is zero of 8.

## Who does what

| Who | What |
|---|---|
| Chanté | Confirms Google sign-in, adds Theo as manager. Photos of nanoplastia work. Asks "what did you have done?" at every review ask. |
| Theo | Search Console and Bing Webmaster, Bing Places, Apple Business, TikTok bio fix, Facebook group answers. |
| Claude | Page updates (captions, dates, new monthly page), consistency check across sites, monthly four-tool check and report. |

## Open question for Theo

The baseline shows Fresha pages fill every "best hair salon in Bellville" result an AI sees. You decided on 19 Nov to go Maps-only with no Fresha or Booksy, and that's a fair call, since it avoids bookings leaking away from Lexi. The cost is that for general "best salon" questions she may stay invisible to AI tools for months. The middle option is a bare Fresha profile with no online booking switched on and Lexi's WhatsApp link in the description. It's your call, and the plan works either way because the treatment searches are open.
