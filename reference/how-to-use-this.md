# How to use this workspace

Read this once. It's the whole operating manual, and it's short on purpose.

---

## What this folder actually is

Not a chatbot with your documents attached. It's a folder on your machine that Claude works inside: reading your files, running things, reaching your tools, and writing down what happened.

The difference that matters: **it remembers.** A chat window forgets you by tomorrow. This doesn't. Every session starts already knowing your business, your team, your numbers and what was decided last week, because all of that is written down in here and loaded automatically.

That's the whole idea. Everything below is just how to keep it true.

---

## The four rules

### 1. Start every session with `/prime`

Type it and press enter. It loads your business into Claude's head and tells you where things stand.

Skip it and you're talking to something that doesn't know who you are. Thirty seconds, every time, and it's the difference between a colleague and a stranger.

### 2. Ask when you're stuck. This is the important one.

You don't need to know a single command. Say what you want in plain English:

> "I need to send a proposal to a client I spoke to yesterday."
> "What did we decide about pricing?"
> "Can you even do anything with my invoices?"
> "I don't know what I'm doing here."

Claude knows what's in this workspace and will pick the right tool and use it. The commands exist to be reached for on your behalf, not memorised by you.

**The failure mode this prevents:** using this like a chat window for three weeks and never discovering it can build you an app, read your calls, or turn your spreadsheet into a database. If you're wondering whether it can do something, ask. The answer is yes more often than you'd think.

### 3. When a session gets long, `/handoff`

Long sessions eventually get woolly and Claude starts losing the thread. When that happens, or when it warns you it's running out of room, type `/handoff`. It packages up where you got to and hands you text to paste into a fresh session. Nothing is lost.

### 4. End with `/log`, though it mostly runs itself

It records what happened, checks whether anything in your context went stale, and backs it all up. Most of the time you won't type it, because it fires on its own at the end of the bigger commands.

Forget it entirely and nothing breaks. The next `/prime` notices and catches up.

---

## What lives where

| Folder | What's in it |
|---|---|
| `context/` | Your business: what it does, who you are, your offer, strategy, numbers, team, tools. Loaded every session. |
| `private/` | The drawer. Real margins, what people are paid, deal terms, personal notes. Never leaves this machine, never reaches a teammate. |
| `ledger/` | The work diary. One line per thing done, written as it happens. This is how you answer "what did we decide in July". |
| `outputs/` | Everything produced: documents, reports, decks. |
| `data/` | Files and exports you drop in for Claude to read. |
| `apps/` | Things you build here that outgrew a chat. |
| `team/` | One profile per person, once you give someone else a seat. |

You never have to file anything yourself. Say where something should go, or don't and let Claude decide.

---

## The commands, for when you want them

You don't need these. Asking in plain English gets you to the same place. They're here because some people prefer knowing.

**Every day**
- `/prime` start of a session
- `/log` end of a session
- `/handoff` when a session gets long

**Building something**
- `/explore` think an idea through properly
- `/create-plan` turn it into a plan
- `/implement` build it
- `/test` make it check its own work

Or just say **"teach me to build"** and it walks the whole thing on something real from your business.

**Everything else**
- `/import-ai-memory` pull what ChatGPT or Claude already knows about you into here
- `/new-capability` connect a tool that has no connector yet
- `/new-teammate` give someone their own seat
- `/document` write up something you built
- `/migrate` bring in another workspace you already had

---

## Connecting your tools

Connectors are built into the Claude app: **Settings, then Connectors**. Sign in once per tool and it's on. Gmail, Calendar, Drive, Slack, Notion, Stripe, HubSpot, Sheets and most other things a business runs on.

Two things worth knowing. It's an app-level setting, so a connector you turn on works everywhere you use Claude, not only here. And some need the app restarted before they show up.

If a tool has no connector, say so and Claude builds a custom one with `/new-capability`.

---

## Two habits that make the difference

**Talk, don't type.** Dictation runs about three times faster than typing, and people simply say more than they write. The richest context in here will come from you talking. This matters most in the long interview about your business, and it keeps mattering after.

**Be greedy with context.** Drop things in even when they feel messy or half-finished. Old strategy docs, a pitch deck, a client spreadsheet, a folder of SOPs nobody updated. Claude reads it all and keeps what's useful. The instinct to tidy up first is the thing that stops most people ever starting.

---

## When something goes wrong

Say what happened, in plain words. "That didn't work." "This looks wrong." "I think you deleted something."

Nothing here is unrecoverable. Every change is a save point, and Claude can undo any of it. You cannot break this folder by using it.

---

*From Liam Ottley's AI Makeover. Watch the builds: youtube.com/@LiamOttley*
