# Lexi (WhatsApp booking assistant)

Production Lexi (Make scenario 5043763) is frozen at fix14: voice notes, service shortcut, photo confirmation, cancel, reschedule, membership, reminders, alerts. Reminders scenario 7617803. Details: `context/lexi.md`. Next paying client: `/lexi-onboarding`.

## Open
- [ ] Check Make for warnings on production Lexi (watchdog session). It showed no errors on 26 Oct
- [ ] Top up Make credits when low (about 60 to 80 credits per Lexi booking)
- [ ] Check the three failed Chales Sheets runs (403 errors)
- [ ] Lexi's opening hours and slot list to match Google (see chales.md)
- [ ] Clean-up pass to shrink the scenario, after the first paying client
- [ ] Reminders scenario template for new clients (10-minute job when a client signs)
- [ ] Export the sanitised template again if `private/lexi-client-template-blueprint.json` is missing in a new session

## Lexi 2.0 (fresh build, zero Make warnings by design, decided 7 Nov)
- [ ] Architecture and design: `plans/lexi2-design.md`, `plans/lexi2-architecture-map.md`. Build in its own sessions, production keeps running unchanged meanwhile
- [ ] Replace the Anthropic key stored in plain text in "Lexi 2.0 (test core flow)" (Make 8179409). `todo/security.md`
- [ ] Decide when Lexi 2.0 replaces production and how clients move over

## Later, after proof
- [ ] Lexi direct server, Phase 1 (own WhatsApp server instead of Make): `plans/2026-10-20-lexi-direct-server-phase-1.md`
- [ ] Multi-stylist support after 10 paying clients: `plans/2026-10-26-multi-stylist.md`
- [ ] Missed-bookings calculator (apps/missed-bookings) as a sales tool
- [ ] Build skills `make-safe-edit` and `whatsapp-meta-setup` so Make mistakes stop repeating
