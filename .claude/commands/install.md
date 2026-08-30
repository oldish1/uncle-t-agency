# /install

> Zero to a working AI operating system. Ten steps, about three hours if you do all of it. Interactive the whole way: Claude asks, you answer, Claude builds.

## Variables

args: $ARGUMENTS (usually empty, and that's fine)

**Always check `.install-state` first, whatever the arguments are.** If the file exists and isn't marked complete, greet them back by name and resume at the first step that isn't done. Never restart a founder who already answered forty minutes of questions. `START-HERE.md` promises them exactly this, so it has to hold.

---

## FOR CLAUDE, how to run this

- **This is a conversation, not a script.** Explain before doing. Wait for confirmation between steps. Never two steps without a stop.
- **Assume a non-technical founder** who may never have used Claude Code before. Smart person, zero coding. No jargon without a plain-English translation in the same sentence.
- **The pattern for every step:** explain → confirm → act → verify → celebrate → stop.
- **No error dumps, ever.** Name the problem simply, fix it together, or park it without blocking the rest.
- **Track state.** After each step, rewrite `.install-state` in exactly this shape, so any later session can resume without re-asking anything:

  ```
  format: 1
  founder: <name>
  os: mac | windows
  plan: pro | max | team | enterprise
  structure: <the Step 2c decision, one line>
  steps:
    0: done | skipped | pending
    1: done | skipped | pending
    ... through 10
  keys: <platforms whose keys are in .env and tested>
  tools: <platforms connected via connectors>
  runtime: ready | skipped | pending
  remote: <github url, or none>
  notes: <anything a resuming session needs, e.g. git still downloading>
  ```

  A step marked `skipped` is finished, not pending: never re-offer it. When Step 10 lands, add `complete: yes`. Record each key by **name only, never the value** (`keys: firecrawl, supadata`) and each linked tool the same way, so a resuming session never asks again for a key that already works.

  **On resume, check the file against reality and let reality win.** `git log`, `git remote -v`, does `.env` exist and what's in it, is `context/` populated, does `context/tech-stack.md` show anything actually wired. Then rewrite `.install-state` to match what you found. A half-finished step often leaves real traces the file never recorded, and **you must never ask a founder something you could have looked up.** Re-interviewing someone who already gave you forty minutes is the moment they close the laptop for good.

  If the file has no `format:` line it was written by an older session: read it best-effort, say in one line what you recovered, confirm the resume point with them, and rewrite it in the shape above. Never restart because you couldn't parse it.

- **Write a ledger row as each step lands, not at the end.** After every step, append one row to `ledger/<founder-first-name>.md` (create it at Step 1, once you know their name), per the standing rule in CLAUDE.md. By Step 9 they should be looking at eight or nine rows of their own morning, which is the entire point of that demo. An install that only logs at the end shows them an empty file.
- **Maintain CLAUDE.md as you go.** Every step that changes what the workspace can do ends with a CLAUDE.md touch-up. The constitution always matches reality. This is continuous, never a step of its own.
- **Signup links and keys come from `reference/getting-keys.md`.** Follow its rules exactly: sign-up link first on its own, wait for them to confirm they're in, then the key page. Never both links at once. The Glaido, Firecrawl, Supadata and Apify signup URLs in that file are Liam Ottley's affiliate links. Say that plainly before sharing one; never remove or replace the tracking. If a console has moved, find the current path, use it, and update that file.
- **Keys never go into chat.** Open `.env` in the editor, point to the empty variable, and have them paste the value there themselves. Wait until they say it is saved. You may read the file to use the key, but never quote, print, log or repeat the value. `.env` is git-ignored and must stay that way.
- **Test every key the moment it lands.** `getting-keys.md` has a verified test per platform. Run it, and don't call the step done until it comes back clean. A mistyped or half-copied key is the most common thing that quietly breaks a workspace a week later.
- **Voice matters.** Encourage talking over typing. Celebrate real milestones in one line, not confetti.
- All prose you write during this install follows `reference/writing-style.md`.
- **Timings below are guidance, not a clock.** They exist so you know what deserves the most room. Step 2 is the one that pays for everything else.

---

## STEP 0, Three questions (2 min)

No header, no ceremony. Ask these three before anything else, because each one changes what happens next.

0. **Check the permission mode before anything else.** Say it plainly: *"Keep this on Auto if you have it, or Ask permissions if you don't. I'll explain what I'm doing and you'll still control anything sensitive."*

   Never ask a founder to enable Bypass permissions on their normal computer. Anthropic reserves that mode for sandboxed containers and virtual machines. If it is already enabled, ask them to switch back to Auto or Ask permissions before continuing.

1. **"Mac or Windows?"** Remember it. Every command you give them from here has to match. On Windows: PowerShell not Terminal, Git for Windows not Xcode tools. If anything Unix-only comes up later, say so plainly and give them the working alternative rather than letting them hit an error.

2. **"Do you already have a folder on your computer that Claude reads at the start of every session?"**
   - **No** → the normal path. Continue to Step 1. This is nearly everyone, including people who are very good with AI but run it all out of a chat window.
   - **Yes** → ask one more: *"Does it load context about your business automatically, and does it keep a record of work that survives between sessions?"*
     - **Yes again:** they have a real system, and sitting them through a beginner install wastes them. **Eject now:** *"You don't need this install. What's more useful is comparing what you've already built against what's in here and taking whatever's worth taking. That's a different command."* Then hand off to `/migrate` and stop. Do not continue to Step 1.
     - **No:** it's a folder with a few prompt files in it, which isn't the same thing. Come back to Step 1 and treat that folder as an import in Step 2.

3. **"Which paid Claude plan are you on: Pro, Max, Team or Enterprise?"** If they're not sure, they'll find out at the first command. If they're on the free plan, say it straight: the Code tab needs a paid plan, here's `claude.ai/upgrade`, and nothing below will work until that's sorted. Better to know now than at step 5.

4. **Then start the git download before you do anything else.** Don't announce this as a step, just do it: run `git --version` quietly.

   - **If it returns a version,** say nothing and move on.
   - **If it doesn't,** this is the one thing that has to start now, because it's a one to two gigabyte download and Step 4 can't happen without it. Say so plainly: *"One thing to kick off in the background before we start talking. It's a big download and I want it running while we do the interesting part."* Then:
     - **Mac:** run `xcode-select --install`. A box appears. Tell them to click **Install** and then ignore it completely. It'll finish while you do Step 2.
     - **Windows:** try `winget install --id Git.Git -e --source winget` first. It installs silently with no dialog and no clicks, and it works on Windows 10 1709 and later. If winget isn't recognised, fall back to https://git-scm.com/download/win, run the installer, accept every default. **Either way they must close and reopen PowerShell afterwards**, or `git` still won't be found even though it installed fine. That one catches everybody.
   - Either way, do **not** wait for it. Note in `.install-state` that git was still installing, carry on to Step 1 immediately, and re-check quietly at the top of Step 4.

   The whole point is that the download runs through the forty-minute context interview and is finished before anything needs it. Never let a founder sit and watch a progress bar.

Write `.install-state`. **STOP.**

---

## STEP 1, What we're building (8 min)

Print:
```
════════════════════════════════════
  AIOS SETUP, Step 1/10: The shape of it
════════════════════════════════════
```

You're painting the whole picture before they type anything. Keep it to a few short paragraphs and check they're with you at the end.

**The gap they're in.** They already have two things: tools that do work when triggered, and chats where they think out loud with something that forgets everything by tomorrow. Neither of those is their business knowing itself. What's missing is the layer underneath both, a place where the business is written down in a form the AI reads automatically. That's what this folder is.

**The layers, bottom to top.** Context (what the business is). Data (the numbers and records it runs on). The workspace and its integrations (this folder, reaching your actual tools). Then what you build on top: exploring it by hand, turning repeated work into skills, handing skills to agents that run without you, and eventually small apps with a screen.

**Today is the bottom four.** Context, data, integrations, and using it. Everything above that gets easier once these exist, and none of it works without them.

**What changes.** Right now they re-explain their business every time they open a chat, they bounce between a dozen tabs, and they type when they could talk. All three of those are hours a week, and all three go away.

Then one question to make it theirs: **"what should I call you?"**

Write state. **STOP: "Ready for the part that does the work?"**

---

## STEP 2, Your business, in my head (40 min)

Print the step header (2/10: Your business, in my head).

**The step everything else stands on.** Say that out loud, and say you'd rather they took the time here than rushed to the fun bit. The order matters: **feed it everything first, analyse, then ask questions to fill the gaps.** Interviewing before reading wastes their breath on things you could have read.

**Offer voice before the long interview.** This step is much easier to speak than type. Ask whether they want to keep typing or install Glaido for voice dictation. If they want Glaido, use its signup link from `reference/getting-keys.md`, disclose that it is Liam Ottley's affiliate link, wait while they install it, and test one dictated answer. If they prefer typing, move on immediately; Glaido is helpful, never required.

### 2a. Get the raw material in (5 min of their effort, then it runs in the background)

1. **"Which do you use more, ChatGPT or Claude?"** Then run `/import-ai-memory`. It hands them a prompt to paste into that app, the model writes out everything it knows about them, and they paste the result back here. Two minutes, and it's months of them explaining their own business in their own words. Say that in one line so they know why it's worth doing.

   Don't send them to the data export. It emails a link that can take hours, and on a business or enterprise plan it's usually gated behind an admin who isn't in the room. Mention once, at the end, that the real export exists if they ever want the full transcripts.

2. **"Now throw everything else into `context/import/`."** Be expansive about this, people are too conservative: business plans, pitch decks, an old strategy doc, their offer or pricing sheet, a services page, onboarding docs, SOPs, a spreadsheet of clients, financial summaries, brand guidelines, anything half-finished. **Nothing is too messy.** They don't need to organise it, that's the point of the folder.

   Say the safety line as you ask, because you're asking for their real documents: *"That folder stays on this machine. It's git-ignored, so none of it reaches the backup or a teammate. I read it, pull out what belongs in the shared context, and the originals stay put."* That's what makes it safe to be greedy here.

3. **"And any links."** Their website, their LinkedIn, Instagram, YouTube, X, a Substack, their booking page, a podcast they've been on. Anything public that describes what they do.

### 2b. Analyse it all before asking anything

Read every file in `context/import/`, then research the links. Actually go and look at the sites, don't guess from the URL.

Then **tell them what you learned**, in a few sentences, before you ask a single question. This does two jobs: it proves you actually read it, and it exposes what's wrong so they correct you rather than reciting things you already know.

### 2c. Decide the shape before writing anything

A real consulting moment, and don't skip it just because it's a conversation rather than a task.

**"How many businesses am I setting this up for?"**

- **One business:** the default flat `context/` structure. Move on.
- **Two or more:** work out the right shape together, out loud. The failure mode to avoid is ten near-identical docs per business, which nobody maintains and which makes every session load noise. Options to walk with them:
  - **A shared top level plus a folder per business.** `context/` holds what's true across all of them (who they are, how they work, the shared team) and `context/businesses/<name>/` holds only what differs. This is usually right.
  - **One primary plus light satellites,** where one business gets the full treatment and the others get a single page each. Right when there's one real business and a couple of side projects.
  - **Fully separate workspaces,** if the businesses share nothing and different people work on each. Say so honestly if that's the answer; it's better than a bloated single workspace.
- Whichever you land on, **write down why** in CLAUDE.md so the next session doesn't relitigate it.

### 2d. The team pass (required)

Not optional, and worth more than people expect. For each person: **name spelled correctly, their email, their role, and a short paragraph on what they actually own.**

Say why: this is loaded every session, so the workspace stops saying "your team" and starts saying "ask Sarah, she owns onboarding". It's also exactly what `/new-teammate` reads later to build someone a seat, so getting it right now saves that conversation twice.

If the team is large, **the core people only.** Anyone who'd be in the room for a decision.

### 2e. Now the questions

Only the gaps. One question at a time, digging where an answer is thin. Skip anything the documents already answered, and say you're skipping it.

- *The business:* what it does in their words, who the customers are, who the ideal one is specifically, what's sold and roughly at what price, how customers find them, what makes them different.
- *The founder:* their role, where the time actually goes, what decisions land on their desk, what they want off their plate first.
- *The strategy:* the two or three current priorities, what success looks like in three to six months, what's undecided.
- *The numbers:* what they track, roughly where things stand, where those numbers live.

### 2f. The drawer

"Anything you wouldn't hand a brand-new hire on day one, real margins, what people are paid, deal terms, personal notes, lives in `private/`. It stays on this machine, never syncs, never reaches a teammate. From everything you've told me, what belongs in there?" Split it: full detail into `private/`, the team-safe version into `context/numbers.md`.

### 2g. Write, read back, correct

Write the context docs to the structure agreed in 2c. Thirty to eighty lines each, clear and scannable. Then read a short summary of each back: "does this capture it? what's off?" Correct until they say yes.

Close by stamping CLAUDE.md: company name, one-liner, their name, currency, timezone, the context structure decision, and any standing instructions.

Verify before you call this done, and verify by looking rather than by remembering:

- Every context file populated, team included, readback approved.
- **`grep '\[' CLAUDE.md` comes back empty of placeholders.** If `[COMPANY NAME]`, `[FOUNDER NAME]`, `[BUSINESS ONE-LINER]` or `[CURRENCY]` are still sitting there, Step 2 is **not** done. This is the one that slips: the interview goes well, the docs get written, and the constitution that loads every single session still doesn't know the company's name.
- The Step 2c structure decision is written into CLAUDE.md, not just into `.install-state`.

Update `.install-state`. **STOP.**

---

## STEP 3, Proof (5 min)

Print the step header (3/10: Watch this).

Short, and it lands hard. Don't over-explain it, just do it.

1. "Close this session and open a fresh one." Wait for them.
2. "Type `/prime`." It loads the brain and reports where things stand.
3. "Now ask me something you'd normally have to explain from scratch. Anything about your business."

Answer with full context. Let the moment sit. Then name what just happened in one line: a brand-new session, no explaining, and it already knew.

Update state. **STOP.**

---

## STEP 4, Save points and backup (15 min)

Print the step header (4/10: Nothing you do here is ever risky).

Teach, check they've got it, then act. After each idea, ask lightly: "in your own words, what does that give you?" One sentence back and you move on.

1. **Save points.** "Git gives this folder save points, like a game. Every version of every file, kept. Nothing you do here can't be undone." Re-check `git --version` quietly. It should already be there, either because they had it or because Step 0 started the download an hour ago. If it's still going, park this step, carry on to Step 5, and come back: never make the room wait on one machine. If it never started (they skipped Step 0 or clicked the wrong thing), start it now per Step 0 and do Step 5 while it runs. Then `git init`, main branch. Show them `.gitignore` and say what it means: "your keys and your private drawer are physically excluded. They cannot reach the backup." First commit, narrated as save point one.

2. **Offer the cloud copy, do not make it a prerequisite.** "GitHub is an optional private backup, and later, where teammates can connect. The workspace already works without it." If they want it, walk the signup click by click. Then check `gh --version` before promising the device flow.

   - **Windows:** if `gh` is missing, run `winget install --id GitHub.cli`, then restart the terminal inside Claude before continuing.
   - **Mac:** if `gh` is missing and Homebrew exists, run `brew install gh`. Otherwise open `https://cli.github.com/` and use the official installer, then restart the terminal inside Claude.

   Run `gh auth login --web --git-protocol https`. GitHub opens a browser-based device flow and stores the credential in the system credential store. Never ask them for a personal access token. Create a private repository, connect the remote, and push.

3. **Prove it works, don't just claim it.** Make a trivial change, commit it, push it, and have them refresh github.com to watch it appear. They should see the loop close with their own eyes once.

4. **Then take git off their plate, explicitly.** Say it plainly: *"That's the last time you'll think about any of this. Branches, commits, merges, conflicts, none of it is your job. I run all of it. If two people ever edit the same document, I'll read both versions and just ask you which bits to keep, in plain English. You will never see a merge conflict."* This matters more than it sounds: git is the single most intimidating thing in the kit and the whole design is that they never touch it.

5. **Mention the GitHub habit.** From here, whenever a developer tool offers "Continue with GitHub", take it. One identity, one place to turn on two-factor, and the same pattern their teammates will use.

6. **The trust moment.** "Open github.com and look. Your files are there. Now notice what isn't: no private folder, no keys, and none of the raw documents you dumped in this morning. The drawer stayed home."

   Before you say that sentence, **check it's true.** Run `git ls-files` and confirm nothing from `private/`, `context/import/` or `.env` is tracked. If any of it is, don't say the line: fix it first (`git rm -r --cached <path>`, confirm it's in `.gitignore`, commit), then say it. Never make this promise on trust.

Skippable if they're nervous or short on time, and say so. If skipped, record it; `/log` will still commit locally and nudge occasionally. No later step may fail just because GitHub was skipped.

Verify: clean `git status`, confirmed push, or a recorded skip. Update state. **STOP.**

---

## STEP 5, Your tools, connected (15 min)

Print the step header (5/10: Reaching your actual world).

1. **Frame it, because this is the point of the whole workspace.** *"Everything your business runs on is about to be reachable from this one folder. Your context is here, your data is here, and now your tools are here too. The goal is that you stop leaving: no bouncing between twelve tabs to answer one question."* Each supported tool takes one normal sign-in through Claude Desktop; there is no separate integration platform to install.

   Be greedy here. **Connect as much as they'll let you.** Every tool that stays outside is a tab they'll keep opening, and each one they connect makes everything downstream better: the research, the apps they build later, the agents.

2. **Use the connectors built into the Claude app.** Nothing to install and no key to paste. In the Claude Desktop app: **Settings → Connectors**, then Browse or Add. They sign in to the tool once in a normal OAuth window and it's on. It works the same on Mac and Windows.

   Do this with them on screen rather than describing it. It's a settings pane and a sign-in box, and watching someone find it is faster than reading them directions.

   Once a connector is on in the app, it's available to you here. Check what you can actually reach before promising anything, and if a connector needs the app restarted, say so and wait.

3. **Which tools.** "What runs this business day to day? Everything: CRM, payments, booking, email, project tool, spreadsheets." Write the full list to `context/tech-stack.md`, and mark each one connected, available, or not covered. Then: "**which two or three do you actually live in?**" Turn those on now, one sign-in each.

4. **Prove one.** Run a real request against a real account: their last five deals, this week's bookings, today's unread. Their data, on screen, from here. Land it: "that's your [tool], reachable from this folder, permanently."

5. **Gmail, Calendar and Drive** are connectors too, not a Google Cloud project. One sign-in each, and no OAuth app to set up.

6. **When a tool isn't there.** Some won't be, especially niche or regional platforms and anything internal. Don't stall on it and don't make it the story of the step. Note it in `context/tech-stack.md` as not covered, finish connecting what is there, and tell them `/new-capability` builds a custom integration for it on any future day. One sentence, then move on.

Update `context/tech-stack.md` and CLAUDE.md's routing. Update state. **STOP.**

---

## STEP 6, The utility stack (20-25 min)

Print the step header (6/10: Eyes and ears on the outside world).

**Set up the local runtime first, then the two core research accounts.** Apify and X search are optional powerups, not blockers.

**Give them the reasoning before the first signup, because otherwise this feels like admin.** Two things this buys them:
- **Now:** their workspace can see the outside world properly. Any site, any video, any platform, pulled in clean rather than guessed at. It's also what makes deep research work at Step 9, and that's the single most impressive thing in the kit.
- **Later:** these same connections drop straight into whatever they build. When they make an app, an automation or an agent in a month, the scraping is already wired up. They won't be starting from a blank page and hunting API docs; they'll be assembling from parts they already own.

Do them in order and land each one before starting the next.

### 6a. Make the shipped research tools runnable

The template includes Python research clients, so verify the runtime instead of assuming it exists.

1. Run `uv --version`.
2. If `uv` is missing, explain that it is the small runtime manager that keeps this workspace's tools isolated from the rest of their computer. Ask before installing it, then use the official installer for their OS:
   - **Mac:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - **Windows:** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
3. Restart the terminal inside Claude if `uv` is not immediately on PATH.
4. Run `uv venv --python 3.12`, then `uv pip install -r requirements.txt`. `uv` downloads Python automatically if the machine does not already have it.
5. Verify with `uv run python -c "import requests, dotenv; print('runtime ready')"`.

Do not mark `runtime: ready` until that exact check passes. If they decline the install, record `runtime: skipped`, explain that the workspace and five beginner commands still work, but the bundled research clients will wait until they add the runtime.

### 6b. Add the research accounts

**How to run each one** (the rules are in `reference/getting-keys.md`, follow them exactly):
- Give the **sign-up link on its own**, then stop and wait for them to say they're in. Never hand over both links at once.
- Then the key page. Open `.env`, point to the empty variable, and have them paste the key into the file themselves. Never put it in chat.
- **Then run that block's test.** Don't move to the next tool until it comes back clean.
- Give each one its thirty-second why as it lands, in terms of *their* business.

1. **Firecrawl.** Reads any website properly: JavaScript-heavy pages, bot-protected sites, PDFs. The upgrade over the basic fetching built into Claude Code. When it lands, update CLAUDE.md's routing so all web research goes through it from now on, and tell them you've done that. Live test: scrape a competitor's pricing page.

2. **Supadata.** Turns video into text. YouTube, TikTok, Instagram, X, plus YouTube search. Live test: pull the transcript of a video in their niche.

3. **Offer Apify only if they need a walled platform.** It reaches Instagram, TikTok, LinkedIn, Google Maps, marketplaces and review sites. If one of those matters to the business, set it up and test a tiny relevant pull. Otherwise record it as skipped and move on.

4. **Offer X search only if current X conversation matters.** This one is paid with no free tier, so say that plainly. Everything else works without it.

**Zero-setup wins, mentioned as you go:** writing style is always on, so nothing this workspace produces sounds like a bot. Academic and Substack search need nothing at all. Demo one quickly on their industry.

**If someone is falling behind,** finish the runtime and get either Firecrawl or Supadata working on one real source. The other accounts can be added on the day they are needed.

Update CLAUDE.md's routing as each lands. Update state. **STOP.**

---

## STEP 7, Make it do something (15 min)

Print the step header (7/10: Now put it to work).

Step 3 proved it knows them. This proves it can act.

1. "Fresh session again. `/prime`."

2. **Build the menu from what they've actually connected**, not from a generic list. You know their tools from `context/tech-stack.md` and you know their business from Step 2, so the options should be specific enough that they recognise their own week in them. Offer three or four, one line each:
   - *If a CRM or pipeline is connected:* pull the last thirty days and tell them what's stalled.
   - *If email is connected:* draft the follow-ups for everyone who went quiet.
   - *If a spreadsheet or finance tool is connected:* turn last month into a one-page PDF.
   - *If they're content-led:* pull a competitor's recent videos and summarise what's working.
   - *Always available:* build a deck from the strategy doc written an hour ago.

3. **Then get out of the way and let them watch.** This is the moment the room goes quiet, so don't narrate over it. The output has to be a real file or a real page they can open, not a wall of chat.

Update state. **STOP.**

---

## STEP 8, The branch (25 min)

Print the step header (8/10: Your pick).

Three lanes, and **the honest default is to skip straight past this if nothing here fits.** Don't manufacture work. If they haven't got spreadsheets and their tools are already connected, send them to Step 9 early and give the room back the time.

### Lane A, get your data into one place

For anyone running the business out of spreadsheets. **Look first, then offer.** If Sheets or Drive is connected, go and see: how many spreadsheets, how many touched recently, which ones are doing a database's job. Come back with the finding, not a question. "You've got thirty-four sheets, nine touched this month, and three of them are really a customer database wearing a spreadsheet costume."

Then:
1. Supabase, per `reference/getting-keys.md`. Use GitHub sign-in if they connected it in Step 4; otherwise use an available email or Google sign-in. The database lane cannot depend on the optional backup lane.
2. Pick two or three sheets that matter.
3. **Audit before you migrate.** Profile them: columns, types, row counts, duplicates, blank columns, inconsistent dates, mixed types in one column. Show them what you found. This alone is worth the step, and it's worth doing even if the database doesn't happen.
4. Propose a schema, including how the sheets relate to each other, and get a yes.
5. Build the tables, import, verify the row counts match, and report what you cleaned versus what you left alone.
6. Then ask it something the spreadsheets couldn't answer. That's the payoff.

They never touch Supabase directly. You build it, you move the data.

### Lane B, connect the rest

For anyone whose problem is tool sprawl rather than spreadsheet sprawl. Work down `context/tech-stack.md`, adding a connector for each and testing it live on their real data. Stop when they've got what they need.

### Lane C, or just move on

Take something genuinely on their plate this week and do it together. Or, if they'd rather push on, go to Step 9. Finishing early with a working workspace beats padding the hour.

Update state. **STOP.**

---

## STEP 9, How the whole thing runs (12 min)

Print the step header (9/10: How this stays alive).

They've run `/prime` twice and had `/log` fire on its own by now, so most of this is naming what they've already felt. Walk the whole system once, so they know what exists and when to reach for it. Keep each one to a couple of sentences.

**The rhythm**

- **`/prime`,** start of every session. Pulls the latest, catches up anything a previous session left unfinished, loads the brain, reports where things stand. If they only remember one command, this is it.
- **`/log`,** end of a session. Sweeps anything unlogged, checks whether a context doc drifted, saves and backs up. **Tell them plainly they will rarely type this**, because it fires automatically at the end of `/implement`, `/create-plan`, `/explore`, `/test`, `/new-teammate` and `/handoff`. It's a workhorse that mostly runs itself.
- **`/handoff`,** when a session gets long and the thread frays. Packages the state and hands them the exact text to open a fresh session with.
- **The ledger.** Rows are written as work happens, not at the end. Point at their own file and show them today's rows. Then the payoff: in six months this answers "what did we decide about pricing in July" without anyone remembering.
- **The safety net.** If they close the laptop mid-session and never log, the next `/prime` notices, writes the missing rows, saves and backs up on its own. **Nothing is lost by walking away.**

**The rule that matters more than any command**

Say this one slowly, because it's the difference between a workspace they use and one they abandon:

> *"You don't have to remember any of these. If you're stuck, or unsure, or you don't even know whether something's possible, just say it in plain English. 'How do I…', 'can this even…', 'I don't know what I'm doing.' I know what's in this folder and I'll pick the right tool and use it. The commands are for me to reach for, not for you to memorise."*

Then **prove it on the spot.** Ask them for something they'd normally assume needs a specialist, take it, and do it. One real example lands this harder than the sentence does.

Tell them the failure mode plainly, because it's the common one: people use this like a chat window for three weeks and never find out it can build them an app, read their calls, or turn a spreadsheet into a database. The way out is asking.

Point at `reference/how-to-use-this.md` as the written version, and say they can ask for it any time rather than going to find it.

**Building things**

- **`/explore`** to think an idea through, **`/create-plan`** to write the plan, **`/implement`** to build it, **`/test`** to make it check its own work. Say "teach me to build" any time and it walks the whole flow on something real.
- **`/new-capability`** when a tool has no connector: it researches that platform's API and builds the integration.
- **`/new-teammate`** when someone joins: it writes their role, decides what they can and can't see, and mints their onboarding pack.
- **`/import-ai-memory`** any time they want more of what ChatGPT or Claude already knows about them pulled in. They've already run it once in Step 2; it's re-runnable whenever their thinking has moved on.

**Under the hood, so they know it's there and then forget it**

- The workspace **documents itself** as they build, and keeps an index so sessions load the right doc rather than everything.
- **Writing style** is always on, so nothing it produces sounds like a bot.
- **Git** is entirely handled. They never touch it.

**Then the model consoles.** Not a signup exercise, just knowing where things are for the day they build something.

- **Anthropic**, `platform.claude.com/settings/keys`. The strong models, and what agents run on.
- **OpenAI**, `platform.openai.com/api-keys`. Mainly Whisper, so call recordings and voice notes into text.
- **Gemini**, `aistudio.google.com/apikey`. Cheap and multimodal, good for volume and for reading images, audio and video.

All three are in `reference/getting-keys.md` with the exact routes. Say plainly that **none of these are needed for the workspace to run**; it works off their Claude subscription. These are for what they build on top.

**Then stop and take questions.** This section always opens a lot of them, and answering three real ones here is worth more than finishing on time.

Update state. **STOP.**

---

## STEP 10, Where to from here (5 min)

Print the step header (10/10: Done).

Quick health check as a green list: context populated, team loaded, prime accurate, backup live, tools connected, first real output made.

Then close with options rather than a goodbye:

```
Your AIOS is live. Where to from here:

→ RECOMMENDED: run /task-audit. It maps where your week goes,
  finds the best work to remove, delegate, augment or automate,
  and gives you one specific idea to take into /explore.

→ Or just use it for a week. /prime to start, /log to end.
  Anything still on your setup list is one sentence away.

→ "teach me to build". Now your tools are connected, I'll walk you
  through building your first app: /explore → /create-plan →
  /implement → /test, on something real from your business.

→ "/new-teammate", when you're ready to give someone their own seat.
  One command writes their role, decides what they can see, and mints
  their onboarding pack.

→ "connect my [platform]", any tool, any day.
```

Mark `.install-state` complete. Write the install's rows into `ledger/<name>.md`, commit, push.
