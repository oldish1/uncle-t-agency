# Test flow and go-live checklist

## Test flow (real WhatsApp messages, write down time for each step)

1. "Hi": greeting and service list arrive. Target under 5 s.
2. Name one service in the first message (typed, then as a voice note): menu is skipped, day list follows.
3. Tap a day, tap a time: each reply 2 to 9 s.
4. Type a name: confirmation arrives with photo, bold details, address and Get Directions button. Calendar event and sheet row created.
5. Book a slot that is already taken: Lexi refuses and offers another.
6. Book again as the same client: the second booking is separate, nothing overwritten.
7. Cancel: offers a different date first, then cancels on confirmation. Calendar event removed, sheet row marked cancelled, other clients' bookings untouched.
8. Reschedule: new day and time, old event removed, new one created.
9. Send a voice note: acknowledgement, transcription, normal reply. A voice note at the name step asks the client to type the name.
10. Send the same message twice quickly: only one action happens (dedup guard).
11. Cancel with nothing booked: "nothing booked yet", no half-finished session left.
12. Ask something off-script (price, location, "do you do braids"): sensible answer from the client's real info, no invented services.
13. Afrikaans message: understood.
14. Reminder scenario: run once, the template arrives on a test number correctly.
15. Check no other client's scenario ran during all of this.

## Go live

- [ ] Reminder template (`appointment_reminder`) created and approved in the client's WhatsApp Manager
- [ ] Reminder scenario scheduled, test-mode number gate removed, tested with a real booking tomorrow
- [ ] Staff alerts point at the owner's real WhatsApp, verified with one test alert
- [ ] Scenario is on, webhook is the client's own, no per-number override pointing elsewhere
- [ ] Lexi's number is on: Google profile appointment link (`wa.me/<number>`), social bios, website buttons, counter QR
- [ ] Opening hours match everywhere: Google listing, website, Lexi's slot list, social bios
- [ ] Owner briefed (the paragraph at the end of `intake.md`), knows how to take over a chat
- [ ] Execution log checked after the first real booking
- [ ] Client file updated, ledger row written, `context/numbers.md` paying-clients count updated
