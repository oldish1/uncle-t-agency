# Handoff: Chales membership tracker, dedup fix, client template, Firecrawl setup

## What we were working on and why

Two threads, both started from Chanté's membership/loyalty spec:

1. **Build the 6 Wash & Blowdry membership tracker into the live "Chales Hair Boutique" Make scenario** (id `5043763`) — deduct a wash on booking, refund on cancel, BALANCE and RENEW keyword replies, final-wash staff alert, basin-treatment-every-2nd-visit logic. This had to go into the LIVE scenario, not a test one, because that's the number Chanté's real clients message.
2. Once that was fully proven live, start on the **reusable client template** — a sanitised, credential-free version of Lexi that can be quickly adapted for Uncle T Agency's next paying client.

Along the way we also fixed the workspace's Firecrawl web-research setup, which was silently broken.

## Where we got to

### Done and proven live
- **Membership tracker**: balance, renew, wash deduction on booking, wash refund on cancel, double-booking handling — all tested live on Theo's own number and confirmed correct. Basin treatment correctly flags on wash 4 (every 2nd wash). Chanté confirmed she loves the salon photo on the booking confirmation — nothing to change there.
- **Root-caused and fixed two real Make bugs** along the way, both worth remembering for any future build in this scenario:
  - Make's `code:ExecuteCode` module output is wrapped under `.result.` (e.g. `{{306.result.ok}}`), not flat — every reference to a new calc module's output needs that prefix or it silently resolves empty.
  - Make has no `mod()` and no `or()` function in its formula language — use `floor()` arithmetic for even/odd, and nested `if()` for OR logic.
- **Found and fixed a duplicate-message-processing bug**: nothing was stopping the same WhatsApp message from being processed twice (a retry, a slow response, whatever the cause), so a duplicate delivery would re-run the wash deduction/refund math and corrupt the numbers. Fixed with a `ProcessedMessages` sheet-backed guard, keyed on WhatsApp's own message ID, wrapping the three non-idempotent actions (deduct, refund, renew-alert). Validated in an isolated test before shipping. This is currently live in the "Chales Hair Boutique" scenario (it's back ON — Theo turned it off briefly mid-debugging, then the fix (`lexi-fix15-blueprint.json`) was imported and the scenario reactivated).
- **Client template built**: `private/lexi-client-template-blueprint.json` — a sanitised copy of the live Chales scenario with all credentials (WhatsApp Bearer token, Anthropic API key) and Chales-specific IDs (phone number ID, sheet ID, calendar email) replaced with clear `{{PLACEHOLDER}}` markers, verified clean. Full process and a checklist of exactly which 11 modules need salon-specific copy changed per new client is documented in `plans/client-template.md`.
- **Firecrawl actually works now**: found `.env` didn't exist yet (created from `.env.example`, Firecrawl key added), found `python-dotenv` wasn't installed so `.env` was never being read by anything (fixed with `uv pip install --system python-dotenv`), and found this sandbox's network policy was blocking `api.firecrawl.dev` entirely. Walked Theo through the environment's own settings (Claude Code sidebar → click the environment name next to the session title → "Edit cloud environment" → Network access) and switched it from "Trusted" to "Custom" with `api.firecrawl.dev` and `chaleshairboutique.co.za` allowed.

### Not done — pick these up next

1. **RENEW alert still doesn't reach Chanté.** Root cause found: the alert's target number (`27714296057`, hardcoded in modules 337 and 346 of the live scenario) is actually **Lexi's own WhatsApp number**, not a separate number Chanté checks. Need Chanté's real personal/business WhatsApp number, then swap it into both modules and re-test. This is a quick fix once we have the number — no rebuild needed, just edit two `"to"` fields and re-import.
2. **Firecrawl's network fix needs a fresh session to take effect.** The environment setting was changed correctly (Custom, with `api.firecrawl.dev` + `chaleshairboutique.co.za` allowed), but per the settings page's own note, this only applies to *new* sessions. First thing to do in the next session: verify Firecrawl actually works now (`uv run python scripts/firecrawl_tool.py status` from the workspace root), then use it to pull Chanté's real contact number from her website if she hasn't sent it directly by then.
3. **Reminders scenario ("Chales - Appointment Reminders", id `7617803`) is still in test mode.** Its module 4 filter only sends to Theo's own number (`testPhone = 27714304346` set in module 1). This means real clients have NOT been getting day-before reminders since it went live. Theo hasn't decided yet whether to turn this off now or wait — ask him, then either clear the `testPhone` value (module 1's `mapper.variables`) or leave it, per his answer.
4. **Reminders scenario doesn't have a reusable-client template yet.** Started (fetched the blueprint, it's small — just 5 modules) but not finished. Same sanitisation approach as the main Lexi template: strip the WhatsApp token, phone number ID, and calendar email into placeholders. Should be a quick follow-up once there's a real second client, or sooner if Theo wants it done proactively.
5. **No second client has signed yet** — the client template work is groundwork, not yet exercised for real. When a lead is close, walk through `plans/client-template.md`'s process with Theo.

## Gotchas for the next session

- The **live "Chales Hair Boutique" scenario blueprint is large** (~230K characters as of this session) — always fetch fresh via `mcp__Make__scenarios_get`, read the saved file with Python (not the Read tool), and never try to hand-type the whole blueprint back through a tool call as one block — build patches with small Python scripts instead, exactly like `build_fix12/13/14/15.py` did (still in the scratchpad, gone once this session ends — the *pattern* is what to reuse, not the files themselves).
- **Never retype a credential literal** (WhatsApp Bearer token, Anthropic API key) into a new script — always pull it programmatically from an already-fetched module (`HEADERS = M[79]['mapper']['headers']` style), exactly as done throughout tonight.
- The Memberships sheet's real tab name has a **trailing space** (`"Memberships "`), and this is by design in the blueprint (Theo was asked to rename it once, unclear if he ever did — check before assuming it's fixed).
- `ProcessedMessages` sheet tab has clean headers, no trailing space, columns are `MessageID | Action | Timestamp`.

## What to do next, in order

1. Get Chanté's real WhatsApp number for staff alerts (ask her directly, or use Firecrawl on her site once confirmed working) → fix modules 337 and 346's `"to"` field → re-test RENEW and confirm she actually receives it this time.
2. Verify Firecrawl works in this fresh session.
3. Ask Theo whether to turn off test mode on the reminders scenario now.
4. Whenever a second client is close to signing, walk through `plans/client-template.md`.
