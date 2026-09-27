# Rex — the Commander Agent

Rex is Theo's WhatsApp ops assistant. He's not customer-facing (that's Lexi's job) — Rex is who Theo texts to ask about the business, the pipeline, or what's going on with a client, and gets a sharp, direct answer back on WhatsApp.

Flow: **Test message in → Make.com webhook → Claude API → WhatsApp reply → logged to Google Sheets.**

**Status: built and live in Make, scenario ID 7638753, currently OFF.** Two secrets are still placeholders — see "The two things only Theo can do" below. Everything else is wired and ready.

## Files here

- `system-prompt.md` — who Rex is, what he knows, how he talks. This is the source of truth; the Make scenario carries a live copy of it in module 2's `system` field. Edit this file first, then paste the change into the scenario.
- `make-blueprint.json` — a copy of the actual blueprint now sitting in Make (scenario 7638753), for the repo's record and so it can be re-imported if the scenario is ever lost. The two credential fields are placeholders in this file on purpose — never real keys, since this repo is public.

## What's actually built in Make

1. **Custom Webhook** ("Rex WhatsApp In", hook 3793690) — `https://hook.eu1.make.com/uumfpgalfefvmi29orokmffsocq3x5ww`. Expects a flat JSON body: `{"from": "...", "text": "...", "message_id": "..."}`.
2. **HTTP — Claude API call** — `POST https://api.anthropic.com/v1/messages`, model `claude-sonnet-4-6`, `max_tokens: 1024`. Uses Make's "Data structure" body input (reusing the same structure Lexi's own Claude calls use), which auto-escapes whatever Theo types — no manual escaping needed. No conversation history is threaded through yet; each message is a fresh call.
3. **HTTP — WhatsApp reply** — sends Claude's reply back to whoever texted in, as a plain WhatsApp text message.
4. **Google Sheets — log row** — one row per exchange in a new sheet, "Rex Conversation Log": timestamp, from-number, message in, Rex's reply, WhatsApp message ID.

## A real number correction made while building this

The task brief for Rex named Phone Number ID `1170555039465381` for Chales' WhatsApp number. Checked it against the live "Chales Hair Boutique" Make scenario (5043763) and that ID doesn't appear anywhere in it — the number actually in production use is **`1197696726762690`**. Rex's WhatsApp-send module uses the correct, verified live ID. Worth checking where the old ID came from, in case it's stale somewhere else too.

## Why Rex doesn't listen on Chales' real WhatsApp number

Meta only allows one webhook callback per Business App/number — this exact collision caused a real incident on 19 Sept (Theo's test messages briefly triggered Chante's live Lexi scenario; see `ledger/theo.md`). So Rex's trigger is its **own separate webhook**, not hooked into Chales' live Meta callback. Rex can *send* WhatsApp messages using Chales' number (outbound is unlimited), but nothing routes Theo's real WhatsApp texts to Rex's webhook yet.

To actually talk to Rex on WhatsApp, one more small piece is needed: something that takes Theo's incoming message on that number and also forwards it to Rex's webhook — the same pattern already used for the "Uncle T Demo - Verification Relay" scenario. That's a follow-up job, not done here, precisely to avoid touching the live Chales scenario without being asked.

## The two things only Theo can do (and only Theo)

Both credentials are real secrets — I won't put them in chat, in this repo, or in any file, because this repo is public. Theo pastes them directly into Make's UI, at these two spots:

1. Open scenario **"Rex - Commander Agent"** in Make → module 2 (Claude API call) → **Headers** → replace `PASTE_ANTHROPIC_API_KEY_HERE` with the real Anthropic API key (the same one the live Lexi scenario already uses, if he wants to reuse it, or a fresh one).
2. Same scenario → module 3 (WhatsApp reply) → **Headers** → replace `Bearer PASTE_WHATSAPP_ACCESS_TOKEN_HERE` with `Bearer <real WhatsApp access token>`.

Once both are pasted in, hit **Run once** to test with a manual webhook call (see below), then flip the scenario to **ON**.

## Testing it once the keys are in

POST a test payload straight to the webhook, e.g. from a terminal:

```
curl -X POST https://hook.eu1.make.com/uumfpgalfefvmi29orokmffsocq3x5ww \
  -H "Content-Type: application/json" \
  -d '{"from": "<your own WhatsApp number, no +>", "text": "Hey Rex, what does Lexi cost?", "message_id": "test-1"}'
```

If it's wired right, that WhatsApp number gets a reply from Rex within a few seconds, and a row lands in the "Rex Conversation Log" Google Sheet.

## Where the numbers live

Rex's business knowledge (pricing, clients, leads, stack) is baked into `system-prompt.md`, pulled from `context/business.md`, `context/lexi.md`, `context/offer.md`, and `context/numbers.md`. If any of those change — new client signs, pricing shifts, a lead converts — update `system-prompt.md` here and paste the refreshed system prompt into module 2 of the live scenario, or Rex starts giving stale answers.
