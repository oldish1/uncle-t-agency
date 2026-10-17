# Handoff: uncletsautomation.co.za website, Mobbin MCP, Meta verification

Written 2026-10-17. Branch: `claude/clever-bardeen-z3eams`.

## What we were working on and why

Theo wants more paying clients. Two things block the way: Rex (his WhatsApp commander agent) is stuck on Meta's free test number because the Meta business verification for Uncle Ts Automation was **rejected**, and he has no award-winning showcase site. One build fixes both: a real website on **uncletsautomation.co.za** (Meta wants a site on a domain the business owns) built by the Web Builder skill.

## Where we got to

**Done today**
- Rex is LIVE and answering Theo on WhatsApp via Meta's test number (+1 555 139 8942, Phone Number ID 1019478207918336, test WABA / messaging account 794125367100266). Make scenario 7638753, webhook hook 3920941. See `apps/rex/README.md`.
- Isolated Rex's test account: removed the Rags To Riches app from it (Luna was answering), subscribed only Uncle T Agents. Created system user Rexbot (Employee) with only the Uncle T Agents app, the test WhatsApp account and the test messaging account.
- Web Builder skill written: `.claude/skills/web-builder/SKILL.md`, research in `reference/research/2026-10-17-award-winning-websites.md`.
- Found the Meta business verification status: **rejected** ("Couldn't be verified"), submitted 12 Sep as a sole proprietor with a claude.ai link as the website.

**In progress**
- The website for uncletsautomation.co.za (not started, this is the next job).
- Connecting the Mobbin MCP so the Web Builder can pull real design references.

**Not started**
- Hosting and email on uncletsautomation.co.za, resubmitting verification.
- Rex delegating jobs to other agents, the Sheets log (removed from the scenario), moving Rex to the real SIM (063 647 6860).

## The Nate Herk video (read from frames only, no audio)

File was a 41 second reel, "Comment MAP and I'll send it over". From the on-screen text, his method for getting good-looking sites/apps out of Claude:
1. Use **Mobbin**, a library of 600,000+ real shipped app and web screens (onboarding, paywalls, profile pages, dashboards, landing pages).
2. Connect Mobbin to Claude through its **MCP**.
3. Ask Claude to research the best examples of the page type inside Mobbin ("Research the best profile pages inside of Mobbin").
4. Give Claude those real designs as the reference, then build/redesign based on them. A second screen shows Claude Code building from a design-tool import (Stitch) using Vite + React + Tailwind + Framer Motion, with a token file for colours and type.
Takeaway: don't ask Claude to invent a design. Feed it proven references first.

**Gap:** if Theo has the full breakdown Nate promised (he commented MAP), ask him to paste it in the new session.

## Mobbin MCP facts (from mobbin.com/mcp), NOT USED

- Gives Claude access to 600,000+ real product screens, web and mobile.
- **Needs a paid Mobbin plan (Pro or Team).** No API key. One-click install for Claude and other tools.
- Theo has to connect it himself (Claude app: Settings, Connectors, or Claude Code's MCP setup, link at mobbin.com/mcp#install). Cloud sessions cannot sign in for him.

## Decisions made

1. Rex stays on the test number until verification clears, then moves to the real SIM.
2. The personal assistant idea is parked. Focus is the business agent team that brings in clients.
3. Website first, because it unblocks verification and doubles as the Web Builder's first showpiece.
4. Keep the demo number (076 492 4196). It is used in the pitch script and Lexi Voice plan.

## What to do next, in order

1. **Mobbin is dropped** (paid plan, Theo will not pay). The Web Builder now studies real award winners for free using Firecrawl screenshots (see step 2 of the web-builder skill). Tested today on Awwwards Sites of the Day and it works.
2. Ask Theo for Nate's full breakdown if he has it.
3. Run the web-builder skill for **Uncle Ts Automation** (the agency itself): brief, then Mobbin research (agency/SaaS landing pages, WhatsApp automation, local service sites), then build in `outputs/websites/uncletsautomation/`. Must show the business name, what it sells, Chales as proof, WhatsApp contact, contact email and address, privacy policy page. Keep it fast (Lighthouse 90+ on phone). Light background, dark text.
4. Hosting and domain: uncletsautomation.co.za is registered at domains.co.za (R99/year) but has **no hosting pointed at it**. Hosting is about R109/month at the same host as Chante's site. Theo decides and buys. Also create an email on that domain.
5. Meta verification resubmit: business name and address must match across site, documents and the Meta entry. Theo is a sole proprietor (not CIPC registered). Open question for him: register with CIPC (small online fee) to make verification easier. Screens: business.facebook.com/settings, Security Center.
6. Afterwards: move Rex to the real SIM, then build Rex's delegation.

## Gotchas

- **Rotate keys that passed through chat:** the Rexbot token and the Anthropic key (named "Rex" in console.anthropic.com). Revoke and regenerate, then update Make through the API (or edit modules 2 and 3), never by pasting into chat again.
- **Never save Rex's scenario in Make's editor.** It turns `max_tokens` into text and Anthropic rejects it. Change it with `scenarios_update` (fetch current first, it replaces the whole blueprint).
- Rexbot needs BOTH the WhatsApp account and the Messaging account assigned, or sends fail with `(#10) Viewer cannot access the provided Paid Message Account`.
- Meta business "Uncle Ts Automation" is capped at 2 phone numbers until verified, so Rex's SIM cannot be added yet.
- The Rex webhook URL and verify token live only in Make. Never write them in the repo (it is public).
- Theo is moving house and works from his phone and an old laptop. Keep steps short and one at a time.

## Update (later 17 Oct): second job and new facts

- **Theo has already moved house.** The old address warning no longer applies, but ask which address he is comfortable showing publicly. Default: show only "Cape Town" plus WhatsApp on the site, and give the full address only in Meta's form. Not sure whether Meta insists on a street address on the site; test.
- **Second build, same session if time allows: a mock-up demo website for Theo's day-job engineering company** (boilermaker/sheet metal, laser and bending machines). Theo has 2 short clips (laser cutter, bending machine). Build it with the web-builder skill.
  - Rules: mock-up only. Mark every invented line as placeholder in the files. No invented ISO or other certifications, client names, safety records or years in business. Write real descriptions of the services (laser cutting, bending, fabrication).
  - Video: ask Theo to attach the clips in chat. Compress with ffmpeg to 8 to 15 second loops, MP4 H.264, no audio, 720p to 1080p, under 8 MB each, plus a poster image. Lazy-load and keep Lighthouse mobile 90+.
  - Permission: the footage and company name belong to his employer. Get the boss's OK before anything is public or sent around. If the boss likes it, he is a paying prospect (R1,499 once-off + R499/month).
- **Order:** agency site (uncletsautomation.co.za, needed for Meta verification) first, works demo second.
- Mobbin is NOT used (paid, Theo declined). Use the free Firecrawl screenshot method in the web-builder skill.
