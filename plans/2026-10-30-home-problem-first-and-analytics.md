# Plan: Uncle T Home goes problem-first, plus visitor counting and Google

Reference studied 30 Oct: frontdeskops-new.netlify.app (made by someone in a Skool community, for luxury property sellers). It opens on the buyer's pain, names three frustrations, shows the fix as a short story, shows the owner's "Monday 9 AM" moment, then outcomes, FAQ and a free-audit form. We copy the structure, not the look, words or pictures.

Home order: hero in the owner's own words, the quiet problem (three frustrations), the fix (pinned day story, already built), the Monday-morning diary, stat tiles, bento, pricing.
Claims stay true. No invented figures.

Visitor counting: Google Analytics 4 on Uncle T's site and Chante's site, with one Google account so Search Console shows the same sites. Needs a Measurement ID (G-XXXX) and a Search Console verification tag from Theo. Code reads them from `apps/uncletsautomation/src/lib/content.js` (`analytics`); empty means off. Privacy page mentions it only when switched on.

Google finding the site: sitemap.xml, robots.txt, canonical and social tags, structured data. The preview stays hidden from Google (noindex) until the real domain is live. Limit: Studio and Start live under #studio and #start, which Google treats as one page, so only Home is indexed until those become real pages.

Chante's live site: backed up to apps/chales-site, sitemap and robots prepared, NOT deployed (needs Theo's explicit go).
