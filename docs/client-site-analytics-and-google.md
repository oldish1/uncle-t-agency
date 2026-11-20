# Visitor counting and Google visibility for any client site

How to give a site (Uncle T's, Chales, or any client) visitor counting and get it found on Google. Written for Theo. Same steps every time. Takes about 20 minutes per site.

Uncle T's site is done and is the working example: Measurement ID `G-K6Y9ZHWHT8`, property "uncletsautomation.co.za".

## What you can and cannot see

Google Analytics shows visitors anonymously: how many, country and city, phone or computer, where they came from (Google, Instagram, TikTok, WhatsApp), which pages, how long. It never shows names or numbers. That is Google's rule and South Africa's POPIA law. A visitor becomes a lead when they tap **WhatsApp us** or send the contact form, and then you see their number in WhatsApp. The site records those taps as events: `whatsapp_click`, `demo_whatsapp_click`, `contact_form_sent`.

## Part 1: Google Analytics (visitor counting)

1. Go to analytics.google.com, sign in with the Google account that will own it.
2. **Admin** (gear) then **Create** then **Account** (one per business, e.g. "Chales Hair Boutique") then **Property** (the website).
3. Time zone South Africa. Currency: type "Rand"; if missing, any currency is fine.
4. Industry and size: any. Objectives: tick **Generate leads** and **Understand web and/or app traffic**.
5. Platform **Web**, URL of the site, stream name e.g. "Chales Website", leave Enhanced measurement on.
6. Copy the **Measurement ID**, it starts with `G-`. This is the one Claude needs. Do not copy the script it shows, Claude installs the tag so visitors are not counted twice.
7. Give the `G-` code to Claude. Claude puts it in the site and redeploys.
8. Check: open the site on your phone, then Analytics, **Reports**, **Realtime**. You should see 1 user.
9. Mark leads: Analytics, **Admin**, **Events**, wait until `whatsapp_click` appears (after the first tap), then switch **Mark as key event** on.

## Part 2: Google Search Console (so Google finds the site)

1. Go to search.google.com/search-console, **Add property**, **URL prefix**, enter the full address with https.
2. Pick **HTML tag**, copy the code inside `content="..."` and give it to Claude. Do not press Verify yet.
3. Claude adds it to the site and redeploys. Then press **Verify**.
4. **Sitemaps**, type `sitemap.xml`, **Submit**.
5. Type the home page address in the box at the top, **Request indexing**. Google takes days to a few weeks to show a new site.

## Part 3: before any of this works

- The site must be on its own domain with HTTPS (the padlock). Netlify: Domain management, Verify DNS configuration, Provision certificate.
- The site must not hide itself from Google. Uncle T's `static/_headers` noindex was removed on 2026-11-08.
- The privacy page must say the site counts visitors. Uncle T's privacy page does this automatically once `analytics.gaId` is set in `src/lib/content.js`.

## Selling it to clients

Offer "visitor counting and a monthly report" as part of the site. Each client gets their own Analytics property, so their numbers stay theirs. Monthly report: visitors, top pages, WhatsApp taps, where visitors came from, written in plain English.
