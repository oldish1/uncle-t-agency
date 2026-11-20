# Branch merge notes, 20 Nov 2026

All 22 branches that had work not on main were merged into `ccr-333f61cf-fmh4ca`. Before this, main was months behind and every session only saw its own branch, which is why sessions kept saying things didn't exist when another session had built them (service pages, the Google listing, the review machine).

## What was merged
claude/clever-bardeen (87 commits: outreach, Rex, agents, plans, research), claude/focused-volta (60: agency site, design skills, QR card), claude/charming-tesla (55: Nita's bot and site), claude/make-lexi-2-performance (Lexi 2.0), ccr-424a3b63 (Lexi Call), ccr-4af36452 (Chales pages, review machine), ccr-9681c220 (sales-coach, 90-day plan, reels), ccr-7d22b758 (Chales SEO live, visibility playbook), ccr-f254526b (booking alert), ccr-30204bfc, ccr-2085cd70, ccr-986f1a46, ccr-ab0aca36, ccr-ac78a146, ccr-ea3898a9, ccr-f185a284, ccr-f646ed8a, claude/agent-autonomous-trading, claude/fervent-hypatia, claude/lead-scraper-lexi-cleanup, plus the three already inside others. A `.gitattributes` rule now merges `ledger/*.md` by keeping both sides.

## Conflicts and how each was settled (review these)
| File or folder | Decision | Why |
|---|---|---|
| `apps/uncletsautomation/` | Kept the clever-bardeen version. The focused-volta version is saved whole in `apps/_archive/uncletsautomation-focused-volta/` | Two sessions built separate full sites in the same folder. The kept one has the 16 Nov pricing deploy. Which one is live: check Netlify |
| `apps/chales-site/` | `site/` (from the SEO-live session, matches the deployed site) is the source. The review-machine session's layout is in `_generator-version/` | Auto-merging the two produced a hybrid with two canonical tags. Rebuilt from the deployed copy |
| `context/numbers.md` | Kept the 16 Nov pricing, marked the older founding-five rows "OLDER, check" | Three documents disagreed. Theo decides (`todo/agency-business.md`) |
| `CLAUDE.md`, `docs/_index.md`, `.gitignore`, `context/lexi.md`, `ideas.md`, `tech-stack.md`, `marketing.md`, `rags-to-riches.md` | Both sides kept | Additions on both sides. May contain repeated or overlapping lines to tidy |
| `scripts/lead_scraper*.py/json`, `docs/lead-scraper-agent.md` | Newer version (25 Oct) | The September one was older. The first-run CSV is saved as `outputs/leads/2026-09-27-hair-salon-all.first-run.csv` |
| `ledger/theo.md` | Sorted by time, exact duplicates removed (481 rows to 478) | |
| My own 28 Oct to 20 Nov CHALES notes | Marked superseded at the top | Written before I saw the other sessions' work |

## Overlap to know about
Two sessions built Chales SEO work on the same day: this session's `/seo` skill (`.claude/skills/seo`, `scripts/seo_check.py`) and the other's `docs/local-visibility-playbook.md`, `scripts/visibility_check.py` and the 41-step checklist. They fit together: `/seo` checks any prospect or client site (the Found Check), `visibility_check.py` tracks Chales' rankings over time. Keep both.

## Not changed
No branch was deleted. The remote branches still exist as a backup.

## Next
Merge `ccr-333f61cf-fmh4ca` into main, then start every new session from main. The GitHub repo is public (see `todo/security.md`): make it private first.
