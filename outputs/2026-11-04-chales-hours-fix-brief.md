# Brief: fix CHALES opening hours everywhere + Lexi directions

> Paste this whole file into a new Claude Code session (start with /prime first). It says what's wrong, what Theo needs from Chanté, and exactly where each change goes. Written 4 Nov 2026. Full background: `plans/2026-11-04-chales-google-page-one.md` (Step 0) and `context/lexi.md`.

## The problem

CHALES shows 3 different sets of opening hours, and Google trusts a business less when its details don't match. Customers can also turn up to a closed door.

| Where | Tue–Fri | Saturday | Sunday | Monday |
|---|---|---|---|---|
| Website (chaleshairboutique.co.za) | 08:00–17:00 | 08:00–17:00 | By appointment | Closed |
| Google listing | 08:00–16:30 | 09:00–15:00 | Closed | Closed |
| Lexi (bookable slots) | 08:00 to 16:00, hourly | 08:00 to 16:30, every half hour | Closed | Closed |
| TikTok bio | Not checked (Theo to look in the app) | | | |

Worst clash: Lexi books Saturday 15:30 and 16:30, Google says she closes at 15:00.

## Confirmed hours (Chanté, via Theo, 6 Nov 2026)

| Day | Hours |
|---|---|
| Tuesday to Friday | 08:00 to 16:30 |
| Saturday | 09:00 to 15:00 |
| Sunday | Closed |
| Monday | Closed (assumed, as everywhere before; Theo to confirm if not) |

**Already done (6 Nov):**
- Google listing already showed exactly these hours. Nothing to change there.
- Website: home page (both hours blocks and Google's hidden business details) and all 5 new treatment pages updated in `apps/chales-site`. Goes live with the next deploy.

**Still to do: Lexi.** Her slot lists don't match:
- Saturday: Lexi offers 08:00 to 16:30 every half hour. Must become **09:00 to about 14:30** (the last start time depends on the answer below). This is the urgent one: right now a client can book Saturday 16:00 when the salon closes at 15:00.
- Tuesday to Friday: Lexi offers hourly 08:00 to 16:00. Opening time is right. Is 16:00 a sensible last start when she closes at 16:30? Only for short services.
- Step 3's slot instruction lists the same times "for every open day". It needs separate weekday and Saturday lists.

## Still to get from Chanté


- [ ] Latest time a client can **start** an appointment (often earlier than closing, e.g. a 3-hour Nanoplastia can't start at 16:00)
- [ ] Weekdays: hourly slots like now, or half-hourly like Saturday?
- [ ] Any lunch break?
- [ ] December and January days she's closed: 16 Dec (Day of Reconciliation), 25 Dec, 26 Dec, 1 Jan, plus any holiday she's taking. Lexi only knows the April 2026 holidays right now.

## The changes, once the hours are agreed

Do all of these the same day.

### 1. Lexi (Make scenario 5043763, "Chales Hair Boutique")

The hours live in 5 steps of the live scenario:

| Step | What it is | What to change |
|---|---|---|
| 3 | Claude API call (Lexi's instructions) | The "CLOSED DAYS, CRITICAL RULE" text (open days, Sunday/Monday rule, public holidays) and the line listing the slot times (8:00 AM to 4:00 PM) |
| 104 | HTTP request | Contains the 04:00 PM slot list |
| 119 | Iterator (feeder) | Contains the 04:00 PM slot list |
| 130 | Code step | Weekday and Saturday slot lists (04:00 PM / 04:30 PM) |
| 140 | Code step | Weekday and Saturday slot lists (04:00 PM / 04:30 PM) |

Also keep `scripts/lexi/build_spoken_taps.py` (slot lists on lines ~104–106, and the "today only before 15:00" rule) matching, so a future rebuild doesn't bring the old hours back.

**Warning:** the scenario is about 280 KB. Resending the whole thing through the Make tool from a session is risky for a live booking system. Safer: fetch it, make the edits in a script, check the result, and either hand Theo click-by-click edits for the Make editor, or push only if the update can be done cleanly. Run a test booking on Theo's own number afterwards, including a Saturday afternoon one.

**Same session, two directions edits** (step 330, "Build photo confirmation"):
- `maps` input: change to `https://maps.google.com/?cid=13659620552899745009` (opens the CHALES Google listing, same pin as before)
- Code: change `46 Alexandra Street, Oakdale, Bellville` to `46 Alexandra Street, Oakdale, Bellville (inside the Vodacom building)`
- Skip these if Theo already made them by hand. Check first.

### 2. Website
- Update the hours in both places on the page (the Location section and the Contact/Visit Us section).
- Add "inside the Vodacom building" under the address in both places.
- The site files live on Netlify, not in this workspace. Pull them down via Netlify first.

### 3. Google listing (Theo or Chanté, at business.google.com)
- Hours: set to the agreed ones. Add special hours for the December holidays.
- Address: add "Inside the Vodacom building" in the second address line, or in the description if Google won't allow it.
- Claude writes the exact text to paste.

### 4. TikTok bio (Chanté, in the app)
- If it lists hours, change them. Make sure the WhatsApp number is Lexi's, 071 429 6057 (still outstanding since 12 Oct).

## Done means
- All four places show the same hours, word for word.
- A test booking on Saturday afternoon and on a weekday only offers times inside the new hours.
- The booking confirmation says "inside the Vodacom building" and the Get Directions button opens the CHALES listing.
- Ledger row written, `context/lexi.md` and `context/marketing.md` updated with the new hours.
