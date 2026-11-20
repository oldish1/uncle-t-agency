# Lexi Call (phone receptionist for Chales, on Bland)

Built 18 Nov 2026 from Jason Cooperson's MIT-licensed Bland template (github.com/jasonc00person/bland-ai-receptionist). Lives in `apps/lexi-call/`. Research: `reference/research/2026-11-18-bland-receptionist-template.md`.

## What it is now
- A Bland v2 agent, "Chales Hair Boutique Receptionist" (agent id `5809a051-cd8a-4315-893f-2971511985e2`), in Theo's Bland account ("theo's Personal Org"). No phone number attached yet, so nobody can call it.
- Call flow: Greeting, Capture Treatment, Offer Availability, Caller Name, Wrap Up (reads the booking back), Confirm And End (hangs up). AI Disclosure is global: always admits it is an AI and offers Chanté. Transfer goes to Chanté (+27 81 433 2756, in `config.json`).
- Open times come live from the **"Lexi Call Test (demo bookings)"** Google Calendar in Theo's account (adamst70), and bookings are written back to it. Chanté's real calendar is not connected yet.
- Jason's SMS step was removed: texting needs a Bland number, and the confirmation will come from Lexi on WhatsApp instead.
- English and Afrikaans, Cape Town tone, no braids or relaxers, never invents prices.

## How to change and test it
- Edit `apps/lexi-call/prompts/*.md`, then `BLAND_API_KEY=proxy-injected python3 scripts/setup.py --update` from `apps/lexi-call`.
- Text test calls (free, no number needed): `BLAND_API_KEY=proxy-injected python3 scripts/simulate.py tests/<name>.json`. Callers: happy_path, service_first (name given early), rude_caller (asks if AI, asks for braids and price), afrikaans.
- In a cloud session the Bland key is a proxy-injected network secret on api.bland.ai (saved 18 Nov), and `stream-v2.aws.dc8.bland.ai` is on the allowed hosts for the test chat. `scripts/agents.py` was changed to tunnel the test chat through HTTPS_PROXY when one is set.
- `.bland-state.json` (agent id) and `config.json` are git-ignored. If they are missing in a new session, recreate config from `config.example.json` and the state file as {"agent_id": "5809a051-cd8a-4315-893f-2971511985e2", "uploaded": true}.

## Status and known issues (18 Nov, after the ending fix)
- Flow is now: Greeting, Capture Treatment, Offer Availability (time and name together), Wrap Up (reads back, asks "anything else?", says the goodbye), Confirm And End ("Bye bye!" and hang up).
- How Bland behaves: moving between steps inside the booking flow is instant, but leaving the flow to hang up always takes one more caller turn. So Lexi says goodbye, and the line drops when the caller says bye back. Designed around that rather than fighting it.
- The end-call step is set to always be picked (`alwaysPick: true` in `scripts/agents.py`), and the hub prompt lists Afrikaans goodbyes and says never restart the greeting. Bland's API does not show whether `alwaysPick` was kept.
- Test results after the fix: English callers 12 of 12 hung up cleanly (happy path, name given early, rude caller asking about AI, braids and price). Afrikaans caller 3 of the last 4. The occasional Afrikaans miss is the controller restarting the greeting after "Totsiens"; on a real call the caller would simply hang up.
- Fixed earlier: Afrikaans half hours ("half twaalf" for 11:30, never "half elf"), never asking for a name twice, no spoken stage directions.


## Calendar connection (built 19 Nov)
- Call flow now: Greeting, Capture Treatment, **Get Open Times** (webhook), Offer Availability (time and name), **Book In Calendar** (webhook), Wrap Up, Confirm And End.
- Make scenario **"Lexi Call - Availability (test calendar)"** (8667038, webhook 4135878): checks the test calendar's busy times (freeBusy) for the next 11 days and returns up to 3 free one-hour slots on each of the next 3 open days. Hours: weekdays on the hour 08:00 to 16:00, Saturday every half hour 08:00 to 16:30, Sunday closed, nothing sooner than 2 hours away. Returns `{"slots_text": "...", "count": n}`; each slot carries an id like 2026-11-20T10:00:00+02:00.
- Make scenario **"Lexi Call - Book (test calendar)"** (8667043, webhook 4135879): takes caller_name, treatment, slot_id, phone and creates a one-hour event "Lexi Call: <treatment> - <name>". Returns `{"booked": true}`. If booked is not true, Lexi says Chanté will confirm on WhatsApp instead of claiming it is booked.
- Both use Make's Google connection 5535950 (Theo, adamst70). Test calendar id: c242755dc2efac3073ffa5155130ac0788d62bf327b2cf0cb185c2b69f3bd32d@group.calendar.google.com. "Lexi Call - One-off: create test calendar" (8667026) is switched off and can be deleted.
- Make gotchas learned: the code step's field is `codeEditorJavascript` (not `code`), its results are read as `{{3.result.json}}` (not `{{3.json}}`), and the calendar step needs `parseDate(...)` around an ISO time. When the diary answer was empty, Lexi invented times, so the prompt now forbids making up times.
- Tests on 19 Nov: English callers 3 of 3 booked the time they picked and hung up; Afrikaans 3 of 3 after teaching the treatment step Afrikaans. 6 test events now sit in the test calendar (safe to clear).
- Known gap: the caller's phone number shows as {{from}} in test-chat bookings (typed tests have no number). Check it fills on the first real call.

## Before Chanté's real calendar
1. A real spoken test call (browser call in Bland, then a number).
2. Point both scenarios at Chanté's calendar with her Google connection, reading her real hours and treatment lengths (colour and keratin take longer than one hour).
3. Re-check a slot is still free just before booking (two callers at once).
4. WhatsApp confirmation through Lexi.

## Next steps
1. Stabilise the ending (above).
2. Live calendar: a Bland webhook step calls a small Make scenario that returns real open slots (demo calendar first, never Chanté's until proven), and a second one writes the booking.
3. Confirmation by WhatsApp through Lexi.
4. Theo hears it: browser test call in Bland's dashboard, then a South African number and call divert.
