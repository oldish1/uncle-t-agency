# CHALES review machine: setup and go-live

> Built 8 Nov 2026. Based on the "How did I do?" video Theo shared: after the visit, the client gets a message, taps through to a star page, happy clients go to Google, unhappy clients reach Chanté first. Part of Phase 2 of `plans/2026-11-04-chales-google-page-one.md`.

## How it works

1. **In the salon:** an NFC card (with a QR code on it too) at the mirror or the till. Tap or scan, and the CHALES review page opens.
2. **That evening at 18:30 (Tue to Sat):** every client Lexi booked that day gets a WhatsApp: "How did Chanté do?" with a **Rate your visit** button. It opens the same page with their name already on it.
3. **The page** (chaleshairboutique.co.za/review): 5 stars.
   Same layout as the video: stars, then a message, then the **Leave a review on Google** button, then "Anything you want me to know? (optional)" with **Send to Chanté**.
   - **4 or 5 stars:** "Thanks, that means a lot. A Google review helps a small salon like CHALES more than anything."
   - **1 to 3 stars:** "Thanks for being straight with me. I'm sorry it wasn't right. I'd like to call you before you leave a review, so I get the chance to make it right. Or WhatsApp me now on 081 433 2756." Name and number boxes appear (filled in when they came from WhatsApp). The Google button stays, as in the video (Google bans hiding it from unhappy clients).
   - **Strangers:** the page isn't in her website menu and is hidden from Google search, so people only reach it through the WhatsApp button or the card. A rating on this page never goes to Google by itself; only the client can post a Google review.
4. **Chanté's alert:** any 1 to 3 star rating, or any written note, reaches her WhatsApp within seconds: "Review page: 2 out of 5 from Thandi (2771...). They said: ..."

## What's built

| Piece | Where | Status |
|---|---|---|
| Review page | `apps/chales-site/review/` (made by `build_pages.py`) | Built and tested. Goes live with the next website deploy. Hidden from Google search on purpose. |
| Alert scenario | Make: **Chales - Review Feedback Alerts** (8445087), webhook "Chales - Review page feedback" | **On, in test mode:** alerts go to Theo (27714304346). 3 test alerts sent 8 Nov. |
| Evening WhatsApp | Make: **Chales - Review Request (after visit)** (8445153), Tue to Sat 18:30 | **Off.** Waiting for the WhatsApp template. Test mode set: only sends to Theo's number. |
| QR code for the cards | `outputs/2026-11-08-chales-review-qr.png` | Ready. Points to chaleshairboutique.co.za/review?s=card |

## Theo's steps

### 1. Send Chanté's Google review link (done 8 Nov: https://g.page/r/CfHUNmaFuJC9EBM/review, now on the page)
Google Business Profile app (or Google "CHALES Hair Boutique" while signed in as her), **Ask for reviews**, copy the link (`g.page/r/...`). Until then the page's Google button opens her listing, where "Write a review" is one more tap.

### 2. Create the WhatsApp template (about 5 minutes)
WhatsApp Manager (business.facebook.com, WhatsApp Manager, Message templates, Create template), on the CHALES business number:

- **Name:** `review_request` (exactly this)
- **Category:** Utility. Meta may move it to Marketing, which is fine (slightly higher cost per message).
- **Language:** English
- **Body:**
  > Hi {{1}}, it's Chanté from CHALES Hair Boutique. Thank you for coming in today, I just want to make sure you love your hair. How did I do, 1 to 5? Tap below to let me know.
  - Sample for {{1}}: `Thandi`
- **Button:** Call to action, Visit website
  - Text: `Rate your visit`
  - URL type: **Dynamic**
  - URL: `https://chaleshairboutique.co.za/review?{{1}}`
  - Sample: `n=Thandi&p=27714304346`

Approval usually takes minutes to a day. Tell Claude when it's approved.

### 3. Program the NFC cards
Buy **blank, rewritable** cards or stands (NTAG213 or NTAG215), not ones locked to the seller's platform. With a free app like **NFC Tools** (Android or iPhone): Write, Add a record, URL, `https://chaleshairboutique.co.za/review?s=card`, write, tap the card. Test with your own phone. Print or stick the QR code on the card as well.

### 4. Go live (Claude does these once you say go)
1. ~~Deploy the website (review page included).~~ Done 8 Nov 2026, live deploy 6af0c20b6aca41a5e4dd4ca3.
2. When the template is approved: switch on the evening scenario, test it with a booking on Theo's number, then clear its test-mode number.
3. Switch the alerts from Theo's number to Chanté's (27814332756).
4. Swap in the real Google review link and redeploy.

## Rules that keep the Google profile safe
- Every client sees the Google button, whatever they rate.
- No discounts, freebies or competitions in exchange for reviews.
- Reply to every Google review within a day or two.
