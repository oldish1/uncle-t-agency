# Security (10 quiet minutes)

## 1. The GitHub repo is PUBLIC (checked 20 Nov 2026, anonymous access works)
Anyone can read it. It holds plans, pricing, the ledger, Make webhook addresses (Lexi Call, the review page, Lexi 2.0 notes), prospects' phone numbers (`outputs/theo-to-do.md` and the outreach files), Theo's and Chanté's numbers, and client details. No API keys or tokens were found in a scan of the tracked files, which is good. But the open item from 25 Sept (make it private) was never done.
- [ ] Make the repo private: GitHub, repo Settings, scroll to Danger Zone, Change visibility, Make private. Only you can do this. Claude can't. Do it before merging more into main
- [ ] After it's private, regenerate the Make webhook addresses that were committed (they let anyone trigger those scenarios): review page feedback hook, Lexi Call availability and booking hooks, the Lexi 2.0 test webhook. Claude lists them and updates the files
- [ ] Old history stays readable to anyone who already cloned or forked it. Treat the old webhook addresses as burned
- [ ] Prospects' numbers in a public repo is a POPIA risk. Moving them out of the repo (to the Pipeline Sheet only) is part of this

## 2. Keys and tokens

- [ ] Rexbot token: Meta, revoke tokens, generate a new one, tell Claude so Rex is updated
- [ ] Anthropic key named "Rex": revoke and make a new one. Do not touch the key named "Uncle Ts Automation"
- [ ] Apify token: rotate it (it showed in an error message earlier)
- [ ] Anthropic key in plain text inside Make scenario "Lexi 2.0 (test core flow)" (8179409): replace it in the Anthropic console, move keys into Make connections
- [ ] The GitHub repo was public on 25 Sept (full-history scan found no keys, but a webhook address was once committed). Check it's private now
- [ ] Reauthorize any Make Gmail connection that has expired (two were due 29 Sept and 7 Oct)
- [ ] Bank details published on the Chales site: confirm removed
- [ ] Never paste keys into chat. They go into Make connections or the environment's secret box only
- [ ] Client tokens (WhatsApp, Anthropic) never go in the repo or a client folder
