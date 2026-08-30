# Log

> End-of-session ritual. Records the work, keeps the context honest, saves and backs everything up. Run it when you finish a chunk of work, always at the end of a session, and any time you've done something worth keeping.

## The three checks, in order

### 1. Ledger completeness

**You are the backstop here, not the mechanism.** Rows should already have been written as the work happened, per the standing rule in CLAUDE.md. Walk what happened this session (files created or changed, decisions made, things built or shipped) and check each one has a row in `ledger/<seat>.md` (your seat's file, never anyone else's). Append only what slipped through, newest at the top:

```
- YYYY-MM-DD HH:MM · <seat> · <area>/<type> · <one-line summary>
```

Types: `build` (something made), `decision` (a choice that shapes future work), `ship` (something went out), `research`, `note`. Area is whatever part of the business it touched (content, sales, ops, finance, workspace...). A pure-conversation session with nothing produced needs no rows, say so and skip to check 3. If you find you're writing more than a couple of rows here, the passive rule isn't firing during the session; say so plainly so it gets fixed.

### 2. Context drift

Did anything this session change what the context docs say? A strategy shift, a new offer, a team change, a tool added? For each drift, propose the specific edit ("strategy.md still says X; today you decided Y, update it?"). Apply on approval, never silently. If something private landed in a shared folder, flag it and offer to move it to `private/`.

And the constitution: if the workspace gained a capability or changed shape this session, make sure CLAUDE.md says so (tool routing lines included).

### 3. Save + back up

```bash
git add -A
git commit -m "<type>: <plain one-line summary of the session>"
git pull --rebase --autostash
git push
```

- Narrate in one line: "Saved and backed up: <summary>."
- If the push is rejected because a teammate pushed first: pull-rebase again and retry, up to 3 times, narrated simply ("Sarah saved work while we did, merging, done.").
- **If a real conflict appears** (same doc edited by two people): never show conflict markers. Read both versions, explain the difference in plain English, propose merged text that keeps both intents, apply on approval, continue.
- If there's no remote yet (backup phase was skipped in the install): commit locally, then remind gently, "your work is saved on this machine, but not backed up to the cloud yet. Say 'set up my backup' any time."
- If offline: commit locally, say so, move on. The next /log pushes it.

## Report

One short block: the ledger rows written, any context updates applied, and the save/backup status. Then: "see you at the next /prime."
