# Conversation scoring guide

Use with `2026-11-02-conversation-scorecard.csv` (opens in Excel or Google Sheets: File, Import). One row per conversation. Fill it in within an hour of the chat, while you still remember the words. Quote their exact words, in their language.

## Columns
- **date, name, business, type, area** : who and where. Type: salon, nail, lash/brow, barber, med spa, clinic, groomer, driving school, other.
- **segment** : "salon" (small, low ticket) or "higher-ticket".
- **channel** : in person, WhatsApp, phone.
- **role** : owner, chair renter, manager, receptionist.
- **top_pain_words** : their exact words for the biggest frustration.
- **pain_category** : no-shows, lost after-hours messages, getting new clients, costs, staff, software, other.
- **tried_before** : what they already tried (app, agency, nothing) and what happened.
- **rand_per_lost_slot** : what one empty appointment costs them, in rand.
- **lost_slots_per_month** : their guess, or ours from what they said.
- **current_spend_rand_pm** : what they pay now for software or staff to handle bookings, per month.
- **decision_maker** : yes / no. Can they say yes to a monthly fee today?
- **would_pay** : none / R100-R300 / R300-R500 / R500-R1000 / R1000+, only if they said or hinted at it. Never ask us to guess.
- **next_step** : what they agreed to, if anything.
- **quote_to_keep** : one sentence we could use word for word in the pitch.

## Scores (0 to 3 each, judged on what they said, not on what we hope)
- **pain** : 0 none named. 1 mild annoyance. 2 clear and recurring. 3 costs them money or sleep and they raised it unprompted.
- **cost_visible** : 0 cannot say. 1 vague. 2 gave a rand or hours figure. 3 gave both and knows it is rising.
- **can_pay** : 0 no budget. 1 tight. 2 comfortable at R300-R500. 3 comfortable above R1,000.
- **fit** : 0 we cannot fix it. 1 partly. 2 mostly (reminders, replies, rebooking). 3 exactly what they described.
- **access** : 0 no way back to them. 1 hard to reach. 2 will chat on WhatsApp. 3 offered a follow-up.

**total** = pain + cost_visible + can_pay + fit + access (maximum 15). Added by the sheet's formula column.

## How to read it after 20 conversations
- Average total by segment. The higher group is where we focus.
- Look at pain_category counts. If one category is 3 or more owners, that is the problem sentence.
- Look at rand_per_lost_slot times lost_slots_per_month. That is the monthly money at stake, and it decides the price: aim to charge about one fifth of it.
- Anyone with total 11 or more and decision_maker = yes is a first founding client. Reach out again within 48 hours with a quantified quick win, not a brochure.
- Anyone below 6 is not our customer right now. Thank them and move on.
- Review every Sunday. Change the messages if fewer than 1 in 5 reply.
