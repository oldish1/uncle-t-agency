# Tech stack

Theo lives in two of these day to day: **WhatsApp** (client-facing, where Lexi runs) and **Google Calendar** (booking backend). Everything else supports those two.

## Platforms

| Platform | What it does for us | Wired in? |
|---|---|---|
| Make.com | Automation backbone, runs Lexi's booking logic and the outreach email sequence | not covered (no connector; Theo works in it directly) |
| Google Sheets | Prospect tracker, CRM stand-in, booking data | connected, reachable through the Drive connector |
| Google Calendar | Booking backend for Lexi (chosen over Calendly to protect margin) | connected |
| Google Drive | Client runbook and documentation storage | connected |
| WhatsApp Business / Cloud API | Client-facing channel for Lexi | not covered (no connector) |
| Meta Business Manager | WhatsApp Business profile config | not covered (no connector) |
| Netlify | Hosting for demo pages and single-HTML sites | needs Theo to authorize it under claude.ai Settings, Connectors, this workspace can't trigger that sign-in itself |
| domains.co.za | Client hosting and domains (CHALES: R109/month) | not covered (no connector) |
| Claude API | Conversational AI layer inside Lexi, called via Make.com HTTP modules | n/a, called directly by Make.com |
| GSAP / ScrollTrigger | Scroll animation on client sites | n/a, code library, not a connected service |

## Integration queue

1. Netlify, once Theo authorizes it (claude.ai Settings, Connectors), so this workspace can help manage deploys directly rather than him doing it by hand.
2. Everything else (Make.com, WhatsApp Business, Meta Business Manager, domains.co.za) has no off-the-shelf connector. `/new-capability` can build a custom one if it's ever worth the time; for now Theo works in those directly and this workspace helps with the content and logic that feeds them.
