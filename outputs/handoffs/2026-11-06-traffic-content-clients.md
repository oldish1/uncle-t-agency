# Handoff: reels, traffic and getting clients (new session)

Written 6 Nov 2026 from the websites session. This new session owns **content, traffic and winning clients**. The websites session keeps building and fixing the sites. Don't redo website work here: ask Theo to take site changes (copy, colours, pages, deploys) to the websites session.

## Who and what
Theo (Uncle T), Cape Town, Ravensmead. Uncle Ts Automation sells Lexi (a WhatsApp booking assistant on her own dedicated number) and websites to small Cape Town businesses, salons first. Voice is NOT built yet, so never claim it, "coming soon" only. Prices: website R799 setup + R499/month; Lexi R1,499 setup + R499/month; both R1,499 setup + R799/month. Demo number 076 492 4196. First live client: Chales Hair Boutique (Chante, Bellville). Theo's sister Nita runs Rags To Riches Cleaning (separate site coming, own booking bot Luna).
Theo works from his phone, keeps steps short and one at a time, wants things he can tick off. Writing rules: `reference/writing-style.md` (no em dashes, plain, contractions), then `humanizer` for client-facing copy. Every claim must be true: no invented numbers, testimonials or results.

## The plan this session executes
- `plans/2026-11-03-launch-and-traffic-plan.md`: 35 numbered, tickable steps (launch, weeks 2 to 4, months 2 to 3, voice track, pricing decisions, weekly numbers).
- Research behind it: `reference/research/2026-11-03-traffic-pricing-voice.md` (Hormozi's Core Four: warm, cold, content, ads last; Gary Vee: document don't create; Liam Ottley crowd: niche, tell your network, free testimonial clients). For local owners the order is warm outreach, WhatsApp and in-person, then local content, Google Maps and reviews, then small ads.
- Already made, in `outputs/content/`: `daily-checklist.md` (10 numbered daily items), `outreach-messages.md`, `google-business-profile.md`, `starter-leads.md` (8 unchecked salons), and `reel-1-missed-booking.mp4` (12 second vertical reel of the sample Lexi chat, made from screenshots with ffmpeg).
- Other useful files: `outputs/2026-09-27-lexi-walkin-pitch.md`, `outputs/2026-10-12-chales-tiktok-fix-and-growth-plan.md` (Chales' TikTok: 4,250 followers, the bio had a wrong number), `context/marketing.md`, `plans/2026-09-27-lead-scraper-agent.md`.

## What this session should do first
1. Cut 2 more reels (9:16, captions burned in) from clips Theo sends, or from screen recordings of the live site and chat. ffmpeg is installed here. Playwright video recording is NOT available; take rapid screenshots and stitch with ffmpeg as done before. Each reel ends with the demo number and the site link.
2. Write bios and 3 captions for TikTok, Facebook Page and Instagram (same name `uncletsautomation`, same bio, same link). Theo makes the accounts himself; Claude cannot post for him.
3. Build a one-page flyer with a QR code that opens WhatsApp to 076 492 4196 (for walk-ins).
4. Keep the lead list moving. The Apify lead scraper hit "Monthly usage hard limit exceeded", so build the list by hand with Firecrawl searches, checking each salon for a phone number and whether it already has online booking (Booksy, Fresha). Skip those that do.
5. Each Friday help Theo read the numbers (messages sent, replies, demos, yeses, WhatsApp taps, site visits) and decide what to do more of.
6. Plan the founding offer (strategy: five founding clients at a discount for a testimonial and one tracked number) and the case study with Chales. Theo decides terms.

## State of the sites (so you can talk about them accurately)
- Uncle Ts site: SvelteKit, deployed to the Netlify site `uncletsautomation-preview` (https://uncletsautomation-preview.netlify.app). Home leads with the owner's pain ("Every missed message is a missed booking"), then the pinned day story, stat tiles, bento, pricing; Studio and Start are the other two views. Contact shows suburb only: Ravensmead, Cape Town, and adamst70@gmail.com. Still hidden from Google (noindex) on purpose.
- Domain `uncletsautomation.co.za` is attached in Netlify but shows "Your connection is not private": no certificate yet, DNS not finished. Theo is fixing it in Netlify Domain management. Don't send people to the domain until the padlock works; use the netlify.app address.
- Pending from Theo: Google Analytics G- ID and Search Console tag (the websites session puts them in), Meta Billing Hub payment method for the WhatsApp numbers (each number only gets 1,000 free replies a month since 1 Oct 2026), Google Business Profile, social accounts.
- Chante's site (chaleshairboutique.co.za) is live on Netlify and was backed up to `apps/chales-site`. A sitemap deploy is prepared but NOT deployed; it needs Theo's explicit go.

## Rules and gotchas
- Never post, message or email anyone on Theo's behalf. Draft only; Theo sends.
- No cold WhatsApp blasts from the business number. One-by-one personal messages only.
- Netlify deploys cost credits (account is on the Personal plan, 1,000 credits). Don't deploy from this session; hand site changes to the websites session.
- The permission check blocks: deploying to a client's live site, changing domain or certificate settings, and running downloaded third-party code. Don't try to get around it; ask Theo.
- Never write secrets (keys, tokens) into the repo; it is public.
- Log your work as rows in `ledger/theo.md` (append only; another session also writes there).
- Skills in `.claude/skills/` you will use most: writing-style, humanizer, supadata (video transcripts), firecrawl (research), apify (if limit resets), plus ffmpeg for video.
