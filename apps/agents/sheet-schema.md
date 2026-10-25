# Uncle T Pipeline: sheet schema

Google Sheet "Uncle T Pipeline" in Theo's Drive (private, shared with nobody). Spreadsheet id: `1H3pqX4Nr5XvgqTeOd0UFialpX8P7zGzpMGx1Fkt2gc8`.

## Leads
id, date_found, vertical, business, suburb, phone, wa_number, channel, rating, reviews, real_detail, website, instagram, tier, status, next_action_date, notes

- `wa_number`: SA mobile as digits with 27 (empty for landlines). `channel`: `whatsapp` when there is a mobile number, otherwise `walk-in or call`.
- `real_detail`: one checkable fact from the public Google listing (stars, review count, share of 5-star, category, Saturday hours). The Writer may use only this, never invent.
- `tier`: A no website, B website of some kind (Facebook, mall directory and WhatsApp catalog pages are noted), C has a booking system.
- `status`: new, drafted, sent, replied, call, won, lost, opted_out. Anyone who opts out is never contacted again.

## Messages
lead_id, business, channel, draft, wa_link, created, sent_on, status

## Replies
lead_id, business, reply_text, intent, draft_answer, date, handled

## Weekly
week_start, found, drafted, sent, replies, calls, won, notes
