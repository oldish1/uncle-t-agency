# How to use the brain

The brain is this workspace: folders of plain files that Claude reads at the start of every session. You never need to learn the file names. You can always just ask.

## See what's inside (four ways)

1. **Ask Claude.** "What's in todo?", "show me the Chales plan", "what do we know about pricing?" Claude opens the right file and tells you in plain English. This is the easiest way.
2. **The brain diagram.** https://claude.ai/artifact/KRgZRG18Dt6LVaAKnxeNna. Tap a part to see what's in it and where it stands.
3. **GitHub in your browser or phone.** github.com/oldish1/uncle-t-agency. Folders are listed on the page, tap one to open it, tap a file to read it. Use the branch menu to pick the branch (the brain is on `ccr-333f61cf-fmh4ca` until it's merged into `main`).
4. **The Claude app.** Files Claude writes in a session can be opened from the session's file list.

## The folders in one line each

| Folder | What it is |
|---|---|
| `CLAUDE.md` | The rules. Loads every session |
| `context/` | What the business is, offers, strategy, numbers, how Lexi works, `brain.md` map |
| `ledger/` | The work diary, one line per piece of work |
| `todo/` | Everything still to do, by area. Start at `todo/README.md` |
| `clients/` | One folder per client: profile, deal, conversations, results |
| `plans/` | Build plans |
| `outputs/` | Things we made: pitches, reels, reports, handoffs |
| `reference/` | Research, writing rules, how-to guides |
| `apps/` and `scripts/` | Things built here |
| `.claude/skills/` | Recipe cards Claude uses (sales-coach, seo, lexi-onboarding and more) |
| `.claude/commands/` | Buttons you press: `/prime`, `/log`, `/seo`, `/new-client` |
| `data/` | Exports and measurements (visibility checks) |
| `private/` | Margins and personal matters. Never syncs, stays on one machine |

## Add things to the brain

You say it in plain English. Claude files it and updates the map.

| You have | Say | It goes to |
|---|---|---|
| A new client | `/new-client <name>` | `clients/<slug>/` |
| What a client or prospect told you | "Add this to <client>'s conversations" | `clients/<slug>/conversations.md` |
| A real result (reviews, bookings) | "Log this for <client>: 12 reviews" | `clients/<slug>/results.md` |
| A fact about the business | "Add to context: <fact>" | the right file in `context/` |
| A document, export or photo | Drop it in the chat and say where it belongs | `data/`, `clients/` or `outputs/` |
| Something to do later | "Add to my to-do: <thing>" | the right file in `todo/` |
| A method you keep repeating | "Turn this into a skill" | `.claude/skills/<name>/` |
| A whole new area (for example a new venture) | "Make a folder for <thing> in the brain" | a new folder plus a line in `context/brain.md` and `CLAUDE.md` |
| Something private (margins, personal) | "Put this in private" | `private/` (this machine only) |

## Data equity (the data only you have)

Dan Martell's idea: AI tools are the same for everyone. What makes your agent better than anyone's is data nobody else has. For Uncle T that is:

- what Cape Town salon owners actually say about missed messages, no-shows and burnout
- real before and after numbers from CHALES and every client after her
- how Lexi was built, what broke, what fixed it
- your own sales conversations, wins and losses
- your pricing, offers and what got replies

**What's in the brain today:** the business, offer, strategy and pricing in `context/`. 497 ledger rows of everything built. How Lexi works and every lesson learned. Competitor and salon-challenge research. CHALES' profile, baseline numbers and plans (now in `clients/chales-hair-boutique/`).

**What is NOT in the brain yet, and where it lives:**
1. Your sales conversations: in the Pipeline Sheet's Conversations tab. Fix: after each chat, tell Claude "debrief" and it writes the lessons into `outputs/sales-dojo/log.md` and `clients/<slug>/conversations.md`. Raw phone numbers stay in the Sheet, not in the repo.
2. Prospect statuses: in the Pipeline Sheet. The Chief of Staff counts them each Monday.
3. The Lexi template file: `private/lexi-client-template-blueprint.json`, on your machine only. If your machine is lost, it's lost. Keep a backup copy.
4. Chanté's past clients and what they say: not collected yet. The win-back messages and Google reviews are how that starts.
5. Real results numbers beyond the first baseline. Fix: first Monday of each month, `/seo monthly chales` adds a row to `results.md`.
6. Lexi's live prompts and routes: they live inside Make. The sanitised template plus `context/lexi.md` are the copy.

**Rule of thumb:** if only you know it, write it down in the brain the same day. If it's a secret, `private/`. If it's a customer's personal detail, keep it out of the repo.

## Pull request, in plain English

When Claude works, it works on a side copy of the brain called a branch, so your main copy can't be broken. A pull request is the request to fold that side copy back into the main copy. You get a page on GitHub showing what changed, and you press the green Merge button if you're happy. Until you merge, new sessions (which start from the main copy) don't see the new work.

## One brain, one branch

Start new sessions from `main`. After a merge, the old side branches can be ignored. Before saying something doesn't exist, Claude checks `git branch -r` and the live site.
