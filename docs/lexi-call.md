# Lexi Call (phone receptionist for Chales, on Bland)

Built 18 Nov 2026 from Jason Cooperson's MIT-licensed Bland template (github.com/jasonc00person/bland-ai-receptionist). Lives in `apps/lexi-call/`. Research: `reference/research/2026-11-18-bland-receptionist-template.md`.

## What it is now
- A Bland v2 agent, "Chales Hair Boutique Receptionist" (agent id `5809a051-cd8a-4315-893f-2971511985e2`), in Theo's Bland account ("theo's Personal Org"). No phone number attached yet, so nobody can call it.
- Call flow: Greeting, Capture Treatment, Offer Availability, Caller Name, Wrap Up (reads the booking back), Confirm And End (hangs up). AI Disclosure is global: always admits it is an AI and offers Chanté. Transfer goes to Chanté (+27 81 433 2756, in `config.json`).
- Open times are TEST SLOTS written into `prompts/_global.md` (Thursday 10:00 and 14:00, Saturday 09:00 and 11:30). No calendar is connected and nothing is booked.
- Jason's SMS step was removed: texting needs a Bland number, and the confirmation will come from Lexi on WhatsApp instead.
- English and Afrikaans, Cape Town tone, no braids or relaxers, never invents prices.

## How to change and test it
- Edit `apps/lexi-call/prompts/*.md`, then `BLAND_API_KEY=proxy-injected python3 scripts/setup.py --update` from `apps/lexi-call`.
- Text test calls (free, no number needed): `BLAND_API_KEY=proxy-injected python3 scripts/simulate.py tests/<name>.json`. Callers: happy_path, service_first (name given early), rude_caller (asks if AI, asks for braids and price), afrikaans.
- In a cloud session the Bland key is a proxy-injected network secret on api.bland.ai (saved 18 Nov), and `stream-v2.aws.dc8.bland.ai` is on the allowed hosts for the test chat. `scripts/agents.py` was changed to tunnel the test chat through HTTPS_PROXY when one is set.
- `.bland-state.json` (agent id) and `config.json` are git-ignored. If they are missing in a new session, recreate config from `config.example.json` and the state file as {"agent_id": "5809a051-cd8a-4315-893f-2971511985e2", "uploaded": true}.

## Status and known issues (18 Nov)
- Last round: 3 of 6 test calls hung up on their own. Every step works, but near the end Bland's routing sometimes loops back ("that's under Fatima, right?") or restarts the greeting. Next fix to try: fewer steps (merge Caller Name into Offer Availability), and stricter Wrap Up and exit wording. Go rule: 3 clean passes in a row for every test caller.
- Fixed: Afrikaans half hours ("half twaalf" for 11:30, never "half elf"), not asking for a name twice, no spoken stage directions, Afrikaans goodbyes end the call.

## Next steps
1. Stabilise the ending (above).
2. Live calendar: a Bland webhook step calls a small Make scenario that returns real open slots (demo calendar first, never Chanté's until proven), and a second one writes the booking.
3. Confirmation by WhatsApp through Lexi.
4. Theo hears it: browser test call in Bland's dashboard, then a South African number and call divert.
