# Local visibility playbook (Google + AI)

How Uncle T Agency gets a small Cape Town business onto page one of Google and recommended by ChatGPT, Gemini, Perplexity, Copilot and Siri. First run: CHALES Hair Boutique, started 20 Nov 2026. Use this for every client after that.

## The idea in one paragraph

Google and the AI assistants recommend a local business when three things line up. The business's own website clearly says what it does, where, and for how much. Google and Bing actually have every page indexed. And the rest of the internet agrees with the website: Google Business Profile, Apple Maps, Bing Places, Facebook, directories and reviews all carry the same name, address and number. Most small businesses have none of the three. Fixing them is mostly setup work, done once, then a light monthly rhythm.

## What we need from the client (intake)

- Login or manager access to their Google Business Profile (or permission to create one)
- Access to wherever the website is hosted, or permission for us to rebuild it
- Their exact name, address, phone, WhatsApp, hours, services and prices
- 20+ real photos: outside, entrance, inside, their work
- A list of their happiest recent clients, for the first review push
- 15 minutes on a call to set up Google Search Console with us

## The steps

Each step is in the client's tickable checklist. The CHALES one is the template: https://claude.ai/artifact/YSHm1L3hynsiYNkBahbUqq (source: `outputs/chales-seo-checklist.html`). For a new client, copy the file, swap the details, publish as a new artifact.

### 1. Baseline (day 1, Claude, 10 min)
Write `data/visibility/<client>.json` with 10 to 12 searches real customers type: brand name, "<service> <suburb>", "<category> <suburb> Cape Town". Then run:

```
python3 scripts/visibility_check.py <client>
```

It saves a dated snapshot in `outputs/visibility/<client>/`. This is the "before" for the case study. Also ask ChatGPT, Gemini and Perplexity the same 3 questions and **screenshot the answers**. Those screenshots are the strongest sales material we'll have.

### 2. Website fixes (week 1, Claude, 1 to 2 hrs)
Audit, then fix:
- One canonical tag per page. A keyword heading (H1) on every page: "<Business>, <category> in <suburb>"
- Structured data (schema.org): LocalBusiness (or HairSalon etc.) with address, geo, hours, phone, price range, `sameAs` social links, `hasMap`; Service + Offer with rand prices on service pages; FAQPage where there's an FAQ
- One page per main service, each with prices and an FAQ, linked from the homepage
- Photos as WebP with descriptive file names and alt text
- `robots.txt` that welcomes the AI crawlers by name, `sitemap.xml`, and `llms.txt` (plain summary for AI)
- An IndexNow key file

Deploy as a Netlify **draft** first, client approves, then publish. CHALES example: `apps/chales-site/`.

### 3. Get indexed (week 1, Theo + client, 20 min)
- Google Search Console: URL-prefix property, HTML-tag verification (client pastes the tag to Claude, Claude adds it), submit `sitemap.xml`, "Request indexing" on each inner page
- Bing Webmaster Tools: import from Search Console
- IndexNow ping (one link)

### 4. Google Business Profile (weeks 1 to 2)
Category, description (Claude writes it), every service with price, hours including holidays, website and WhatsApp booking links, 20+ photos, attributes, then one post a week.

### 5. Reviews (from week 1, ongoing)
A review page on the site that sends happy clients to Google and catches unhappy ones privately (CHALES: `/review/`). The WhatsApp bot sends the link after each visit. The owner personally messages their last 20 to 30 happy clients. Reply to every review within 48 hours. Target 25.

### 6. Same details everywhere (weeks 2 to 3)
One copy-paste block of name, address, phone, hours and URL, used on Instagram, TikTok, Facebook, Apple Business Connect, Bing Places, Fresha/Booksy (for salons) and SA directories (Snupit, Brabys, Cylex, Hotfrog).

### 7. AI recommendation layer (month 2 onwards)
Get into local "best <category> in <area>" lists, answer local Facebook group requests honestly, say the service and suburb out loud in short videos. Monthly: rerun the baseline and the AI questions.

### 8. More pages (month 2 to 3)
Extra services and nearby-suburb pages, before and after photos.

## Measuring and showcasing

Monthly:

```
python3 scripts/visibility_check.py <client> --compare <baseline date>
```

That writes a before-and-after table to `outputs/visibility/<client>/`. At month 3, build the case study from four things: that table, Search Console's clicks and impressions graph, the Google review count then and now, and the AI answer screenshots then and now. Include bookings that came through Google if the WhatsApp bot can tag the source.

## What Claude does vs what people do

Claude does: audit, all website code, structured data, photo work, llms.txt, deploys, every piece of copy (profile description, posts, directory listings, review messages), the monthly checks and the case study.
People do: anything behind a Google, Apple or Microsoft login (Claude can't sign in to those), photos, and asking clients for reviews.

## Realistic timeline

- Week 1 to 2: all pages indexed, profile complete
- Month 1: shows for the brand name and the easiest suburb searches ("<category> <small suburb>")
- Month 2 to 3: page one and the Maps top three for "<category> <suburb>" once reviews pass about 20
- Bigger searches ("<service> Cape Town") take longer and depend on reviews and mentions

Don't promise "number one on Google". Promise the work, and show the before and after.
