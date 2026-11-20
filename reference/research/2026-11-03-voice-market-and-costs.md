# Voice in South Africa: who sells it, what it costs us, what we can charge

Date: 3 Nov 2026. Updates `2026-09-25-lexi-voice.md`. Sources: WhichVoIP SA comparison (updated Oct 2026), BizAI, Agent Help, Retell, Vapi, ElevenLabs and OpenAI pricing pages, Hustlery, ai-360, Manano, ChatAvocado. Rand figures at about R18 to the US dollar. Vendor pages are marketing: prices are what they publish, claims are what they claim.

## 1. Does the competition have voice? Yes, a lot of it.

| Provider | Entry price | Minutes included | After that | Setup |
|---|---|---|---|---|
| SME Advantage | R849/m | none | about R8.50 to R10.50/min all-in | done-for-you from R6,950 |
| BizAI Voice Valet | R999/m add-on (R1,998 total on a base plan) | 100 | on request | assisted R850/hour |
| Remi Lite | R1,900/m | 500 | R1.85/min | none |
| AiSky Professional | R1,999/m (R2,399 month to month) | 250 once only | R0.97/min | none |
| Agent Help Starter | R1,999/m ex VAT | 150 | R13/min | none |
| Le Roux Digital | R1,450/m | not published | not published | R3,950, 3-month minimum |
| AI Automated Solutions | R5,000/m | not published | per build | not published |
| Aiployee | R7,500/m ex VAT | unlimited, one call at a time | telephony extra | R5,000 |

Also in the same space: Blyssbook (AI that answers WhatsApp and replies to voice notes with a voice note, plus an AI phone receptionist on its top plan, beta), Hustlery (missed-call text-back for trades), ai-360 (quote on phone, invoice on site, AI missed-call receptionist for plumbers and electricians).

What this means: voice on its own is not a gap. Eight or more local providers already sell it, several aimed at trades, and Agent Help gives away a demo number so owners can hear it. Their entry prices (R1,450 to R2,000 a month) are the benchmark an owner will compare us with.

## 2. What it costs us

| Item | Cost | Source |
|---|---|---|
| Live call agent, all-in (AI brain, speech, voice, platform) | about $0.13 to $0.15/min, range $0.07 to $0.31 | Retell published rates, Vapi, ElevenLabs |
| In rand | about R2.40 to R2.70/min, plan on R3 to R4 | |
| A typical 3-minute booking call | about R8 to R12 | |
| Client-initiated WhatsApp call | free from Meta | Meta calling pricing |
| Ordinary phone call route (SA number, call divert) | number about R18 to R72/m plus under R1/call; needs a Cape Town address and ID, about 2 days | Twilio, Telnyx |
| Voice note transcription (what Lexi already does) | $0.003/min with gpt-4o-mini-transcribe, about R0.05/min | OpenAI |
| A 45 second voice note start to finish | well under R1 including the AI reply | |
| Browser "Talk to Lexi" demo button on the website | same as a call, R3 to R4/min, needs a spend cap | |

Notes: Retell gives $10 free credit (about 70 to 90 minutes). Vapi gives $5. ElevenLabs lists $0.08 a minute on top of included minutes. None of these has been tested by us on Cape Town accents or Afrikaans names yet, and Meta's calling switch on the demo number depends on the demo number's business verification, which was still unresolved in September.

## 3. What we can charge (draft, lock after the cost test)

Assume 100 included minutes costs us R300 to R400.

| Tier | Price | Our cost | Comparison |
|---|---|---|---|
| Lexi (chat, reminders, voice notes) | R1,499 once-off + R499/m | existing | Booklink R79, Blyssbook R184 to R818, Chatty not shown |
| Lexi Voice (adds live calls) | + R799/m with 100 minutes, then R6/min. Setup R1,500 | about R300 to R400 | BizAI R1,998 total, AiSky R1,999, Agent Help R1,999 |
| Lexi Trade (voice note to quote PDF, missed-call answering) | hypothesis only: R1,499/m, setup R2,500. Not built | to be costed | ai-360, Hustlery, Agent Help |

Lexi plus Voice is R1,298 a month, below every published voice receptionist that includes minutes. Remi at R1,900 for 500 minutes is cheaper per minute for heavy callers, so we should not compete on volume.

## 4. Where voice actually matters

- **Hair salons and beauty:** clients already message on WhatsApp. Voice notes and typing cover most of it. A live call agent is a nice extra, not the main reason to buy. A missed call costs about one service (R150 to R450).
- **Plumbers, electricians, builders, installers:** hands full, on a ladder or under a sink, callers phone instead of WhatsApp, a missed call can be a R3,000 job or more. Agent Help claims 3 to 5 missed calls a day for trades (their number, a vendor claim, not verified). Voice is a much stronger fit here.
- **Clinics, dentists, vets, groomers, driving schools:** receptionist time is the cost, calls come in while staff are with someone.

## 5. The voice-note-to-quote idea

You mentioned construction workers sending a voice note that comes out as a PDF. I did not find it in the workspace notes, so I am treating it as your idea. Related products exist: Manano (UK and Ireland, WhatsApp voice note to quote and invoice with deposit), ChatAvocado (Singapore, technician messages produce a service report and invoice PDF), ai-360 (SA, quote and invoice on the phone, not voice-first). I did not find an SA product that does WhatsApp voice note to quote PDF for trades, but I did not search exhaustively. Lexi already transcribes voice notes, so the front half exists. The missing half is turning the transcript into a quote PDF with the owner's rates, logo and numbering, and sending it to the customer.

## 6. Risks to test before promising anything
1. Does speech recognition handle Cape Town English, Afrikaans, and mixed sentences? WhichVoIP says performance drops on heavy accents and code-switching.
2. Delay: US-hosted platforms may leave long pauses for callers in Cape Town.
3. Meta WhatsApp Calling on the demo number: needs the number's verification sorted.
4. POPIA: recording calls needs a short disclosure and a clear policy on where recordings live.
5. Abuse of a public demo line: cap minutes and spend.
