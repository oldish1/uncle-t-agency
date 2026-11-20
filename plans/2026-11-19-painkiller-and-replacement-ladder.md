# Painkiller first, then the replacement ladder (from Dan Martell's "How to Build a 1-Person Business with AI Agents")

Written 19 Nov 2026 from the video Theo shared (transcript pulled with Supadata). The video is also where the "I've owned a salon for 10 years, find me 30 nuanced and observable challenges" prompt came from. Martell sells his own tools (Apex, an AI operating system), and his revenue claims are self-reported, so we take the framework, not the sales claims.

## The method in four moves

1. **Find the painkiller, not the vitamin.** Ask the AI for 50 nuanced, observable problems your customer has. Check which ones they already pay to fix. Pick the top three.
2. **Ask for advice, not the sale.** Message 10 people in that market: "Have you ever experienced these three pains? Do you have time to give me advice on my new company?" His line: "If you ask for the sale, you get advice. If you ask for advice, you get the sale."
3. **Present the offer only after the advice.** Ask if they want to be the first customer.
4. **Then buy your time back with the replacement ladder:** inbox agent, delivery agent, marketing agent, sales agent, then one shared brain. Each agent gets four things: data equity (what only you have), a blueprint (the steps), a schedule, and a sensor (a way to see it working).

## Where we are

| Move | Status |
|---|---|
| 30 observable challenges, which ones owners pay for | Done: `reference/research/2026-11-19-salon-challenges-30.md` |
| Top three painkillers | Chosen below, Theo to confirm |
| Advice messages to 10 owners | Message drafted below, 10 names to choose |
| Discovery chats in person | Script done: `outputs/sales/universal-discovery-script.md` |
| Inbox agent | Partly. Rex runs on Telegram. Replies to salons are handled in the outreach desk session |
| Delivery agent | Not built. Needed at client number one |
| Marketing agent | Partly. Scout finds leads on request. The daily brief task has no Sheets access yet |
| Sales agent | Not built. Mock-call coaching can start in chat today |
| One brain | This workspace plus the Pipeline Sheet. Conversations and Replies tabs are the shared notes |

## The top three painkillers (my pick, from the evidence)

1. **WhatsApp enquiries go unanswered while the owner is mid-service** (challenges 1, 3, 8).
2. **No-shows and cancelled slots that stay empty** (4, 5).
3. **The owner never switches off and burns out** (7, 30).

## The advice message (WhatsApp, Theo sends)

For salons we have not contacted before, or owners Theo meets in person. Never use it on a salon that was sent the "I'll close your file on Friday" message, or that said no.

> Hi [name], Theo here from Cape Town. I'm building something for salon owners and I want advice before I build more. Three things keep coming up: WhatsApp messages going unanswered while you're with a client, no-shows and empty slots after a cancellation, and never getting a proper day off. Have you run into any of these? If so, could I ask you three quick questions, by voice note or a five minute call? If it's not for you, no problem at all.

## The ladder, applied to Uncle T Agency

- **Inbox agent:** Rex plus a reply helper that drafts answers to salon replies in Theo's voice and writes the row in the Replies tab. Review mode only: Theo reads and sends, as now.
- **Delivery agent (build at client one):** after a yes, an intake form (services, prices, hours, calendar, greeting), a four-day setup checklist, and a first-win message. Start from `plans/client-template.md`. Use Martell's prompt to interview Theo about the Chales setup and turn it into a checklist.
- **Marketing agent:** Scout finds 10 new salons each weekday, the booking check filters them, the outreach writer drafts the messages. Needs the scheduled task rebuilt with Sheets attached. Content: the nine pains on the website turn into short videos.
- **Sales agent:** Claude plays a salon owner and Theo practises the discovery script, then Claude scores the talk versus listen ratio and the steps skipped. Later it qualifies enquiries before Theo spends time on them. The close stays human.
- **One brain:** the ledger, `context/`, the Sheet. Friday handoff: the objections and pains from the week's chats go into the website copy and the follow-up messages.

## Careful

- A voice agent that cold-calls leads (as in the video) needs thought in South Africa: POPIA direct-marketing rules apply, and our own rule is that Theo sends every first message himself.
- Searching Facebook groups for people complaining is fine for research, but reaching out to individuals needs the group's rules and a human touch. Ask for advice, don't pitch.
- Build the delivery agent only when a paying client is close. Martell's own order is inbox, then delivery, then marketing, then sales, so marketing doesn't bring in customers we can't serve.
