# Salon lead finder

Finds Cape Town salons whose own Google reviews complain about the things Lexi fixes, checks they're busy enough to pay R499 a month, and drafts a first WhatsApp message for each one. Code lives in `apps/lead-finder/`.

## What it looks for

Each salon gets a score out of 100, made of three parts:

| Part | Points | What earns them |
|---|---|---|
| Need for Lexi | 50 | Reviews saying "never replied", "couldn't get hold of them", "double booked me", "cancelled last minute" (English and Afrikaans). Owner replies apologising for a missed message. Clients booking on WhatsApp. A cellphone as the main number. No online booking tool. |
| Website gap | 15 | No website at all (15), only a Facebook/Instagram/link page (12), or a website that doesn't load (10). |
| Can they pay | 35 | Number of Google reviews (30 to 400 is the sweet spot), rating 4★ and up, a review in the last four months. |

Hot is 60 and up, Warm is 40 to 59. Salons already using Fresha, Booksy, Setmore and similar tools lose 15 points and aren't pitched Lexi, because they've already solved the problem. Chains (Sorbet, Carlton and the like), closed salons and anyone already in the pipeline (CHALES, Zanzibar, Sistergirl, Reeva, JEM, No Love Lost) are skipped.

Every point comes with a written reason, and the report quotes the review that triggered it, so you can see why a salon made the list before you message them.

## What it produces

- `outputs/leads/<date>/report.md`, the top 25 hot and warm salons with phone, a one-tap WhatsApp link, the evidence, and a first message to edit and send.
- `outputs/leads/<date>/leads.csv`, every salon checked, ready to import into the prospect Google Sheet.
- `data/leads/raw-<date>.json`, the raw sweep, so the scoring can be tweaked and re-run without paying for another search.
- `data/leads/seen.json`, so the next run flags which salons are new.

## Running it

Just ask in a session: "run the lead finder", or "find salons in Parow and Goodwood". Claude runs it and walks you through the results.

Under the hood:

```
python apps/lead-finder/lead_finder.py                                  # all 12 areas, 4 salon types
python apps/lead-finder/lead_finder.py --areas Bellville Parow          # just these areas
python apps/lead-finder/lead_finder.py --queries "barber" "dog groomer" # other trades
python apps/lead-finder/lead_finder.py --source apify                   # deeper: 30 reviews per salon
python apps/lead-finder/lead_finder.py --from-raw data/leads/raw-<date>.json   # re-score, no cost
python -m unittest discover apps/lead-finder/tests                      # check it still works
```

Default areas: Bellville, Parow, Goodwood, Mitchells Plain, Kuils River, Brackenfell, Elsies River, Athlone, Durbanville, Kraaifontein, Belhar, Delft. Default searches: hair salon, braiding salon, nail salon, lash and brow. Both lists sit at the top of `lead_finder.py`.

## Keys it needs

**Google Places key (main source).** `GOOGLE_PLACES_API_KEY`. One-time setup, about 10 minutes:

1. Go to console.cloud.google.com and sign in with your Gmail.
2. Create a project called "Uncle T Leads".
3. Add a billing card. Google insists on one, but the monthly free allowance should cover this; a full sweep is under 100 searches.
4. APIs & Services, Library, search "Places API (New)", Enable.
5. APIs & Services, Credentials, Create credentials, API key. Restrict it to Places API (New).
6. In Quotas, cap it at 200 requests a day so a mistake can never run up a bill.
7. Paste the key into `.env` on your laptop, and into the cloud environment's variables for cloud sessions.

**Apify token (optional, deeper).** `APIFY_API_TOKEN`. Google only hands over 5 reviews per salon, so some salons with real problems won't show them. Apify pulls 30, which catches far more. It's paid per result, so use it on the areas that matter most. Note: the cloud workspace's network currently blocks Apify, so this option only works from your laptop until the environment's network access is widened.

## Known limits

- The review check reads for key phrases. It catches the obvious complaints and will miss sarcasm or unusual wording. Claude can read the full reviews of any shortlisted salon on request.
- Only 5 reviews per salon from Google, sorted by Google's "most relevant", so pain can be hidden. Apify fixes this.
- Website checks need open internet. In a locked-down cloud session the sites can't be opened, so booking tools like Fresha go undetected and those salons score a little high on need. Run from your laptop for the full check.
- Messages are drafts. Each one asks a single yes/no question (can I send the 90-second demo video?). One message, one follow-up a week later, then stop. A yes is their permission to keep talking, which is what POPIA asks for. Video script: `outputs/lexi-demo-video/script.md`.
