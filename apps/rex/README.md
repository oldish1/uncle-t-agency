# Rex — the Commander Agent

Rex is Theo's WhatsApp ops assistant. He's not customer-facing (that's Lexi's job) — Rex is who Theo texts to ask about the business, the pipeline, or what's going on with a client, and gets a sharp, direct answer back on WhatsApp.

Flow: **WhatsApp message from Theo → Make.com webhook → Claude API → WhatsApp reply → logged to Google Sheets.**

## Files here

- `system-prompt.md` — who Rex is, what he knows, how he talks. This is the source of truth; the Make scenario just carries a copy of it. Edit this file first, then copy the change into the live scenario's Claude API module.
- `make-blueprint.json` — the Make.com scenario blueprint (5 modules: webhook in → Claude API → parse JSON → WhatsApp reply → Sheets log). It's a template, not a one-click import — see "What needs setting up by hand" below.

## The four modules

1. **Custom Webhook (trigger)** — receives the incoming WhatsApp message. Expects Theo's WhatsApp Business API payload to be pre-parsed (or parse it here) into at least: `from` (his WhatsApp number), `text` (message body), `wa_id`, `message_id`.
2. **HTTP — Claude API call** — `POST https://api.anthropic.com/v1/messages`, model `claude-sonnet-4-6`, headers `x-api-key`, `anthropic-version: 2023-06-01`, `content-type: application/json`. Body carries the Rex system prompt plus the incoming message as the one user turn. No conversation history is threaded through yet — each message is a fresh call. If Theo wants Rex to remember earlier turns in a session, that's the next iteration (pull recent rows from the logging sheet and fold them into the prompt).
3. **HTTP — WhatsApp reply** — `POST https://graph.facebook.com/v19.0/1170555039465381/messages` (Chales's WhatsApp Business API phone number ID — reused here since Uncle T Agency's own dedicated Rex number isn't set up yet), `Authorization: Bearer <WhatsApp access token>`, sends Claude's reply back as a plain text message to whoever messaged in.
4. **Google Sheets — log row** — one row per exchange: timestamp, from-number, message in, Rex's reply, WhatsApp message ID.

## What needs setting up by hand before this goes live

Make blueprints can't carry API keys or webhook IDs — those get created inside Make's UI, not in the JSON. Before this scenario can run:

1. **Create the Custom Webhook** in Make (Webhooks → Add → Custom webhook), point Theo's WhatsApp Business API's message webhook at the URL it gives you, and wire it into module 1.
2. **Add a connection for the Claude API key** (`ANTHROPIC_API_KEY`) — HTTP header-auth connection, used in module 2.
3. **Add a connection for the WhatsApp access token** (`WHATSAPP_ACCESS_TOKEN`) — HTTP header-auth connection, used in module 4.
4. **Paste the system prompt.** Copy the contents of `system-prompt.md` into module 2's `system` field as one JSON-escaped string.
5. **Pick or create the logging sheet**, and drop its spreadsheet ID and tab name into module 5.
6. **Connect Google Sheets** in Make if it isn't already connected in this account.

Once those five are done, activate the scenario and it's live.

## Where the numbers live

Rex's business knowledge (pricing, clients, leads, stack) is baked into `system-prompt.md`, pulled from `context/business.md`, `context/lexi.md`, `context/offer.md`, and `context/numbers.md`. If any of those change — new client signs, pricing shifts, a lead converts — update `system-prompt.md` here and push the refreshed text into the live Make scenario, or Rex starts giving stale answers.
