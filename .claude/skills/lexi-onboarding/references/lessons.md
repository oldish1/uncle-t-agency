# Lessons from building and running CHALES

Each one cost time. Dates are 2026.

## Make and the scenario

- **Router fallbacks are stored by position** (25 Sept). Inserting a route before existing ones silently changed which route was the "else", and names stopped confirming. Append new routes at the end and check every router's fallback still points at the same route.
- **Code modules return output under `.result.`** (27 Sept). Eight references to the membership calculations were missing it and BALANCE failed. Check the output path of any new code step.
- **Make has no `or()` function** (25 Sept). Use nested `if` or `contains`. Test every new formula in a throwaway scenario first, then delete the scenario.
- **`notexist` on an empty variable isn't safe** (27 Sept). Remove the variable instead of emptying it. An emptied variables array also blocked saving in Make's editor even though the API accepted it, so remove an unused module rather than leaving it empty.
- **No duplicate protection means double deductions** (27 Sept). The ProcessedMessages sheet keyed on WhatsApp's message ID fixes duplicate deliveries. Keep it for every client.
- **Slow came from too many modules** (23 Sept). Taps were 11 to 20 s. Moving the AI into a typed-message-only branch, sending the reply before sheet bookkeeping, merging lookups and replacing code steps with formulas got taps to 3 to 9 s. Don't add steps before the reply is sent.
- **Calendar lookups**: use the plain calendar address, an encoded one gave a 404. Delete events by real event ID through the Google API.
- **Blueprint size**: the full scenario is about 230K characters. Don't push it through one tool call. Import files for Theo, or small edits.
- **Frozen at fix14** (25 Sept): voice notes, service shortcut, photo confirmation. No more features until a clean-up pass after the first paying client.

## WhatsApp and Meta

- **Test messages hit a live client** (19 Sept). A test subscribed Chanté's app to the demo account's events, and then a leftover per-number webhook override still pointed at her callback URL. The per-number override outranks the app-level setting. Check both before testing, and keep demo and client accounts fully separate.
- **No template needed for the booking confirmation** because it's sent inside the 24-hour chat window. Reminders and review requests are business-started, so they need an approved template and carry a small per-message fee from Meta.
- **Staff alerts pointed at Lexi's own number** (found 27 Sept). Always set them to the owner's real WhatsApp and send a test alert.
- **Reminders sat in test mode for four days** (23 to 27 Sept) with a gate that only sent to Theo's number. Check the gate at go-live.
- **Emoji**: 📅 showed "FEB 24" on Samsung phones. Use 🗓️.
- **Voice-to-text heard "Theo" as "Siyou"**. Names must be typed.

## Marketing and handover

- **The TikTok bio listed the owner's personal number instead of Lexi's** from launch, so the best videos sent leads to a chat nobody automated. Put Lexi's wa.me link in every bio and caption template on day one.
- **Maps pin vs real listing**: "Get Directions" pointed at a bare street address. Use the business listing link once it exists.
- **Hours drifted** across website, Google, Lexi and TikTok. One confirmed set, changed everywhere on the same day.
- **Don't claim "5 star rated"** on a site with no reviews.

## Security

- The agency repo was public for a while (25 Sept). Full-history scan found no keys, but Lexi's webhook address had been committed. Keep the repo private, keep secrets in Make and `private/`, and only public images in `oldish1/chales-assets`.
- Bank details on a client's public website: flag to the owner.
