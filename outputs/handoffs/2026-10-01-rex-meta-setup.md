# Handoff: Rex, the agent system, and the Meta setup

Written 2026-10-01. Branch: `claude/rex-commander-agent-d2ak3z`.

## What we were working on and why

Theo wants a team of AI agents that win Uncle T Agency clients: Scout (finds prospects and competitor gaps), Content, Strategist, Outreach, and later a personal assistant. All of them answer to **Rex**, the Commander Agent, and Rex answers to Theo on WhatsApp. Only Rex needs a WhatsApp number. The other agents run as separate Make scenarios that Rex calls and reads back from.

## Where we got to

**Done**
- Rex's system prompt: `apps/rex/system-prompt.md`.
- Rex's Make scenario built: "Rex - Commander Agent", scenario **7638753**, currently OFF. Dedicated webhook (hook 3793690); its URL is on Make's Webhooks page and is not stored in this repo, because it works like a password. Flow: webhook, Claude API, WhatsApp reply, Google Sheets log. Sheet: "Rex Conversation Log" (Theo's Drive).
- Repo copy of the blueprint and a README in `apps/rex/`. Pushed.

**In progress**
- The Meta setup for Rex's own WhatsApp number (see "What to do next").
- Adding the Supadata and Firecrawl keys to the cloud environment so cloud sessions can pull YouTube transcripts and research the web.

**Not started**
- Rex's inbound path (blocked on the Meta setup).
- The other agents. Build order: Scout first, then Content/Strategist/Outreach, then the personal assistant last.
- Pulling the Nate Herk video transcript: `https://youtu.be/4hKJ9X6rGFo`. Theo wants an honest read on how real the "Grok bot" claims are.

## Decisions made

1. **Rex is fully isolated from Lexi and Chales.** No relay through the live Chales scenario (5043763). Two auto-mode safety checks blocked even the prep work, correctly: that scenario is booking real clients. Do not edit it.
2. **One general "Uncle T Agents" Meta App/WABA for all future agents**, set up once under the existing verified Business Portfolio ("Uncle Ts Automation"), so no new business verification.
3. **Start on Meta's free test number**, then migrate to a real SIM number later by swapping the Phone Number ID and token in Make. Test mode only sends to up to 5 pre-verified recipients, which is fine (just Theo).
4. **Outreach agents draft, humans send.** No cold WhatsApp messages from the business number, as Meta bans numbers for that, and that would kill Rex too.
5. **The personal assistant finds, compares and prepares; Theo approves before any money moves.** Suggested virtual card with a spend limit.
6. **Skip the community "WhatsApp MCP"** from Instagram: unofficial, bans risk on Theo's personal number, laptop-only, prompt-injection risk. Revisit only for the personal assistant, read-only first.
7. **Corrected a stale ID:** the brief gave Chales' WhatsApp Phone Number ID as 1170555039465381, but the live Chales scenario uses **1197696726762690**. Rex's scenario uses the live one.

## What to do next, in order

1. **Ask Theo whether the "Uncle T Agents" Meta app exists yet.** Guided step 1 was: developers.facebook.com/apps, Create App, "Other", type Business, name "Uncle T Agents", link to the existing verified portfolio.
2. Guide the rest, one step at a time (Theo clicks, Claude can't use Meta's UI or receive OTPs): add the WhatsApp product (Meta provides a test number, Phone Number ID and temporary token); add Theo's personal WhatsApp number as a test recipient and verify by OTP; create a **permanent** System User access token; under WhatsApp > Configuration set the webhook to Rex's URL (from Make) and subscribe to `messages`. Meta will also ask for a verify token, so agree one with Theo.
3. Theo gives Claude the **Phone Number ID**. The **token goes only into Make's header field, never into chat**.
4. Update Rex's scenario: module 3's URL (phone number ID) and the `Authorization` header; module 2's `x-api-key` still says `PASTE_ANTHROPIC_API_KEY_HERE`. The trigger must now accept Meta's webhook shape (`entry[].changes[].value.messages[]`), including the hub_mode/hub_challenge verification request, instead of the flat test payload. Then turn the scenario on and test.
5. Pull the Nate Herk transcript (needs the cloud environment keys, below) and give Theo an honest read.
6. Then `/explore` the full agent lineup and build order, and start with Scout.

## Gotchas

- **Rex's old webhook URL is in this public repo's git history** (an earlier README commit). Before turning Rex on, create a brand-new webhook in Make (or add API-key authentication to it), point the scenario at that, delete the old hook, and never commit the new URL.

- **Keys exposed in chat.** Theo shared screenshots that showed his Firecrawl key and Apify token in plain text. Treat both as exposed: generate fresh ones, store them in the cloud environment's **API credentials** (not the plain "Environment variables" box, which is visible to anyone using the environment), delete the two old lines. Never write key values into this repo; it is **public**.
- **Cloud environment setup.** Settings > API credentials > Add credential has: Name, Credential type (defaults to Bearer), Allowed websites, and Custom headers (Name / Prefix / Value). Firecrawl: allowed site `api.firecrawl.dev`, header `Authorization`, prefix `Bearer`. Apify: `api.apify.com`, same. **Supadata uses `x-api-key` with no prefix**: allowed site `api.supadata.ai`, header name `x-api-key`, leave Prefix empty. Allowed domains (network access) must also include `api.supadata.ai`. A new session is needed after saving.
- The workspace scripts (`scripts/utils/supadata.py`, `scripts/firecrawl_tool.py`) read the key from an environment variable. With hidden credentials they may report the key missing; if so, fix the scripts rather than exposing the key.
- YouTube itself is blocked from cloud sessions; Supadata is the route.
- Make's `scenarios_update` replaces the whole blueprint, so always fetch current first. Router fallbacks are stored by position: append routes, never insert (see `context/lexi.md`).
- The auto-mode checks block copying live keys between scenarios and reading production client executions. Don't work around them; ask Theo.
- Theo is moving house and checks in from his phone; keep replies short and plain, step by step.
