# Lexi voice notes: plan

Status: **ready to build.** Step 0 done 25 Sept: OpenAI connected in Make as "OpenAI Lexi." (connection 11285759), $5 prepaid, auto-reload off.

## The problem today

Lexi's live scenario ("Chales Hair Boutique", 5043763) only lets through text messages and button taps (module 2, filter "Has message text"). A voice note arrives as type `audio`, fails that filter, and **Lexi says nothing back.** A client who sends a voice note gets silence right now.

## What we're building

A client sends a voice note ("Hi, can I come in Saturday for a wash and blowdry?"). Lexi:
1. Replies straight away: "Got your voice note, give me a sec 🎧" (this covers the few seconds the transcription takes).
2. Turns the voice note into text.
3. Carries on exactly as if they'd typed it: same AI, same calendar check, same booking, cancel and reschedule.

## How (the trick that keeps it small)

Nothing in the existing 94 modules changes. A new route at the very front handles voice notes only:

1. **Router at the start.** Route A: `messages[].type` = `audio`. Route B: everything else, which is today's whole flow, untouched.
2. **Route A steps:**
   - Send the "give me a sec" reply (same HTTP send as module 240).
   - Ask Meta for the audio file's download link: `GET graph.facebook.com/v25.0/{audio.id}` with the same Bearer key.
   - Download the file from that link (same key).
   - Send it for transcription (OpenAI "Create a transcription", model whisper-1 or gpt-4o-mini-transcribe). Handles English and Afrikaans, including mixing the two.
   - **Re-post to Lexi's own webhook** a copy of the original Meta message, with `type` changed to `text` and `text.body` set to the transcript. Lexi then treats it as a typed message, so every existing branch just works.
3. **Fallback:** if transcription fails or comes back empty, reply "Sorry, I couldn't catch that voice note, could you type it for me?" Never silence.
4. **Log it:** add the transcript to the chat-history sheet marked as a voice note, so Chanté can see what was said.

## Cost and speed

- Transcription costs well under R0.10 per voice note (a 20-second note is a fraction of a cent in US dollars). Check the current OpenAI price before quoting.
- It adds roughly 3 to 5 seconds before Lexi's real answer. The instant "give me a sec" reply hides most of that.

## Step 0: what Theo needs to do

- Create an OpenAI API key (platform.openai.com) and load a small credit, about R100 is plenty for months. Claude can't make accounts or handle payment.
- Add it to Make as an OpenAI connection (Make, Connections, Add, OpenAI), so the key never needs to be pasted into chat.
- Alternative providers if preferred: Groq (cheaper and faster Whisper), Deepgram, ElevenLabs Scribe. Claude's own API can't take audio, so it has to be one of these.

## Testing

- Build it as a blueprint and import it into the live scenario, the way fix2 to fix11 were done.
- Test from Theo's number only: a short English note, a long note, an Afrikaans note, a note with background salon noise, a cancel request by voice, a silent or empty note.
- Measure the time from sending a note to Lexi's real reply. Target: under 10 seconds.

## Phase 2 (the extra wow, optional)

Lexi **replies** with a voice note too, using an SA-sounding voice (ElevenLabs). Costs more per message and adds a few seconds, so offer it as an option, not the default. Only once phase 1 is solid.

## Build notes (25 Sept)

- Builder: `scripts/lexi/build_voice_notes.py`. It takes the live "Chales Hair Boutique" blueprint and adds a router (301) in front. Route A (filter: message type = audio): 302 ack, 303 get media link, 304 download, 305 OpenAI transcription, 306 code step that rebuilds the Meta message as a text message, 307 router, 308 re-post to Lexi's own webhook, or 309 "please type it". Steps 303 to 305 fall back to the "please type it" reply (310 to 315) if they error. Route B is the whole existing flow, unchanged.
- The WhatsApp key is copied inside the script from module 240 and never printed. The finished import file goes to `private/` (git-ignored).
- Lexi runs sequentially, so the re-posted message is queued and handled straight after the voice-note run finishes. No deadlock.
- Tested: dry run with no duplicate IDs; the rebuild code tested with normal, empty and Afrikaans-with-quotes transcripts.
- Waiting on: exact OpenAI module config, copied from a "Voice note helper" scenario Theo saves.
- Transcription prompt (helps spell service names right): "Chales Hair Boutique, a hair salon in Cape Town. Services: Wash and Blowdry, Trim, Precision Cut, Root Touch Up, Full Color, Hair Colour and Highlights, Brazilian and Keratin, Nanoplastia, Botox and Glowtox, Basin Treatment. Clients book, cancel or reschedule appointments." Model: gpt-4o-mini-transcribe.
