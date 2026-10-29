---
name: outreach-writer
description: >
  Drafts personal WhatsApp outreach messages for Uncle T Agency's pipeline. Use when Theo says "draft 5
  outreach messages", "today's 5", "write messages for these salons", "outreach", "who do I message today".
  Reads leads from the Uncle T Pipeline Google Sheet, writes one message per business using only true facts
  from its listing, saves drafts to the Messages tab, marks the leads drafted, and returns tap-to-send links.
---

# Outreach Writer

Sheet: "Uncle T Pipeline" (id in `apps/agents/sheet-schema.md`). Read it with the Google Sheets connector (`get_spreadsheet`, `update_values`, `append_values`). Daily limit: 5 new conversations.

## Pick the leads
0. Before drafting for any lead, run the booking check: `uv run python scripts/booking_check.py "<business>" <suburb>`. Google's website field is often empty even when a salon already has a Fresha, Setmore or Booksy page (found 25 Oct: 12 of 24 Parow leads did). If a booking page turns up, set status `has booking page` and skip it for the Lexi pitch. Put the URL in the booking_hint column. Wait 3 to 4 seconds between searches to avoid rate limits.
1. Leads tab: status `new`, channel `whatsapp`, tier starting `A`, sorted by reviews (highest first). If fewer than the number asked, fall back to tier B, then say so.
2. Skip anyone with status `opted_out`, `sent`, `lost`.

## Write each message (the rules)
- 50 to 75 words. Plain Cape Town English, Theo's voice. Max one emoji, and zero is better.
- Greeting uses the business name. Never invent an owner's name, years in business, clients or results.
- Use ONE true detail from `real_detail` (stars, review count, share of 5-star, Saturday hours). Rephrase it like a person, don't paste the sheet text.
- One sentence on what Lexi does: clients book on WhatsApp while the owner is busy with someone in the chair. Say a local salon uses it (CHALES is true). No prices in the first message.
- End with one easy question about THEM (for example whether Saturday bookings come through WhatsApp), plus a short opt-out: "If it's not for you, no problem at all. Just let me know and I won't message again." (softened 26 Oct, keep the opt-out but never the blunt wording)
- Banned: "I hope you're doing well", "valuable time", "imagine", "game-changer", "revolutionize", "leverage", "streamline", "solution", exclamation chains.
- Each message must differ in opening and detail. If two read alike, rewrite one.
- A walk-in or call lead gets a 2-line spoken opener instead (use `outputs/2026-09-27-lexi-walkin-pitch.md`).

## Save
- Messages tab row: lead_id, business, channel, draft, wa_link, created (today), sent_on (blank), status `drafted`.
- wa_link = `https://wa.me/<wa_number>?text=<url-encoded draft>`.
- Leads tab: set status to `drafted`.
- Give Theo the drafts plus links. He attaches the Lexi video in WhatsApp (the typed text normally becomes the caption), sends, then says "sent <name>" so the lead is marked `sent` with next_action_date 3 days out.

## Rules
- Theo sends every message himself, from his own phone. Never automate first contact.
- Any reply that says no, stop, not interested: set status `opted_out` and never draft for that lead again.
- Not legal advice: remind Theo to have the POPIA direct-marketing rules checked before raising volume above 5 a day.

## Name the proof client (29 Oct 2026)

The attached demo video shows Lexi working for CHALES Hair Boutique in Bellville. Say so in the message: "I built a WhatsApp assistant for CHALES Hair Boutique in Bellville that handles bookings while the owner is with a client. Video attached." Do not say "a local salon". Chante must be happy to be named. Stop naming her if she says otherwise.

## Follow-ups (from reference/research/2026-10-29-what-gets-replies.md)

- No reply: one follow-up on day 3 and one on about day 10, then stop. Each under 50 words, with one new fact. Never "just checking in".
- Day 3 example: "Hi [name], Theo again. In case the video got buried: Lexi answers your WhatsApp bookings while you're with a client. Flat R499 a month, no commission on any client, first month free. Worth a quick look? If not, no problem at all."
- Say the needle as fact: flat price, no commission, clients stay in their own WhatsApp. Never name or attack a competitor.
- Bulk sending Tuesday to Thursday, 9 to 11 am.
