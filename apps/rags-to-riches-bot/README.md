# Rags to Riches booking bot: source

The live bot is the Make scenario **"Rags to Riches - Booking Bot"** (ID 7645932). This folder is its source, so changes are made here and uploaded, not hand-edited in Make.

- `code/`: the six Make Code steps (A day picker, B date + duration, C capacity count, D Claude request, E parse Claude, F confirmation + event). `node code/test.js` runs the tests.
- `system-prompt.txt`: the Claude instructions (goes into the "Inbound + config" step).
- `base.json`: the webhook, config and session-lookup steps.
- `build_blueprint.py`: builds `blueprint.json` (the whole scenario) from the above.

To change the bot: edit here, run `python3 build_blueprint.py && mv full.json blueprint.json` (blueprint.json is git-ignored because it carries the bank details from `private/`), upload it with the Make connector (scenarios_update), then download it back and compare. Keys and tokens are never stored here: they're placeholders (`PASTE_...`) filled in directly in Make.

## Several dates (added 17 Oct 2026)
For clients who book a month ahead across different apartments (Kobie). In the day list the client taps
**Several dates** and types one line per date with the place, e.g. `26 Oct 2910 Bree`. Claude reads the list
(code/M1.js builds the request, M2.js checks it), M3.js checks each date against Nita's calendar using the same
2-points-a-day rule as C.js, the client picks one arrival time for all, and M4.js re-checks and builds up to
10 calendar events plus one confirmation. The list waits in BookingSession column S (`multi_json`) between
messages. Tests: `node code/test_multi.js`.

## Change / cancel (added 28 Oct 2026)
A client messages "change" or "cancel" (K.js spots it). Luna lists their upcoming bookings from Nita's calendar
(events carry `extendedProperties.private.wa_id`), they tap one, then Change date / Cancel booking / Keep it.
- Cancel: the event stays in Nita's calendar, renamed "❌ CANCELLED ..." (grey, transparent); capacity checks
  (C.js, M3.js, M4.js, X4.js) ignore anything starting with ❌.
- Change: pick a day (or type one, X5.js), pick a time, X4.js re-checks that day without counting the booking
  itself, then PATCHes the same event.
- Less than 24 hours before: R150 fee warned up front and flagged in the calendar title ("R150 LATE FEE" /
  "R150 LATE CHANGE"). Fee and hours are `FEE_IN` in build_blueprint.py.
Calendar write steps have an Ignore error handler so one Google hiccup can't switch Luna off. Tests: `node code/test_manage.js`.
