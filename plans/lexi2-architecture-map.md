# Lexi (Chales Hair Boutique) — Current Architecture Map

Source: Make.com scenario 5043763 ("Chales Hair Boutique "), pulled 2026-10-26.
Purpose: faithful reference for building "Lexi 2.0" without losing any existing business logic.

## Headline facts

- **~340 modules** in one flat scenario (one giant nested router tree, no sub-scenarios).
- **1 AI brain call** total (not 5, despite 5 separate "No intent, no pending reply" filter gates reaching it from different branches — see Surprises).
- **4 Google Sheets tabs**, all in spreadsheet `130twXjBTQGWxt87x5Vji9dLTyEwUChBT618ON0NYAH8`: `BookingSession`, `Sheet1` (main client/booking log, numeric sheetId `148622901`), `Memberships `, `ProcessedMessages`.
- **One stray reference to a second spreadsheet** (`1gjUewL4lt72MH2U0VHKbCIEXeT1cmh43wHt91IuUjZY`) near line 4629/4631 of the raw blueprint — not yet understood, flag for follow-up, don't assume it's dead.
- **1 Google Calendar** used as source of truth for availability: `herbertchante3@gmail.com`, timezone `Africa/Johannesburg` hardcoded everywhere dates are parsed.
- **WhatsApp Business number**: phone-number-id `1197696726762690`, endpoint `https://graph.facebook.com/v25.0/1197696726762690/messages` — used in ~34 separate HTTP modules (one per place a message goes out; no shared "send message" sub-flow).
- **1 inbound webhook callback** to Make itself (`https://hook.eu1.make.com/oyazyu3x8gspj4o5bb1cjtji4fo1vc2t`) used twice — looks like a self-trigger/loopback, not yet understood, flag for follow-up.

## Top-level flow

```
[1] gateway:CustomWebHook  — WhatsApp inbound webhook trigger
  |
[301] BasicRouter
  ├─ Branch "Voice note" (id 302) — message has audio
  │    → ack → download voice note (modules 310/312) → openai-gpt-3:CreateTranscription (305)
  │    → ExecuteCode (306) extracts transcript/phone/msgId fields
  │    → BasicRouter (307): "Got words" → hand transcript to Lexi as text
  │                          "No words" → ask user to type instead
  │
  └─ [2] filter "Has message text" → gateway:WebhookRespond (ack 200 to Meta immediately)
       |
     [160] google-sheets:filterRows on BookingSession (look up this phone's in-progress session)
       |
     [157] BasicRouter
       ├─ "Pending Exists" (159) — session row found, mid-flow
       │    → TextAggregator (265) + ExecuteCode (266) rebuild conversation state
       │    → [162] BasicRouter — classify what the reply means:
       │         ├─ "Cancel" (164)
       │         │    → BasicRouter: "Ask Stage" (240, confirm they want to cancel)
       │         │                    "Confirm Stage" (168, 165/166/167/169/338 —
       │         │                       google-calendar:makeApiCall x2 + Sheets addRow/deleteRow,
       │         │                       actually deletes the calendar event + session row)
       │         ├─ "Refund a wash" (appears twice, 1305/1356 — membership wash credit logic,
       │         │    touches Memberships + ProcessedMessages tabs)
       │         ├─ "Reschedule" (1425) → re-run availability check, same addRow/deleteRow pattern
       │         ├─ "Other" (1661) → fallback reply
       │         ├─ "No booking on file" (1735) → tell them nothing to cancel/reschedule
       │         └─ "Session row exists" (1845) → normal continuation
       │
       └─ "No Pending Reply" (1909) — fresh conversation
            |
          [1976] "Intent Detected" — free-text booking intent without a prior menu tap
            ├─ "Balance or Renew" (2058) / "Renew alert" (2258, 2311, dup) — membership balance questions
            ├─ "Tap reply" (2401) — they tapped a WhatsApp interactive element
            │     → "Time Selected" (2420) → "Slot Available" (2504) → books it
            │     → "Day Selected " (2759) → shows times for that day
            │     → "Service Selected" (2961)
            │          → "First treatment pick" (3009) → "Second treatment picked" (3129)
            │          → "Second treatment: no" (3257) / "Second treatment: yes" (3331)
            ├─ "Greeting Interceptor" (3396) — plain "Hi"/"Hey" style opener
            │     → "Service named" (3486) already said what they want
            │     → "No single service" (3575) → **module 57: real WhatsApp interactive LIST
            │          send** (the correctly-built tap menu — only reached from THIS branch)
            └─ "Booking Name Capture" (3640) — collecting the client's name
                 → "Slot Available" (3801) → confirms + writes Sheet1/BookingSession
                 → "Member deducted" (4106, 4148 dup) / "Final wash" (4192) — membership logic
                 → "Slot Taken" (4537) — race-condition catch, re-offers slots

          5 parallel gates all named **"No intent, no pending reply"** (4690, 4732, 4801, 4842,
          4881) — each one is a different upstream branch's fallback that converges on the
          SAME single AI call:
            |
          [149] http:MakeRequest → https://api.anthropic.com/v1/messages (model claude-sonnet-4-6)
            — the monolithic staged system prompt (STAGE 1 → 5). This is the one AI brain call
            in the whole scenario; everything upstream is deterministic routing trying to avoid
            calling it unless genuinely needed (cost/latency control).
            |
          AI reply is free text. Downstream:
            ├─ "Booking Confirmed" (4922)
            ├─ "Booking Ready" (5070) — AI emitted `[BOOKING_READY]|...` tag
            ├─ "Check Availability" (5118) / "CHECK_AVAILABILITY detected" (5159) — AI emitted
            │    `[CHECK_AVAILABILITY|...]` tag → parsed by ExecuteCode → google-calendar
            │    freebusy call (timeMin=today, timeMax=+8 days, Africa/Johannesburg) →
            │    "No existing session" (5228) → "Slot Available" (5322, empty conditions —
            │    i.e. an else-branch) → "Exclude Taken Slot" (5351) → "Slot Taken" (5421)
            │    → generates the slot list → sent as plain text, NOT module 57's interactive
            │    list (this is the Stage 1/1B bug: the AI types menus/slot lists as prose
            │    instead of handing off to a tap UI, confirmed root cause from prior session)
            └─ "Normal Conversation" (5509) — just chat, send AI's text as-is
```

## Sheets usage summary

| Tab | Written by | Read by | Purpose |
|---|---|---|---|
| `BookingSession` | addRow/deleteRow at confirm/cancel/reschedule (modules 167/169/241/242 etc.) | `filterRows` (160) at top of every inbound message | Tracks in-flight conversation state per phone number — this is also the race-condition surface (no per-row lock, hence sequential processing being forced on the whole scenario) |
| `Sheet1` (gid 148622901) | addRow on confirmed booking | — | Main client/booking log, what Theo actually looks at |
| `Memberships ` (trailing space in the real tab name) | deduct/credit on wash usage | balance/renew checks | Membership wash-credit tracking |
| `ProcessedMessages` | addRow per processed inbound message | checked to avoid double-processing | Idempotency guard against WhatsApp webhook retries |

## Calendar usage

- Single calendar `herbertchante3@gmail.com`, always `Africa/Johannesburg`.
- Availability checked via `google-calendar:makeApiCall` freebusy-style query, window = today → +8 days.
- Slot duration logic: services containing `" + "` (i.e. two services combined) get 120/119 minutes, single services get 60/59 — this "+1 minute off the round number" pattern recurs (59 vs 60, 119 vs 120) and looks like a deliberate buffer-avoidance hack worth carrying over or replacing with an explicit buffer field.
- Booking write = calendar event creation (module 165/166 area) + Sheet1/BookingSession rows, in that order — if the calendar write succeeds but the Sheets write fails (the Oct 25 storage incident), you get a real calendar booking with no corresponding sheet record. Lexi 2.0 should write the source-of-truth record first (or make both idempotent/retryable) rather than calendar-then-sheet.

## WhatsApp send pattern

- 34 separate outbound HTTP modules, each hardcoding the same bearer token and URL — no shared "send WhatsApp message" subroutine. Only **one** of them (module 57, under "No single service") sends a real `interactive: {type: "list"}` payload. Every other outbound module sends plain `type: "text"` bodies, including the two places that most need to be tappable: the Stage 1/1B service menu and the slot list after `CHECK_AVAILABILITY`.

## Other utility/safety modules

- `code:ExecuteCode` appears 5 times — reassembling session state from the aggregated session rows (266), extracting voice-note transcript fields (306), and parsing the AI's `[CHECK_AVAILABILITY|...]` / `[BOOKING_READY]` tags out of free text. This tag-parsing step is exactly the "stray quote breaks JSON" risk point referenced in prior incident history — it's regex/string-splitting on AI prose, not structured output.
- `util:TextAggregator` (265) — stitches multiple BookingSession rows/fields into one text blob fed back into the AI's context.
- Idempotency: `ProcessedMessages` tab + webhook-respond-first pattern (ack Meta before doing any real work) — solid pattern, worth keeping as-is in Lexi 2.0.

## Surprises vs. what we already knew (modules 57 & 149)

1. Only **one** AI call in the entire scenario — the "No intent, no pending reply" filter is duplicated 5 times across different branches, all funneling into the same module 149. That's not 5 bugs, it's 5 copies of the same gate — worth collapsing into one shared path in Lexi 2.0 rather than copy-pasted branches.
2. Module 57's interactive list is reachable from exactly **one** entry point ("Greeting Interceptor" → "No single service"). Every other path that needs to show a menu or slot list (Stage 1B text-intent, the CHECK_AVAILABILITY slot list, the post-cancel re-offer) falls through to the AI typing it as text. So the "inconsistency" isn't a one-off mistake — the proper interactive-send mechanism was only ever wired to one of at least four places that need it.
3. **Resolved** — the second spreadsheet (`1gjUewL4lt72MH2U0VHKbCIEXeT1cmh43wHt91IuUjZY`) is just a raw conversation transcript log (every user/assistant turn, phone + message + role) in its own `Sheet1` tab — useful for debugging/QA, not core booking logic. The self-looping webhook (`hook.eu1.make.com/oyazyu3x8gspj4o5bb1cjtji4fo1vc2t`) fires only when a voice note transcribes successfully (`306.result.ok == "yes"`) — it re-feeds the transcript back into the scenario's own webhook so it's treated exactly like a normal typed message, reusing the one main flow instead of duplicating it for voice. Both are intentional, low-risk, worth carrying over as-is in Lexi 2.0.
4. The booking write order (calendar first, then Sheets) is itself a latent bug class beyond the one Oct 25 storage incident — any future Sheets-write failure leaves a real calendar booking with no record of it, independent of root cause.
5. Voice-note handling (transcription via OpenAI Whisper, not Anthropic) is a feature not mentioned anywhere in the task/incident history so far — full voice-note-to-text flow exists and must be carried over, not dropped, in Lexi 2.0.
