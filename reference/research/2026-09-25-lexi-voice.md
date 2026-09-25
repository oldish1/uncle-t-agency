# Lexi Voice: research (25 Sept 2026)

> Homework for the parked Lexi Voice idea (`context/ideas.md`). Answers the four open questions: SA numbers, Rand cost, accents, pricing. Done by web search only; several vendor sites were blocked from this session, so prices come from recent 2026 comparison pages and should be checked on the vendor's own page before quoting a client. Rand figures assume about R18 to the US dollar.

## The big finding: WhatsApp calls, not phone calls

WhatsApp now lets businesses receive voice calls through the same Cloud API Lexi already runs on (the WhatsApp Business Calling API). South Africa is in the supported countries.

- **Calls a client makes to the business are free.** Meta only charges for calls the business makes.
- The call can be passed to an AI voice agent over SIP (a standard way of connecting phone systems) or WebRTC (the browser version). Vapi and ElevenLabs are named as partners.
- It's the same number, the same Meta app and the same brain as Lexi on WhatsApp. A client who'd rather talk than type just taps the call button in the chat they already have open.
- **Catch:** the number reportedly needs to be on the 1,000-conversations messaging tier, and calling has to be switched on. Need to check which tier Chales' number is on.

This is the cheapest and best-fitting route, so it goes first.

## Route 2: ordinary phone calls

For clients who dial the salon's cell or landline.

- **Getting a number:** Bland has no numbers of its own anywhere. You bring your own from Twilio or any SIP provider. Vapi's own numbers are US and Canada only. So either way we'd buy a South African number from Twilio or Telnyx (about $1 to $4 a month, R18 to R72) and connect it.
- A local 021 number needs a real Cape Town street address (no PO Box) and ID documents. Twilio takes up to two business days to review them.
- **How calls reach it:** the salon keeps its own number and sets it to divert calls it misses or can't take to the AI's number. Codes are the same on Vodacom and MTN: `**61*<number>#` if unanswered, `**67*<number>#` if busy. Setup is free, but the salon pays a normal call rate for each diverted call.

## What a call costs us

A booking call runs about 3 minutes.

| Platform | Per minute | 3-minute call | Notes |
| --- | --- | --- | --- |
| Bland | $0.11 to $0.14 (plan dependent) | about R6 to R7.50 | AI, voice and transcription all included. $0.015 minimum on failed calls. Transfers to a human cost extra on Bland numbers, free with your own Twilio. |
| Vapi | $0.05 platform + parts, $0.10 to $0.30 all-in | about R5.50 to R16 | Cheapest start, most moving parts to set up |
| Retell | $0.07 + parts, about $0.13 all-in | about R7 | $10 free credit to test (roughly 70 to 90 minutes) |
| Twilio SA number (Route 2 only) | about $0.01 inbound | under R1 | Plus about $1 a month for the number |

On WhatsApp calling (route 1), only the AI platform charges. Meta's part is free for calls clients make.

**Rough monthly cost at a busy salon:** 100 booking calls a month is about R600 to R800 in AI minutes.

## Competition: this already exists in SA

**BizAI** (already on our competitor list) sells "Voice Valet": R999 a month ex-VAT, about 200 AI-answered minutes included, then R3.50 a minute. You divert your existing number to it, and it claims SA accents, WhatsApp integration and POPIA compliance (South Africa's data-privacy law). Other local options go up to about R3,500 a month (WhichVoIP). A human virtual receptionist costs R8,000 to R15,000 a month.

What that means for us:
- BizAI's R999 for 200 minutes costs about R500 in Bland minutes, so there's little margin in matching their price as a standalone product.
- Our edge isn't voice on its own. It's one Lexi across WhatsApp chat and calls, booking straight into the same calendar, with cancel, reschedule and reminders already working. Sell it as an upgrade to Lexi, not a separate receptionist.

## Accents and languages: still open

No platform publishes proof that it handles South African English well. ElevenLabs has Afrikaans voices and some African-accented English voices, but none sold as SA English. Most of these platforms run on US servers, which may add a noticeable delay on calls from Cape Town. The only real answer is a test: call it ourselves in local accents, with local service names (braids, relaxer, wash and blowdry), and time the pauses.

## Pricing thoughts (not decided)

- An add-on to the Lexi System, not a new product.
- BizAI's R999 is the local price to beat. At our cost of about R6 to R8 per booking call, an add-on around R500 to R900 a month with a sensible number of minutes included has room. Decide once we have real cost-per-call numbers from a test.
- The US demo's $2,000 build + $500 a month (about R36,000 + R9,000) is far too high for Cape Town salons.

## Recommended next steps (once the first paying client signs)

1. Check the Chales WhatsApp number's messaging tier and whether calling can be switched on.
2. Free test: Retell's $10 credit or a Vapi trial, connected to WhatsApp calling on the **demo number** (never Chanté's live number first). Theo calls it in Cape Town accents and times the replies.
3. If it passes, connect it to Lexi's existing booking steps (calendar check, booking, sheet).
4. Only then look at Route 2 (a 021 number plus call divert) for salons whose clients phone rather than WhatsApp.

## Sources

- Bland pricing: [getmacha.com](https://www.getmacha.com/blog/bland-ai-pricing-explained), [cloudtalk.io](https://www.cloudtalk.io/blog/bland-ai-pricing/), [bland.ai/pricing](https://www.bland.ai/pricing)
- Bland bring-your-own numbers: [docs.bland.ai](https://docs.bland.ai/tutorials/custom-twilio), [parloa.com](https://www.parloa.com/knowledge-hub/voice-ai-api-global-telephony/)
- Vapi: [cloudtalk.io](https://www.cloudtalk.io/blog/vapi-ai-pricing/), [lindy.ai](https://www.lindy.ai/blog/vapi-ai)
- Retell: [cekura.ai](https://www.cekura.ai/blogs/retell-ai-pricing-per-minute), [layer3labs.io](https://www.layer3labs.io/guides/retell-ai-pricing)
- Twilio SA: [twilio.com voice pricing ZA](https://www.twilio.com/en-us/voice/pricing/za), [twilio.com ZA regulatory](https://www.twilio.com/en-us/guidelines/za/regulatory)
- Telnyx SA numbers: [telnyx.com](https://telnyx.com/phone-numbers/south-africa)
- Call divert codes: [entrepreneurhubsa.co.za](https://entrepreneurhubsa.co.za/how-to-divert-calls-to-another-number-on-vodacom-mtn-telkom-cell-c/)
- WhatsApp Calling API: [Meta developer docs](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/pricing), [ycloud.com](https://www.ycloud.com/blog/whatsapp-calling-api-pricing-explained), [chakrahq.com](https://chakrahq.com/article/whatsapp-cloud-api-calling-feature-details), [3cx.com](https://www.3cx.com/docs/whatsapp-sip-calling-integration/)
- SA competitors: [bizai.co.za](https://www.bizai.co.za/blog/best-ai-receptionist-south-africa-2026), [whichvoip.co.za](https://whichvoip.co.za/phone-systems/ai-voice-agent/best-ai-voice-agents-south-africa/)
- ElevenLabs voices: [elevenlabs.io](https://elevenlabs.io/text-to-speech/afrikaans)
