# Jason Cooperson's Bland AI receptionist: what it really is

Date: 18 Nov 2026. Source: his Loom walkthrough (loom.com/share/d4b5b4065dc1403ab1e8bfb22a8dd027, 11 min) and his public repo github.com/jasonc00person/bland-ai-receptionist (MIT licence, so we may reuse and sell work built on it). Theo sent the Loom after the Instagram reels reviewed on 11 Nov.

## What it does
A phone receptionist for a made-up car shop ("Apex Auto Works", agent "Clint") on Bland (bland.ai). Picks up, offers times, takes name and car, takes the work list, texts the caller mid-call, says goodbye and hangs up. Admits it is an AI when asked and offers a human. A Python installer builds it in the user's Bland account; a text-only simulator runs three scripted test callers (happy, rude, out of order).

## What it does not do (the gap between the reel and a real client)
- **No calendar.** The open times are written into the prompt ("next Tuesday only, 9, 11:30 or 2"). The "calendar link is on its way" line is only spoken. His README says so.
- **No booking is saved anywhere** except the call record and the text.
- **US setup.** It assumes a Bland number on the Agent Phone Plan (unlimited US and Canada minutes and texts). SMS is sent through Bland. Not checked yet: Bland's South African numbers, SA texting, or pricing outside the US.
- Bland retired its old "pathways" editor on 15 Nov 2026; the template already builds on the new agent system.

## What we would change for Chales
1. Replace the fixed times with a live lookup: a webhook step that calls a small Make scenario, which checks Chanté's Google Calendar the way Lexi does and returns open slots.
2. A second webhook step writes the booking (calendar event and sheet row), reusing Lexi's booking pattern.
3. Confirmation goes by WhatsApp (Lexi's photo confirmation), not SMS.
4. Swap the car shop for Chales: services list from `context/lexi.md` (no braids), salon rules, a South African voice, English and Afrikaans.
5. Test on a demo calendar and the browser or text simulator first, never Chanté's calendar.

## Worth copying as is
His prompt lessons, each from a failed live call: write prompts the way people talk, keep the flow in one straight line, never let the caller talk while the text step is active (it re-sent 10 texts), make the "are you an AI?" trigger strict, test every change three times. Also the scripted test callers.
