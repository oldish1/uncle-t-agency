# Clients

One folder per client. This is where the data only we have lives: what each client sells, what they said, what we built for them, and what changed after we did. Every new client makes the whole brain better, because the next pitch, the next build and the next case study start from real numbers.

## Rules

1. **No secrets, ever.** No tokens, keys, passwords or webhook addresses. Those live in Make connections and `private/`. A client file may say "the WhatsApp token is in Make connection X" and nothing more.
2. **Real client details only after the GitHub repo is private.** It is public today (`todo/security.md`). Until that changes, keep a client's personal details (their customers' numbers, private messages, money figures they told us in confidence) out of these files.
3. **Every client stands alone.** Own folder, own number, own scenario, own sheet, own calendar, own key. Nothing is copied between clients except the template.
4. **Numbers beat opinions.** Fill `results.md` with real before and after figures. It is the case study and the sales proof.

## Folder shape

```
clients/<slug>/
  profile.md        who they are, services, prices, hours, owner, tone of voice
  deal.md           what they bought, price, start date, the one metric we agreed
  assets.md         where their stuff lives (links and IDs, never secrets)
  conversations.md  what the owner said in our own words, pains, objections
  results.md        before and after numbers, dated, plus testimonials
  log.md            running notes for this client (optional, the ledger has the headline)
```

## Add a client

Say "new client: <name>" or run `/new-client <name>`. Claude copies `clients/_template/`, fills what it knows, and adds the client to the brain map, the Chief of Staff watch list reminder and the to-do list.

## Clients so far

| Client | Folder | Status |
|---|---|---|
| CHALES Hair Boutique | `clients/chales-hair-boutique/` | Live, proof client |
| Rags to Riches Cleaning (Nita) | `context/rags-to-riches.md` | Family deal, bot on test number. Move into a folder when it goes live |
