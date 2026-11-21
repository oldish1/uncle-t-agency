# New client

> Create a client's folder in the brain and wire it in. Use when a client signs, or when starting to record a prospect that is about to sign.

## Variables

client: $ARGUMENTS (the business name, and the trade or suburb if known)

---

## Instructions

1. If no name was given, ask for the business name in one plain question.
2. Check first: look for existing files on this client (`clients/`, `outputs/`, `plans/`, `todo/`, other branches with `git branch -r`, the ledger). Say what already exists in one line.
3. Make the slug (lowercase, hyphens, for example `zanzibar-hair-and-beauty`). Copy `clients/_template/` to `clients/<slug>/`.
4. Fill in everything already known from the conversation, the Pipeline Sheet or existing notes. Mark unknowns `<ask>` so they show up as questions, never guess.
5. Remind Theo of the rules in `clients/README.md`: no secrets in these files, and real client details only once the repo is private.
6. Wire it in: add the client to the table in `clients/README.md`, add a row to `todo/README.md` or `todo/lexi.md` for onboarding (`/lexi-onboarding`), and tell Theo to add the client's Make scenario ID to the Chief of Staff watch table in `apps/chief-of-staff/PLAYBOOK.md` the day they go live.
7. Write the ledger row, tell Theo in plain English what was created and the next question to ask the owner.
