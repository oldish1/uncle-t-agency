# Skills, in plain English

A skill is a recipe card for Claude. It's a folder with one file (`SKILL.md`) that says: when to use this, the steps, the traps, and any helper scripts to run. Claude reads the card when the job matches and follows it, so the work comes out the same way every time instead of being figured out from scratch.

**Why it feels like a superpower.** Everything we worked out in a long session (what to check, what we got wrong, the report format) normally disappears when the session ends. A skill keeps it. The next session, or a teammate, starts from the finished method instead of the first guess.

**Skill vs command.** A command (`/seo`, `/log`) is a button you press to start something. A skill is the know-how behind it. Commands live in `.claude/commands/`, skills in `.claude/skills/<name>/SKILL.md`. A skill can also run on its own when Claude sees a matching request, without you typing anything.

**What makes a good skill.**
- A job you'll do 3 or more times.
- Steps you can write down, with real examples of good output.
- The mistakes made last time, written as rules.
- Helper scripts for the boring, exact parts (`scripts/seo_check.py`).

**What doesn't need one.** One-off questions, and anything that changes every time.

**When it loads.** New skills show up in a fresh session (start a new one after we add one). Claude sees each skill's short description first and loads the full card only when it's needed, so having many skills doesn't slow anything down.

**Turning a long session into a skill.** After a session that produced a method, ask: "turn this into a skill". Claude pulls out the steps, the mistakes and the output format, adds a script if some part is mechanical, and tests it once on a real case. The `seo` skill came from the CHALES sessions.

Skills in this workspace: see `.claude/skills/`. Commands: `.claude/commands/`.
