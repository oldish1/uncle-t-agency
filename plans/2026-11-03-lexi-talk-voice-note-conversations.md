# Plan: Lexi Talk, a two-way voice note conversation on WhatsApp

Date: 3 Nov 2026. Status: draft for Theo. Replaces the phone call as the first voice product. The phone call plan (`plans/2026-09-27-lexi-voice-receptionist.md`) stays as a later rung.

## The idea
The client chooses how to talk to Lexi: **tap** (the buttons and lists Lexi has now) or **talk**. In talk mode the client sends a voice note and Lexi answers with a voice note, in English or Afrikaans (isiZulu possible), back and forth like a normal WhatsApp chat with a person. The booking, calendar, sheet, reminders, cancel and membership logic stay exactly as they are.

## Is it possible? Yes, checked against Meta's own docs
- WhatsApp Cloud API can send a real voice message: an OGG file with the Opus codec, mono, sent with `"voice": true`. It shows on the client's phone as a voice note with the play button and our profile picture.
- The play button only appears if the file is 512 KB or smaller. Keep replies short (under about 60 seconds) and encode small.
- Lexi already receives voice notes and transcribes them (fix12, verified live 25 Sept).
- The missing piece is text-to-speech: turn Lexi's reply text into an Opus audio file, upload it to Meta, send it.
- Voices that speak our languages exist. Azure neural voices: Afrikaans (Adri, Willem), South African English (Leah, Luke) and isiZulu (Thando, Themba). OpenAI text-to-speech can also output Opus directly. I could not hear them from here, so quality in Afrikaans is the first thing to test.
- Not yet verified by us: that the file from either service plays correctly as a WhatsApp voice note (mono Opus is the usual trap), and how Make handles the upload.

## Does anyone else do it?
- **Blyssbook** has a switch, "reply to voice notes with a voice note", on its paid plans. It works only for short answers with no link in them, otherwise it replies in text. Its pitch and templates are English, Arabic and Spanish.
- **Omni24** (South African) understands voice notes in Afrikaans, isiZulu and isiXhosa, but its pages show it answering in text. It sells to larger firms (support, claims, onboarding).
- **Others** (Chatty, Booklink, Instantreply, Hustlery) read voice notes at most and reply in text.
- I did not find a South African salon or trades tool that holds a full voice back-and-forth on WhatsApp in Afrikaans for bookings. That is a gap, but one thin search is not proof. Check it with competitors' demo lines when we build the demo.

## What it costs us
| Step | Cost |
|---|---|
| Transcribe the client's voice note (gpt-4o-mini-transcribe) | about R0.05 a minute |
| Lexi's AI reading and replying | about R0.30 to R0.60 per turn (estimate) |
| Text to speech (Azure or OpenAI, about $15 per million characters) | a 300 character reply is under R0.10 |
| Meta, reply inside the 24 hour window | free |
| A whole booking by voice, about 6 turns | roughly R2 to R4 (estimate) |

Compared with a live phone call at R8 to R12 for a 3 minute booking, voice notes cost about a quarter and need no phone number, no Meta calling approval and no telephony.

## Why it fits our customers
- South Africans send voice notes all day. A stylist with wet hands, a plumber under a sink and a gogo who hates typing can all speak.
- It works in the chat they already use, with no app and no call.
- It answers the "cheap tools make the owner do the work" hole: the client does the talking and Lexi does the rest.
- It is a clean upgrade story for the website: Tap, Talk, then Call.

## Design rules (so it feels like a person, not a gimmick)
1. **Choice at the start:** "Tap the options below, or send me a voice note, whichever is easier." No forced mode.
2. **Mirror the client:** if their last message was a voice note, reply by voice. If they tap or type, reply in text. They can say "text please" or "voice please" any time.
3. **Voice for the conversation, text for the facts.** Always follow the final confirmation, prices, addresses, dates and times with a text message or the existing photo confirmation. People forget what they heard.
4. **Keep it short.** Under about 30 seconds a turn, one question at a time, same stage-by-stage flow as the WhatsApp prompt.
5. **Say what it is.** The welcome line says Lexi is the salon's AI assistant. The voice is clearly synthetic, so no pretending to be a person. OpenAI's own terms require telling users the voice is AI-generated.
6. **Fall back safely.** If transcription is unsure ("I did not catch that, could you say the date again, or tap one"), or the voice file fails, send text. Never leave the client without a reply.
7. **Under 20 seconds a turn** (the workspace rule for Lexi). A voice note in already takes about 14 seconds to a real reply (25 Sept). Voice out adds about 2 to 4 seconds. Measure it.

## Pricing ladder (draft, lock after the test)
| Tier | What the client gets | Price |
|---|---|---|
| Lexi Tap | Booking, reminders, cancel and reschedule on WhatsApp, voice notes understood | R1,499 once-off + R499/m (as now) |
| Lexi Talk | Everything above, plus Lexi replies by voice note, full back and forth, English and Afrikaans | + about R299/m, includes about 60 voice conversations, then about R5 each |
| Lexi Call | Live phone or WhatsApp calls answered | + about R799/m, later (see `2026-11-03-voice-edge-and-launch-plan.md`) |

At about R2 to R4 a voice booking, 60 conversations cost us roughly R120 to R240 a month, so R299 leaves a thin margin until we have real numbers. If the cost test comes in lower, we can include Talk in a R599 tier.

## Build and test steps

### Step 1: The ear test (half a day, almost free)
- Generate the same three Lexi replies in Azure Afrikaans (Adri), Azure South African English (Leah) and OpenAI, plus isiZulu (Thando) as a bonus. Use real lines: "Lovely, a wash and blowdry! Which day suits you?"
- Play them to Theo, Chanté and 3 salon owners. Ask: "Would you be fine getting this from a salon's assistant?" That is also a discovery question.
- Needs: an Azure Speech key (free tier, 0.5 million characters a month) or OpenAI's existing key from Make, and Theo to listen.

### Step 2: The delivery test (an hour)
- Send one test voice note through the Meta API from the demo number to Theo's phone: Opus, mono, under 512 KB, `"voice": true`.
- Pass if it shows the play button and plays clearly. If not, fix the encoding before anything else.

### Step 3: Build Lexi Talk on a copy
- Clone the template (`plans/client-template.md`), never the live Chales scenario. Add: voice-or-tap welcome line, mode memory per phone number, text-to-speech step after the reply is written, upload to Meta, send as a voice note, text fallback.
- Keep the Chales scenario (5043763) frozen at fix14 as decided on 25 Sept, until Talk is proven.

### Step 4: Test (20 conversations)
- Run at least 20 real conversations: 10 English, 10 Afrikaans or mixed, in noisy places, with real service names.
- Log accuracy of the booking, the time for each turn, and how it sounds in `reference/research/2026-11-03-lexi-talk-test-log.md`.
- Go if: 16 of 20 bookings correct, each turn under 20 seconds, Afrikaans voice judged acceptable by at least 3 listeners, cost per booking under R5.

### Step 5: Demo and offer
- Record the demo: a client sends a voice note, Lexi answers by voice, the booking lands, the photo confirmation arrives. This clip is the best advert we can make.
- Demo line: "Send a voice note and Lexi talks back." Put the same line on the website.

## Risks
- **Afrikaans voice quality.** Standard neural voices may sound stiff. Test first, and have a text fallback.
- **Pronouncing names and treatments.** "Nanoplastia", "Glowtox" and Xhosa or Afrikaans names may be read badly. Spell them phonetically in the voice text if needed.
- **Meta rules.** Audio replies inside the 24 hour window are fine. Business-started voice notes later than that need templates, so reminders stay text.
- **Privacy.** We store transcripts, not audio, unless a client needs it. Say so in the terms. POPIA applies.
- **Latency.** Make plus two extra API calls could pass 20 seconds. Measure on the first build.
- **Make's size limits.** Keep this as a separate, smaller scenario that is called by the template, as with the reminders.

## Questions for Theo
1. Is the OpenAI connection in Make ("OpenAI Lexi.", connection 11285759) the right key to use for text-to-speech, or do you prefer Azure's free tier?
2. Can you run the ear test with Chanté and two other salon owners this week?
3. Do you want Talk to replace the phone call as the first voice product? I recommend yes: cheaper, faster to build, and nobody else seems to have it.
