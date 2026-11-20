# SEO

> Check how a local business shows up on Google Maps, Google and AI tools, and what to fix. Uses the `seo` skill.

## Variables

request: $ARGUMENTS (a business name or website, or `full <business>`, `monthly <client>`, `fix <url>`)

---

## Instructions

Load the `seo` skill (`.claude/skills/seo/SKILL.md`) and follow its mode for the first word of the request. With no first-word mode, run the Found Check. With no request at all, ask for the business name and website in one plain question.

Before checking anything, look in this workspace for existing work on that business (outputs, plans, other branches, the ledger). Report what already exists in one line before starting.

Finish by saving the report where the skill says, writing the ledger row, and telling the user in plain English the 3 biggest findings and the next step. No jargon without a translation.
