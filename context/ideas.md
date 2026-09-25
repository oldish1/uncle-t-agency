# Ideas, parked

> Someday/maybe. Not active, not scoped, not forgotten. Revisit when the current priority (Lexi rebuild, founding clients) has room to spare.

## AI email assistant for the day-job receptionist

An assistant to sort supplier emails and draft purchase orders at the boilermaking day job. Separate from anything Uncle T Agency sells, this is internal tooling for Theo's own workplace, not a client product.

## The Turkish businesswoman lead (via Nita)

Referred in through Nita. Runs a tour company, restaurants, and rentals. Two separate needs surfaced: her businesses could use the same booking/WhatsApp automation Uncle T Agency sells, and she also wants an honest bookkeeper, which isn't something the agency currently offers. Worth a conversation to find out which one she actually wants solved first.

## AIOS-as-a-service

Once this context/ledger workspace system is proven on Uncle T Agency itself, package the same setup for other small business owners, starting with Nita's cleaning business as the first real test case beyond Theo's own. A second product line sitting alongside Lexi, not a replacement for it.

## Lexi Voice (queued behind Lexi 2.0)

An AI phone receptionist that answers the salon's line, books the appointment and sends a WhatsApp confirmation during the call. Inspired by a reel (Sept 2026) showing a Bland AI + Claude Code build for a US auto shop, pitched at $2,000 build + $500/month retainer. The creator shared a public template: github.com/jasonc00person/bland-ai-receptionist.

How the demo call flows: Greeting → Offer availability (three slots, not an open question) → Caller + vehicle → Capture service list → Text VIN + parts link mid-call → Wrap up → Confirm + End. Two global steps can fire at any point: AI disclosure (tells the truth if asked "am I talking to a bot?") and Transfer to human.

Salon version: Greeting → Offer three slots → Name + phone → Capture services (cut, colour, braids, etc.) → WhatsApp the booking and price list mid-call → Wrap up → Confirm + End. Globals: AI disclosure, transfer to Chante.

Why it's a good fit: it reuses what 2.0 is building anyway (the Calendar availability check, the booking write, the tracking sheet, cancel/reschedule). Voice becomes a second front door onto the same brain, not a separate product. It also covers the calls a salon misses while the stylist's hands are busy, which WhatsApp alone can't.

Questions to answer before building:
- Can Bland (or Vapi/Retell) give a South African number, or forward a local number to it cleanly?
- Per-minute cost is charged in US dollars. Work out the real Rand cost per booking call before pricing it.
- Does the voice handle Cape Town accents, and Afrikaans or isiXhosa words in service names, well enough?
- Local pricing: $2,000 + $500/month is US money. It needs its own Rand price for Cape Town salons, probably an add-on tier on top of the Lexi System.

Cheaper first step worth testing: let Lexi on WhatsApp understand voice notes. Lots of clients send those instead of typing, and it's a small bolt-on once 2.0 is live.

Trigger to start: Lexi 2.0 live, under 20 seconds, with at least one paying client on it.
