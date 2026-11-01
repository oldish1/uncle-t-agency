# Plan: multi-stylist Lexi

Date: 26 Oct 2026. Status: designed, not built.

## Decision first

We target **solo salons** now. Solo owners are the quickest to sign and Lexi already fits them. Multi-stylist and the other Fresha-style features are built **once we have 10 paying clients**, or sooner if a salon with a team signs and pays for it. Until then Lexi stays frozen at fix14 (see `context/lexi.md`) and Chales' live scenario is not touched.

## What "multi-stylist" means

A client picks who she wants ("with Chanté", "with Thandi", or "anyone"), and Lexi books into that stylist's own diary. Two clients can book the same hour with different stylists. Fresha charges $14.95 a month for each extra team member, so this is where teams will compare us.

## Where it plugs into the current scenario (5043763)

Lexi is about 170 modules. Everything below is read from the live blueprint.

| Job | Modules now | Change |
|---|---|---|
| Check what is free | Calendar searches 100, 109, 129, 132, 138 | Search the chosen stylist's calendar, or all of them for "anyone" |
| Create the booking | Calendar events 38 and 81 | Create it on that stylist's calendar |
| Cancel or reschedule | Calendar calls 165, 166, 171, 172 | Use the calendar saved with the booking |
| Remember the choice | Sheet "BookingSession" | One new column, `stylist` |
| Ask the client | Router 40 / 321 (service shortcut) | New step after service: "Who would you like to book with?" |

New sheet tab **Stylists**: `name`, `calendar_id`, `services`, `days_off`. One row per stylist. A salon with one row works exactly as Lexi does today, so solo clients never see the new step.

## Build steps

1. Copy the client template (`plans/client-template.md`), never the live Chales scenario.
2. Add the Stylists tab and the `stylist` column.
3. Skip the "who" step if the Stylists tab has one row.
4. Make the three calendar jobs read the calendar from the chosen stylist.
5. Add "anyone": check every stylist, offer the first free slot, book that one.
6. Test with two made-up stylists, a cancel and a reschedule. Follow the router rule in `context/lexi.md`: append routes, never insert before existing ones, and check the fallback.
7. Only then offer it to a paying salon, at +R150 a month per extra stylist (to confirm with Theo).

Rough size: two to three working sessions, plus testing.

## After 10 clients: the rest of the list

In this order, because each one earns or saves a client money:

1. Multi-stylist (this plan).
2. Review requests after a visit (message ready in `outputs/chales/google-business-profile-kit.md`).
3. "Your usual?" rebooking.
4. Win-back message for clients who have gone quiet.
5. Monthly report to the owner.
6. Deposits and payment links.
7. Waitlist.

## Not planned

Point of sale, stock, payroll. Fresha owns that. We stay the assistant.
