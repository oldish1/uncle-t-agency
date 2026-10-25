# Plan: Your own booking channel for Nita's hosts ("a mini Booking.com that's theirs")

**Created:** 2026-10-25
**Status:** Draft
**Request:** Make this its own product: a booking channel the hosts own, that takes direct bookings and keeps all guest messages in one place, so Booking.com's closed inbox stops being the problem.
**Purpose:** Hosts keep the 15% Booking.com takes, own the guest relationship, and handle every guest message on WhatsApp where we can automate it. Builds on `plans/2026-10-20-host-guest-assistant.md`, which becomes the messaging half of this.

---

## Overview

### What This Plan Accomplishes

Each host gets a stand-alone stay: a mobile-first booking page for their apartment (photos, price, rules, live availability) and a WhatsApp number behind it. A guest picks dates on the page, taps "Book on WhatsApp", and the assistant takes it from there: checks the calendar, holds the dates, sends payment details, confirms, and then answers every question during the stay. Host and Nita's team get one list of bookings and extras.

### Why This Matters

Booking.com sells two things: discovery (strangers finding you) and a messaging and payment wrapper. We can't copy discovery, and pretending we can would waste Theo's time. We can copy the wrapper, and that is the part hosts pay 15% on for guests who already know them. Repeat guests, friends of friends and corporate stays are the first targets. A host with 9 dates in a month who books even three of those direct saves real money, and every guest conversation is automated instead of manual.

Be straight with hosts: this does not replace Booking.com for finding new guests. It keeps the guests they already have.

---

## Current State

### Relevant Existing Structure

- `plans/2026-10-20-host-guest-assistant.md`: the guest messaging plan (ask, extras, host paths; House, Extras, Requests tabs). Unchanged by this plan except Step 11 and decision 8, which now point here.
- **Luna** (Make scenario 7645932, source in `apps/rags-to-riches-bot/` on branch `claude/charming-tesla-j7vsii`): already books dates against a Google Calendar, handles several dates, confirms, writes a sheet. The booking mechanics are proven.
- `design-taste-frontend` skill and the T & T Engineering build (`apps/tt-engineering`): the pattern for a client site, Next.js or static, deployed with `scripts/deploy_netlify.sh`.
- `reference/research/2026-10-20-booking-com-guest-messaging.md`: commission figures (Booking.com about 15%, Airbnb 15.5% host-only fee).

### Gaps or Problems Being Addressed

- No way for a guest to see a host's place and dates outside Booking.com or Airbnb.
- No way to stop double bookings between our channel and Booking.com or Airbnb.
- No payment step for stays. Luna uses EFT on completion, which is wrong for a stay: a stay needs a deposit before the dates are held.

---

## Integration Type

**Classification:** App (static site plus Make scenario), one per host, stamped from a template.
**Reasoning:** Same shape as Luna plus a client site, both proven. A single multi-host platform with logins is a much larger product (and the thing Booking.com is). Not for the pilot.
**Location:** `apps/host-stay/` (template site), `apps/host-assistant/` (messaging, from the other plan), per-host copies under `apps/host-stay/hosts/<name>/`.

---

## What each host gets (stand-alone)

| Piece | Own per host |
|---|---|
| Booking page (their domain or a free Netlify address) | yes |
| WhatsApp number | yes |
| Make scenario(s) | yes |
| Google Sheet (House, Extras, Requests, Bookings) | yes |
| Google Calendar for direct bookings | yes, theirs |
| Claude API key | yes |
| Meta app | yes |

Nothing shared with Luna, Lexi or another host. Shared building facts get copied, never linked.

---

## The guest journey

1. **Find:** the host shares their page link on WhatsApp status, Instagram, to past guests, in the QR in the apartment ("book your next stay direct"), and in a short thank-you after check-out.
2. **Look:** the page shows photos, a short description, rules, price per night, and a date picker greyed out where the place is taken.
3. **Ask to book:** guest picks dates and tap "Book on WhatsApp". The button opens the host's number with the dates pre-filled in the message (`wa.me/<number>?text=...`).
4. **Assistant checks:** reads the calendars, replies "Free for 14 to 17 Nov, 3 nights, R___ total", asks name and number of guests.
5. **Hold and pay:** assistant holds the dates for 24 hours, sends EFT details with a booking reference. Deposit amount is the host's choice (question below).
6. **Host confirms payment:** one tap on the host's WhatsApp ("Paid 4821"), then the guest gets confirmation, check-in details on the day, and the House Q&A and extras from the other plan.
7. **After the stay:** thank-you, a review request, and a "book direct next time" link.

Messages stay on WhatsApp the whole way, so there is no closed inbox to fight.

---

## Design Decisions

### Key Decisions Made

1. **A booking request, not instant checkout.** Host and guest both stay in control, and no card gateway is needed for the pilot. EFT with a reference matches how Nita already works. Card payments (PayFast or Yoco) are phase 2 once volume justifies the fees.
2. **The page is static, the brain is the assistant.** The page only shows facts and availability and opens WhatsApp. All logic lives in the Make scenario, as Luna does it. That keeps the page cheap to host and easy to copy to host two.
3. **Availability comes from three places, and double-booking is the main risk.** Direct bookings live in the host's own Google Calendar. Booking.com and Airbnb both give a calendar link (iCal) that the scenario reads on every availability check. Do not rely on importing it into Google Calendar, which refreshes slowly. For the other direction, the host exports our calendar's iCal into Booking.com and Airbnb. Both platforms refresh iCal feeds on a delay of hours, so the scenario also holds a tight rule: a direct booking asks the host to block the dates on Booking.com straight away. A channel manager would solve this properly and is out of scope for the pilot.
4. **Honest about discovery.** The page launches with the host's existing circle, not strangers. If the pilot shows hosts want strangers too, Google Business Profile and a simple Google search presence come next, not a marketplace.
5. **Host-first copy.** Priced against commission: "Booking.com takes about 15% of the full booking, including the cleaning fee. This takes a flat monthly fee."
6. **No hosts' private details on the page.** Address shown only as the building and suburb until the booking is confirmed. Exact unit and codes arrive on WhatsApp after payment.
7. **Same light background, dark text rule** (Theo's preference), and the `design-taste-frontend` skill for the page so it looks designed, not templated.

### Alternatives Considered

- **One shared platform with logins for many hosts ("our own Booking.com"):** the real thing, but needs search, accounts, payments, dispute handling and traffic. Months of work and an unwinnable fight on discovery. Rejected for now, revisit if five or more hosts want to be listed together.
- **Smoobu, Lodgify, or Hospitable subscriptions:** they exist and handle channel sync, but they bill in dollars or euros and don't carry the WhatsApp or Nita angle. Worth a look as a fallback for calendar sync if the iCal approach proves leaky.
- **Instant card checkout from day one:** more friction to set up, gateway fees, and the host must sign a merchant account first. Phase 2.

### Open Questions

1. **Deposit rule:** full payment up front, 50% deposit like Nita's deep cleans, or pay on arrival for people the host already knows? Ask Fancy.
2. **Cancellation rule** and who decides refunds. Always the host, never the assistant.
3. **Price per night and minimum stay** per apartment, and whether the cleaning fee is separate. (Nita's clean fee ties in: a direct booking can add a checkout clean as a paid extra.)
4. **Payment host-confirm step:** is one tap on "paid" enough, or does the host want to attach proof of payment? Start with the tap.
5. **Domain:** free Netlify address for the pilot, or a name in the host's name (about R99/yr, bought in their name as with Nita)?
6. **Is Fancy the right pilot for this half?** The messaging pilot can start on Booking.com guests today. Direct booking needs the host to have repeat guests to send to the link. Ask in the questions below.
7. **Pricing:** one flat monthly fee covering assistant plus page. Directional: R299 to R499 per apartment, to be set after the free month. Compare with the host's own commission saved (about R150 on a R1,000 booking).

---

## Questions to add for Fancy (send with the existing 16)

*17. Do you have guests who come back, or friends and family who stay?* A) Many B) A few C) None yet
*18. How would you like to be paid by direct guests?* A) Full amount up front B) 50% deposit, rest on arrival C) Pay on arrival
*19. Price per night, minimum nights, and cleaning fee for each apartment.*
*20. Cancellation: how many days before arrival can a guest cancel for a refund?*
*21. Can you send 5 to 10 good photos per apartment, plus a short description in your own words?*
*22. Please send the calendar link (iCal) from Booking.com and Airbnb for each apartment.* (I'll tell you where to find it.)

---

## Step-by-Step Tasks

Steps marked **Theo** need him. The messaging steps are in the other plan and run first.

### Step 1: Send the combined questions (Theo)

Add questions 17 to 22 to Message 1 of `outputs/rags-to-riches/host-assistant-questions.txt`, then send. Confirm the pilot host from answers 1, 3 and 17.

### Step 2: Build the messaging half

Run Steps 2 to 10 of `plans/2026-10-20-host-guest-assistant.md`. The direct-booking path plugs in as a fourth path ("book") next to ask, extras and host.

### Step 3: Bookings tab and availability check

**Actions:**

- Add a `Bookings` tab: `ref`, `guest_wa_id`, `guest_name`, `arrive`, `leave`, `nights`, `total_zar`, `status` (held, paid, cancelled, done), `hold_expires`, `source`.
- Availability Code step: read the host's Google Calendar plus each iCal link, treat all-day events and "Reserved" or "Booked" blocks as taken, return free or the nearest free dates.
- Node tests: back-to-back stays, a one-night gap, a stay that straddles a Booking.com block, an iCal with a time-zone offset, and a host feed that is unreachable (fail safe: do not offer the dates, tell the guest the host will confirm).

### Step 4: The "book" path

**Actions:**

- Parse dates and guest count from the message or the page's pre-filled text. Claude extracts, the Code step validates (no past dates, minimum stay, maximum guests).
- Quote the total from the Extras and price settings. Hold the dates (calendar event titled `HOLD ref`) and set `hold_expires` to 24 hours.
- Send EFT details from the host's sheet with `ref`.
- Hold-expiry scenario runs hourly and releases expired holds, telling the guest.
- Host "paid ref" reply confirms the booking and swaps `HOLD` for the guest's name.

### Step 5: The booking page

**Actions:**

- Use the `design-taste-frontend` skill, light background and dark text, mobile first, one page: hero with a real photo, the place in a few lines, amenities, price, house rules, month calendar showing taken dates, Book on WhatsApp button, small "Why book direct" line.
- Availability on the page is read from a small published feed generated by the Make scenario (dates only, no names), refreshed hourly.
- Deploy with `scripts/deploy_netlify.sh`. Address kept to building and suburb.
- Add the page link to the QR sheet, the thank-you message and Booking.com's post-stay message.

### Step 6: Test

**Actions:**

- Fake guests from 3 test numbers: a clean booking, a double-booking attempt on dates Booking.com shows as taken, an expired hold, a cancellation inside and outside the rule, a guest asking for a discount (must go to the host), and a voice note.
- Run `/test` before calling it done.

### Step 7: Pilot with real guests

**Actions:**

- Fancy shares the link with 5 past or future guests who know them.
- Watch the first three real conversations read-only; fix the same day; one ledger row per fix.

### Step 8: Review after the free month

**Actions:**

- Count: direct bookings, commission saved at the host's own rates, messages handled without the host, extras sold for Rags to Riches, hours saved.
- Decide price. Roll to Kobie and Megan from `apps/host-stay/` template if it worked.

---

## Connections & Dependencies

### Updates Needed for Consistency

- `plans/2026-10-20-host-guest-assistant.md`: decision 8 and Step 11 now point to this plan (done in this session).
- `CLAUDE.md` map and `context/rags-to-riches.md` once `apps/host-stay/` exists.
- `context/tech-stack.md`: row per host number and domain.
- `docs/host-assistant.md` via `/document` after it works.

### Impact on Existing Workflows

None on Lexi or Luna. Only touch point is Luna's branch, which must be merged or copied first (same dependency as the messaging plan).

---

## Validation Checklist

- [ ] Questions 1 to 22 answered by the host
- [ ] A guest can pick dates on the page and land in WhatsApp with them pre-filled
- [ ] Assistant refuses dates already taken on Booking.com or Airbnb
- [ ] A hold expires after 24 hours and is released
- [ ] Host can confirm payment with one reply
- [ ] No exact address, door code or password on the public page
- [ ] Replies in under 20 seconds
- [ ] Nothing shared with another host

## Success Criteria

1. The pilot host takes at least one real direct booking through the page and assistant.
2. No double booking happens during the pilot.
3. The host says guest messages are easier to handle and wants to keep it.
4. The host's saved commission is worth more than the monthly fee.

---

## Notes

- Never put wifi passwords, door codes, bank details or guest phone numbers in this repo. They live in each host's sheet.
- Booking.com's and Airbnb's rules about steering guests off-platform apply to people who found the host there. Telling past guests about a direct link is normal practice, but the pilot host should not put a direct-booking link in a Booking.com message to a guest who booked there. Check each platform's current terms before the page goes live.
- iCal sync delay is the single biggest risk. If it causes even one double booking in the pilot, move to a channel manager before onboarding host two.
