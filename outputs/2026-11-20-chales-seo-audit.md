# CHALES Hair Boutique: SEO audit

**Site:** chaleshairboutique.co.za · **Date:** 20 Nov 2026 · **Goal:** get Chanté onto page one of Google for Bellville hair searches (strategy priority 3).

## The short version

The site is built properly. Titles, descriptions, local business data, HTTPS, sitemap and the five service pages are all in place. What's holding it back is outside the code: **Google has only indexed the homepage**, and the salon has no Google reviews or Maps presence doing the work. Competitors on page one for "hair salon Bellville Cape Town" are mostly Fresha, Booksy, Brazilian Bar and established salon sites. CHALES isn't in the top 10.

Where CHALES already wins: "hair salon Oakdale Bellville" is owned by Chanté's TikTok (5 of the top 9 results). The suburb-level search works. The site just isn't the thing ranking.

## Where it ranks today

| Search | CHALES position |
|---|---|
| CHALES Hair Boutique | #5 (website), behind 3 TikTok links and Instagram |
| hair salon Oakdale Bellville | TikTok holds #1, #2, #3, #7, #8, #9. Website not listed |
| hair salon Bellville Cape Town | Not in top 10 |
| brazilian blowout Bellville Cape Town | Not in top 10 (Brazilian Bar is #1) |
| keratin treatment Bellville | One TikTok video at #5 |
| nanoplastia Cape Town | Not in top 8 |
| site:chaleshairboutique.co.za | **1 page indexed out of 6** |

(Checked through Firecrawl's search, which approximates Google. The Maps "local pack" isn't visible this way.)

## What's already right

- Unique titles and descriptions on all 6 pages, each with "Bellville" in them
- HairSalon structured data with address, phone, hours, price range and social links
- Service pages for Nanoplastia, Keratin/Brazilian, Botox/Glowtox, Colour/Highlights, plus a Prices page, all with one clear H1 and their own canonical
- robots.txt allows everything, sitemap lists all 6 pages
- HTTPS with HSTS, http redirects to https, proper 404 page
- All images have alt text, gallery images lazy-load

## Fix list, in order of impact

### 1. Get the 5 new pages indexed (15 min, Theo)
The service pages went live on 4 Nov and Google hasn't picked them up. Set up **Google Search Console** for the domain (verify via Netlify DNS or an HTML file), submit `sitemap.xml`, then use "Request indexing" on each service page. Without this, the service pages do nothing.

### 2. Google Business Profile (biggest single lever)
For "hair salon near me" and "hair salon Bellville", Google shows the Maps pack *above* every website. The site already links to a Google Maps listing (and the /review/ page points to its review form), so a profile exists. Fill it out completely: category "Hair salon", all services with prices, hours matching the site, 20+ photos, the website link, and the booking link pointing to Lexi's WhatsApp. Then post weekly (repurpose the TikToks).

### 3. Google reviews
Already on the roadmap as review automation. The site says "5 Star Rated Salon" with nothing behind it. Reviews are the top ranking factor in the Maps pack. Have Lexi send a review link after each appointment. Target: 25 reviews in 60 days.

### 4. Homepage code fixes (30 min, Claude can do)
- **Two conflicting canonical tags** on the homepage (`...co.za` and `...co.za/`). Delete the one without the slash.
- **H1 is just "CHALES".** Google reads the H1 as what the page is about. Make it "CHALES Hair Boutique, hair salon in Bellville" (keep the big logo look with CSS).
- **Homepage never links to `/prices/`.** The nav goes to the `#pricelist` section instead. Add a "Full price list" link so Google sees the page matters.
- **Add FAQPage structured data** for the existing FAQ section. Can earn extra space in results.
- **14 gallery photos all share one alt text** and are named `IMG-20260221-WA0079.jpg`. Rename (e.g. `balayage-bellville-chales.webp`) and give each a description of the actual style.
- **Images are 240-300 KB JPGs.** Converting to WebP cuts them to roughly a third and speeds up mobile loading, which Google measures.

### 5. Link TikTok to the site
TikTok already outranks the site for Chanté's own name. Put `chaleshairboutique.co.za` in the TikTok and Instagram bios (alongside the Lexi link from the 12 Oct fix) and in video captions now and then. Fix the "Oakdale Beville" typo in TikTok captions, it splits the location signal.

### 6. List on Fresha and Booksy (free listing)
Fresha and Booksy hold #1 and #2 for "hair salon Bellville Cape Town". A free profile on each puts CHALES on page one through their pages while the site builds authority, and gives backlinks.

### 7. More pages, later
Once 1 to 3 are done: a "Balayage in Bellville" page, and short pages targeting nearby suburbs people search from (Parow, Durbanville, Kuils River, Tygervalley). Each existing service page is around 430 words. Adding before/after photos and 2 or 3 client stories per page would strengthen them.

## A pricing note

Brazilian Bar ranks #3 for "nanoplastia Cape Town" with "from R430". CHALES lists R1 800 to R2 200. Not an SEO problem, but anyone comparing from Google will see that gap, so the Nanoplastia page should explain what makes the higher price worth it (product, duration, results).

## Who does what

| Task | Who | Time |
|---|---|---|
| Search Console + submit sitemap | Theo (Claude walks through it) | 15 min |
| Google Business Profile set up / complete | Chanté or Theo | 1 hr |
| Homepage + schema + image fixes | Claude | 30 to 60 min |
| Review requests through Lexi | Claude builds, Theo approves | 1 to 2 hrs |
| TikTok/IG bio links | Chanté | 5 min |
| Fresha + Booksy listings | Chanté | 30 min each |

## Update, same day

- Correction: the service pages already carry Service, price and FAQ structured data, and a Google Business Profile exists. The first pass misread that.
- Built: canonical fix, keyword H1, FAQ + full salon structured data on the homepage, price-page link, 15 photos converted to described WebP (4.1 MB to 1.3 MB), llms.txt, AI-crawler robots.txt, IndexNow key. Uploaded as a Netlify preview; live site unchanged until Theo approves.
- Site source now saved at `apps/chales-site/`.
- Tickable checklist of all 41 steps: https://claude.ai/artifact/YSHm1L3hynsiYNkBahbUqq
