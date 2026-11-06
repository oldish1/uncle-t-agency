# Rex go-live checklist (6 Nov 2026)

Rex today: running in Make (scenario 7638753) on Meta's **test number**. You cannot message that number from a normal phone, and the test setup only answers your number. To be a real chief of staff he needs his **own number** (the SIM 063 647 6860) on a verified Meta business, plus the new brain in this folder.

What is ready (done by Claude): new brain in `system-prompt.md`, a clean copy-paste Make blueprint with no secrets in `make-blueprint.json` ("Rex - Commander Agent v2").

## Part A: you, today (10 minutes, needs no one else)

1. **Rotate the Rex Anthropic key.** console.anthropic.com, API keys, create a new key named "Rex v2", then revoke the old key named "Rex". Do NOT touch the key named "Uncle Ts Automation". Keep the new key in your password manager. Never paste it in chat.
2. **Make a new WhatsApp token.** Meta Business Settings, System users, your Rexbot user, Generate token for the Rex app, permissions whatsapp_business_messaging and whatsapp_business_management. Keep it safe. Never paste it in chat.
3. **Activate the SIM** 063 647 6860. Keep it in a phone that can receive an SMS or call for the Meta code.

## Part B: when the other session says Meta verification passed

1. In Meta, WhatsApp Manager, Phone numbers, **Add phone number**. Enter 063 647 6860 (+27 63 647 6860), display name "Rex". Meta sends a code by SMS or call to that SIM.
2. Copy the new **Phone Number ID**.
3. If Meta asks for registration, register the number with a six digit PIN you choose and keep.

## Part C: connect Rex v2 in Make (15 minutes)

1. Make, Create a new scenario, three dots, **Import Blueprint**, choose `make-blueprint.json` from this folder.
2. In the first module, add a **new webhook** and copy its URL.
3. Open the Claude module (number 2), Headers, replace `PASTE_ANTHROPIC_API_KEY_HERE` with the new key. In the router filter replace `PASTE_VERIFY_TOKEN_HERE` with a made-up word you also use in Meta (for example rex-and-a-random-string).
4. Open the WhatsApp module (number 3), replace `PASTE_REX_PHONE_NUMBER_ID_HERE` in the URL and `PASTE_WHATSAPP_ACCESS_TOKEN_HERE` in the header.
5. Do not edit the module settings in Make's editor beyond pasting those values. Make's editor saves some numbers as text and breaks the Claude call. If something looks wrong, tell Claude and it will fix it through the API.
6. Turn the scenario on. Turn the old "Rex - Commander Agent" scenario off.

## Part D: point Meta at Rex v2

1. Meta app, WhatsApp, Configuration, Webhook: Callback URL is the new webhook URL from Part C, Verify token is the word you chose. Click Verify and save.
2. Subscribe to the **messages** field.
3. Make sure Rex's number is the one connected to that app. Do not point the live Chales number at this webhook (that would break Lexi).

## Part E: test

Message Rex from your own phone: "Rex, who are you and what can you do?" He should answer in a few seconds. Then "what does Lexi cost?" (R499 a month, R1,499 setup). Then ask for something he cannot do, such as today's reply count, and check he says so plainly.

## Next upgrade (Rex v2.1), after he is live

1. Read the Pipeline Sheet so he can answer "who needs a follow-up today?" from real data.
2. A Tasks tab: you tell Rex "website agent, build X", he writes a row, and the agents pick it up on their schedules.
3. Memory: last few messages stored in a Sheet tab.

## What Rex will never do

Message a prospect, send anything to a client, spend money, or publish, without your yes. First messages to salons stay with you, from your own number.
