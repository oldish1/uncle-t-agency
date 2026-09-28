# Rags to Riches booking bot: source

The live bot is the Make scenario **"Rags to Riches - Booking Bot"** (ID 7645932). This folder is its source, so changes are made here and uploaded, not hand-edited in Make.

- `code/`: the six Make Code steps (A day picker, B date + duration, C capacity count, D Claude request, E parse Claude, F confirmation + event). `node code/test.js` runs the tests.
- `system-prompt.txt`: the Claude instructions (goes into the "Inbound + config" step).
- `base.json`: the webhook, config and session-lookup steps.
- `build_blueprint.py`: builds `blueprint.json` (the whole scenario) from the above.

To change the bot: edit here, run `python3 build_blueprint.py && mv full.json blueprint.json` (blueprint.json is git-ignored because it carries the bank details from `private/`), upload it with the Make connector (scenarios_update), then download it back and compare. Keys and tokens are never stored here: they're placeholders (`PASTE_...`) filled in directly in Make.
