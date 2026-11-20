# Skills roadmap

> Which of our repeated jobs should become skills, ranked. Built from reading the ledger across all branches (about 150 rows, Aug to Nov 2026), the plans, and the handoffs. Skills already in the workspace: see `.claude/skills/`. Others exist on other branches (sales-coach, built 19 Nov) and need merging.

The test for a skill: we've done the job 3 or more times, the steps can be written down, and last time's mistakes are worth keeping.

| # | Skill | Why | Evidence in the ledger | Status |
|---|---|---|---|---|
| 1 | lexi-onboarding | First paying client is the top priority and there is a lot to remember | 56 `lexi/` rows, the client template plan, 2 incidents | Built 20 Nov |
| 2 | make-safe-edit | The same Make mistakes cost hours: router fallbacks, `.result.`, no `or()`, blueprint size, live edits | Fix2 to fix15b on 23 to 27 Sept, 8 separate bugs | Not built. Partly covered in lexi-onboarding lessons |
| 3 | whatsapp-meta-setup | Webhooks, per-number overrides, templates, the demo number mix-up, Rex's separate SIM and Meta app | 19 Sept incident, 14 Oct Rex setup, template steps | Not built |
| 4 | client-site (build, sync, draft deploy, publish) | Sites built and redeployed repeatedly (CHALES, T&T, Uncle T's own); the live site changed behind our back twice | T&T v1 to v3, CHALES pages, deploy script | Not built. Needs the design-taste-frontend skill alongside |
| 5 | reel-edit | Chanté films, Claude edits, Theo posts; scripts exist | 19 Nov competition reel, curls reel, cinematic_cut.py | Scripts exist, no skill |
| 6 | seo (Found Check, monthly) | The Get Found product | CHALES Oct to Nov | Built 20 Nov |
| 7 | sales-coach | Daily sales practice | Built 19 Nov on another branch | Exists, not merged here yet |
| 8 | discovery-chat | The 20 salon conversations and Hormozi script | Commits 141c429, 6fec0fe, fd91443 on other branches | Scripts exist, could join sales-coach |

## Do next

Make-safe-edit and whatsapp-meta-setup would protect the live client from the next mistake. Merging the other branches is needed so all skills sit in one place, otherwise each session only sees what its own branch has.
