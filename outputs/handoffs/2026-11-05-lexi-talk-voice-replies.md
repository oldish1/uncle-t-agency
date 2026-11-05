# Handoff: build Lexi Talk (WhatsApp voice note replies)

Written 5 Nov 2026 for a fresh session that works only on this. Branch the earlier work is on: `claude/client-problem-discovery-3umz6b`.

## What we are doing and why
Theo wants Lexi to hold a real back-and-forth by WhatsApp voice note. The client chooses: tap (buttons and lists, as now) or talk (send a voice note, Lexi replies with a voice note). Plain version of the plan: Lexi Talk is the first voice product, ahead of live phone calls. Why it matters: it is a possible edge in South Africa (no local salon or trades tool found doing a full Afrikaans voice conversation for bookings), it costs about R2 to R4 per booking, and it works inside the WhatsApp chat clients already use. It also makes a strong demo for sceptical owners.

"Lexi 2.0" in Theo's words means the current Lexi product line. The old scenario literally named "Lexi 2.0 TEST" (7288450) was abandoned when Meta's webhook could not be re-verified. The live bot is "Chales Hair Boutique" (5043763).

## Where we got to
Done (research and plans only, no build):
- `plans/2026-11-03-lexi-talk-voice-note-conversations.md`: the full spec, design rules, cost, tier draft, 5-step test, risks. Read this first.
- `reference/research/2026-11-03-voice-market-and-costs.md`: competitor voice prices and cost per call.
- `plans/2026-11-03-voice-edge-and-launch-plan.md`: wider voice plan (demo, website tiers, content). Live phone calls are the later rung.
- `context/lexi.md` and `context/strategy.md` updated to say voice replies are back on.
Not started: the ear test, the delivery test, the build, the test log.

## Decisions made
1. Talk is the first voice product. Live calls (Retell or similar) come later.
2. Tap or talk, client's choice. Mirror the client: voice in gets voice out, tap or type gets text out. They can say "text please" or "voice please".
3. Voice for the conversation, text for the facts. Final confirmation (date, time, address, price) always goes as text or the existing photo confirmation.
4. Keep replies short, under about 30 seconds, one question at a time.
5. Lexi says it is an AI assistant. Always fall back to text if anything fails.
6. Do not touch the live Chales scenario (5043763). It stays frozen at fix14 until Talk passes its test. Build on a copy of the client template (`plans/client-template.md`).
7. Draft pricing: Lexi Tap R499/m (as now), Lexi Talk about +R299/m with about 60 voice conversations, Lexi Call about +R799/m later. Lock after real cost numbers.

## The facts the build depends on (verified from docs on 3 Nov, not yet by us)
- Meta WhatsApp Cloud API sends a voice message as an OGG file, Opus codec only, mono only, with `"voice": true`. If the file is over 512 KB, the play button is replaced by a download arrow. Wrong codec means it fails.
- Lexi already receives and transcribes voice notes (fix12, gpt-4o-mini-transcribe, OpenAI connection in Make "OpenAI Lexi." id 11285759, working live on 25 Sept, about 14 seconds from the note to Lexi's reply).
- Text to speech options: Azure neural voices (Afrikaans Adri and Willem, South African English Leah and Luke, isiZulu Thando and Themba, free tier 0.5 million characters a month, about $15 per million characters after) or OpenAI text to speech (about $15 per million characters, can output Opus). Not heard by us yet.
- Reply inside the 24 hour window is free from Meta. Reminders stay as text templates.
- Cost estimate per voice booking, about R2 to R4 (transcribe R0.05 a minute, AI R0.30 to R0.60 a turn, speech under R0.10 a reply). These are estimates.

## What to do next, in order
1. **Ear test.** Generate the same three Lexi lines with OpenAI text to speech first (several voices, in English and Afrikaans). Only add Azure Afrikaans and South African English voices if OpenAI sounds wrong. Real lines, for example "Lovely, a wash and blowdry! Which day suits you?". Theo plays them to Chanté and two salon owners and asks if it would be fine from a salon's assistant. Needs a key: Azure Speech free tier, or OpenAI's key via Theo. Keys live in `.env` and Make connections, never in the repo, and `.env` does not carry between sessions.
2. **Delivery test.** Send one Opus voice note via the Meta API from the demo number to Theo's phone. Pass only if it shows as a voice note with a play button. Check mono and size under 512 KB first.
3. **Build on a copy.** Clone the client template. Add: tap-or-talk welcome line, mode memory per phone number, text to speech after Lexi's reply is written, upload audio to Meta, send as voice note, text fallback. Keep it a separate or small addition, since the main scenario is about 146 modules and hits size limits when pushed whole.
4. **Test 20 real conversations** (10 English, 10 Afrikaans or mixed, noisy places, real service names). Log in `reference/research/2026-11-03-lexi-talk-test-log.md`. Go if 16 of 20 bookings are correct, each turn under 20 seconds, Afrikaans voice acceptable to at least 3 listeners, cost under R5 per booking.
5. **Demo.** Record a clip: voice note in, voice note out, booking lands, photo confirmation arrives. Update `context/lexi.md`, `context/numbers.md` with real cost, and the ledger as each step finishes.

## Gotchas
- **Make router rule (learned 25 Sept):** a router's fallback is stored by position. Never insert a route before existing ones, append and then check the "else" route still points at the same route. Fix15 broke name capture this way.
- **Make pushes:** a full blueprint of the live scenario is about 230K characters, too large to send in one call. Prefer small separate scenarios or Theo imports a file.
- **Make has no audio converter.** Get Opus directly from the speech API, or test an alternative.
- **Names at the name step must be typed.** Voice-to-text heard "Theo" as "Siyou". Do not ask for names by voice.
- **Pronunciation.** Treatments like "Nanoplastia" and "Glowtox" may be read badly. Try phonetic spelling in the voice text.
- **Chales services list** is in `context/lexi.md`. Chanté does not do braids, never use braids as an example.
- **Demo number** (076 492 4196, "Uncle T Demo") had an unresolved Meta webhook and a pending business verification in September. Check status before relying on it. Never test on Chanté's live number or data.
- **Apify and Supadata** hit usage limits on 3 to 5 Nov. Firecrawl worked. Network allow-list for any new host (api.openai.com, Azure) may need adding in the environment settings.
- **Privacy:** store transcripts, not audio. Tell clients Lexi is an AI. POPIA applies.

## Open questions for Theo
1. ~~Which key for speech?~~ Decided 5 Nov: start with OpenAI, using the existing Make connection "OpenAI Lexi." (id 11285759, confirmed present in Make on 5 Nov). Azure's free speech tier is the fallback only if the Afrikaans voice sounds too English in the ear test. Do not open an Azure account (needs a card) unless that happens. Estimated cost to reach a go/no-go: under about R50, and about R1 extra per voice booking per client.
2. Can he run the ear test with Chanté and two salon owners this week?
3. Is the demo number's verification finished?

## Not part of this session
The customer discovery and selling work is separate and continues alongside: `plans/2026-11-02-client-problem-discovery.md`, `outputs/discovery/` (pain scan, competitor holes, outreach messages, higher-ticket messages, scorecard, Theo's memorizable script). Facebook group plan, the Chales reactivation proof (needs Chanté's yes) and the website next week are also separate threads.
