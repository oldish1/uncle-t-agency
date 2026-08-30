# Prime

> Start-of-session ritual. Pulls the latest, catches up anything left unfinished, loads the brain, reports where things stand. Run it first, every session.

## Phase 1: Catch up (quietly, only speak if something happened)

1. **Who's in the seat.** Read `.seat` if it exists (`person: <name>`). No file means the founder named in CLAUDE.md.

2. **Work out what's stale, BEFORE you pull.** Order matters here and it's easy to get wrong: `git pull --autostash` stashes uncommitted work and pops it back afterwards, and popping **rewrites every one of those files' timestamps to now**. Do it the other way round and every genuinely abandoned file looks like it was touched a second ago, so the catch-up below can never fire. Take the list first:

```bash
git status --porcelain=v1 -uall -z | while IFS= read -r -d '' e; do
  f=${e:3}                                   # strip the two status chars and the space
  case "$f" in *" -> "*) f=${f##*" -> "};; esac   # a rename reports "old -> new"; keep the new path
  [ -e "$f" ] && [ -z "$(find "$f" -mmin -60 2>/dev/null)" ] && printf '%s\n' "$f"
done
```

`-z` keeps paths with spaces intact (git quotes them otherwise), and `-uall` lists the files inside an untracked folder rather than just the folder, whose own timestamp tells you nothing about what's in it.

3. **Now pull** (skip silently if git or the remote isn't set up yet):
```bash
git pull --rebase --autostash
```
If the pull hits a conflict, resolve it conversationally: read both versions, explain the difference in plain English, propose the merged text, apply on approval. Never show conflict markers.

4. **Sweep unfinished work from a closed session,** using the list from step 2:

   - **Untouched for over an hour** means a previous session closed without logging. Don't ask. Read what changed, write the missing `ledger/<seat>.md` row(s) yourself, commit with a plain-English message, push, and mention it in one line in the report. This is the whole point of the catch-up: the founder should never lose work because they closed a laptop.
   - **Touched in the last hour** belongs to a session that may still be open in another window. Leave it completely alone and say so in one line: "Left N recently-changed file(s) for the session that's working on them."

   If git isn't set up yet, skip this silently.

## Phase 2: Load the brain (read-only)

Read, in order:
1. `CLAUDE.md`
2. `reference/writing-style.md` (rules apply to all output this session)
3. Every `.md` directly in `context/` (business, you, offer, strategy, numbers, team, tech-stack), plus every `.md` under `context/businesses/` and `context/roles/` if those folders exist. **Never `context/import/`**: that's the raw dump, it can be enormous, and it holds the un-sorted originals of things that belong in `private/`. If you notice something in there that clearly shouldn't be in a shared folder, say so in one line in the report and offer to move it.
4. `docs/_index.md`, the routing table. **Read the index, not the docs.** It tells you what documentation exists and when each doc is relevant; load an individual `docs/*.md` only when the task at hand matches its condition. This is what stops a growing workspace loading everything every session.
5. If a teammate seat: `context/shared-manifest.md` decides the context list instead, plus `team/<seat>.md`
6. The last 14 days of rows across ALL files in `ledger/` (interleave by date)

## Phase 3: Report

Short and useful, not a book report:

1. **The business in one line** (proof the context loaded)
2. **Where things stand**: the 2-3 most recent threads from the ledger, across everyone
3. **Anything needing attention**: unfinished work found in Phase 1, a stale-looking context doc, a backup that hasn't happened in a while
4. **Ready.**

Then get to work.

**On closing.** Most sessions never need `/log` typed by hand, because `/implement`, `/create-plan`, `/explore`, `/test`, `/new-teammate` and `/handoff` all run it themselves when they finish. Type it explicitly only when a session did real work without going through one of those, and if it gets forgotten entirely, the sweep above catches it next time.
