# Rex on Telegram (stopgap until his WhatsApp number is verified)

Decided 6 Nov 2026. Telegram needs no Meta verification, so Theo can talk to Rex today. Later the same brain moves to WhatsApp (`GO-LIVE.md`).

## Why this needs no secret keys from Theo

Make has built-in modules that need no Anthropic key:
- **Anthropic Claude, Simple Text Prompt**: Claude Sonnet 5, billed in Make credits (about 6 credits for a normal chat message). Used for chat, planning and drafting.
- **Make AI Web Search, Generate a response**: searches the web (paid plans, no connection). Used for fixtures, scores, news, prices, "look this up". Basic: it reads page source and uses a small model, so deep research stays with the Claude sessions.
- **Telegram Bot**: the only connection. Theo creates it himself in Make with the bot token from BotFather. The token never goes in chat or in this repo.

## Build plan

Stage 1, chat and web search (scenario "Rex - Telegram"):
Watch Updates, a filter so ONLY Theo's chat id gets answered (anyone can find a bot by its name), then a router: web-search route for questions that need current facts, default route Claude with the Rex system prompt from `system-prompt.md`, then Send Reply Message.
To learn Theo's chat id: build with the filter set to a placeholder, he sends hi, read the id from the first execution, then lock the filter.

Stage 2, reminders without paying to poll:
Polling a sheet every few minutes would burn most of the monthly Make credits. Instead Rex creates **Google Calendar events with a phone notification** on Theo's own calendar: "remind me tomorrow 17:00 to call Chante" becomes an event with an alert at that time. Free, reliable, and Google does the scheduling.

Stage 3, Arsenal:
A weekly scenario (Monday 07:00 SAST) asks web search for Arsenal's first-team matches in the next 7 days with kick-off in SAST, then creates a calendar event for each with an alert 30 minutes before. A daily morning message "Arsenal play today at 17:30" is the backup. Fixture data comes from web search, so Theo should glance at it; it is not a verified fixture feed.

## What Rex can and cannot do on Telegram

Can: chat as Rex with the current brain, answer from the web, plan and draft, set reminders, track Arsenal.
Cannot yet: see the Pipeline Sheet, remember earlier chats, start the other agents, or message anyone but Theo. Those are Rex v2.1 (see `GO-LIVE.md`).

## Safety

The bot answers only Theo's chat id. Rex never messages a prospect and never sends, pays or publishes without Theo's yes.


## Status, 7 Nov 2026: LIVE

Scenario "Rex - Telegram" (Make id 8428548), Telegram listener hook 4057483, connection "Rex Telegram" (12797086). Bot @UncleTRex2bot. Locked to Theo's Telegram id only (filter on message.from.id), so nobody else gets an answer.

Built so far: chat with the Rex brain (Claude Sonnet 5 via Make's Simple Text Prompt) and web search (Make AI Web Search) for messages that contain words like search, price of, how much is, news, weather, score, fixture, arsenal.

Field names learned the hard way (the Make API here cannot validate modules, so we found them by testing):
- anthropic-claude:simpleTextPrompt takes model, max_tokens, textPrompt. Answer is {{N.result}}.
- make-ai-web-search:generateAResponse takes input. Answer is {{N.result}}.
- telegram:SendReplyMessage takes chatId and text, with the connection in parameters.__IMTCONN__.
- telegram:WatchUpdates takes the hook as parameters.__IMTHOOK__.

Not built yet: reminders as Google Calendar events, the weekly Arsenal fixtures, memory, Sheet reading, the Tasks list for delegation.

## Update 7 Nov 2026: reminders and Arsenal

- Reminders: message starts with "remind" (e.g. "remind me tomorrow at 5pm to call Chante"). Route 3 of scenario 8428548: Claude turns it into "YYYY-MM-DD HH:mm|title", Google Calendar event created on adamst70@gmail.com (15 min, connection 5535950), Telegram confirms. The phone alerts through Google Calendar, so no polling and no extra Make credits for scheduling.
- Web and chat routes exclude messages starting with "remind".
- Arsenal: scenario 8428725, Mondays 07:00 SAST. Web search lists fixtures, Telegram gets the list, each match becomes a calendar event. Fixture times come from a web search, so glance at them.
- Rex replies in plain text (no markdown asterisks).

## Correction 7 Nov 2026: Arsenal

Web search guessed fixtures wrongly, so scenario 8428725 is switched OFF. Use the Sky Sports calendar feed instead (exact times, refreshes hourly): https://www.skysports.com/calendars/football/fixtures/teams/arsenal. Theo adds it once in Google Calendar on a computer (Other calendars, plus, From URL). Reminders route tested working.
