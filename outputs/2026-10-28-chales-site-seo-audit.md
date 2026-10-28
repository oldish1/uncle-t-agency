# CHALES website SEO audit, 28 Oct 2026

> Run by hand with the claude-seo checks (technical, local, schema, tracking) against chaleshairboutique.co.za. The repo's full `/seo audit` needs the plugin installed in a fresh session, so this covers the same ground with direct fetches. Speed score is missing: Google's PageSpeed service refused the request (daily quota), rerun later.

## Verdict

The site is decent for a one-pager: fast to load (1.3 seconds, 70 KB page), HTTPS, a real address, hours, prices and an FAQ. It has no way to tell you whether it works, and one thing hurts her on Google: the map embed isn't pointing at a real business listing.

## What's good

- Title and description say "Bellville", "Oakdale" and the services.
- `HairSalon` schema with name, address, hours, price range, phone, social links.
- Dedicated sections for prices, payment, FAQ and gallery. 8 headings, one H1.
- All 17 photos have alt text. Netlify hosting, HTTPS, robots.txt allows everything.
- Two WhatsApp booking buttons that open Lexi with a pre-filled message, plus a tap-to-call link.

## What's wrong, most important first

1. **No analytics.** No Google Analytics, no Search Console tag, nothing. Right now nobody can say how many people visit or how many book because of the site. (The "G-20260221" hits in the code are just a photo filename, not a tracking ID.)
2. **Map embed has a made-up place ID** (`0x1dcc503a97c4b5e5:0x1`). It shows an address pin, same as Lexi's "Get Directions" link, not her business. Replace it with the real embed once the Google profile is verified.
3. **Phone numbers disagree.** Site and schema say 081 433 2756, buttons go to Lexi 071 429 6057. See the number decision in the profile plan.
4. **No sitemap.xml** (404). Google can still find a one-page site, but a sitemap gets it into Search Console cleanly. 5 minutes to add.
5. **Photos are straight from WhatsApp**, 240 to 310 KB each (17 of them, about 4.5 MB if all load). They're lazy-loaded so the page is quick, but compress to ~80 KB each and rename (`nanoplastia-bellville.jpg` not `IMG-20260221-WA0112.jpg`). Filenames count a little, and phones on prepaid data will thank her.
6. **`sameAs` links** point at a Facebook page and an Instagram with 18 followers and one post. Fine to keep Instagram, but verify the Facebook page exists.
7. **Single page for everything.** Google ranks pages, and the #1 local ranking factor is a page per service. One page for Nanoplastia, one for Keratin and Brazilian, one for Colour and Highlights, each with price, before/after photo and a WhatsApp button. This is the bigger SEO job, and it's the Next.js build mentioned in `CLAUDE.md` if we rebuild.
8. No `aggregateRating` in schema yet. Add after 10+ Google reviews, it can show stars next to her listing.

## Does the website bring clients?

Right now, nobody can answer that, and that's the real finding. Quick, free ways to find out:

- **Google Analytics 4 and Search Console**, both free. Needs Chanté's Google login (or she adds Theo as a user). Gives visitors per day, where they come from, what people search to land on her, and how many tap the WhatsApp button. About 30 minutes to set up and I can write the code.
- **Tag each channel in Lexi.** The website buttons already send "Hi Lexi! I'd like to book..." Give the Google profile its own opening text ("Hi Lexi, I found you on Google") and TikTok another, then have Lexi write the source into her booking sheet. Within a month the sheet answers "where do my bookings come from?" without any extra software.
- **The Google profile itself** shows calls, direction requests, website clicks and message clicks under Performance. That's usually where local salons get most of their leads.

## Fix list, in order

1. Verify Google Business Profile (Chanté).
2. Add GA4 and Search Console, add sitemap.xml (Theo, 1 hour).
3. Replace the map embed with the real listing and fix the phone numbers (Theo, after verification).
4. Compress and rename photos (Theo, 30 minutes).
5. Add `aggregateRating` once reviews pass 10.
6. Rebuild with a page per service when there's time, using the taste skill for design.
