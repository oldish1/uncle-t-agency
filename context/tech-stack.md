# Tech stack

## Platforms

| Platform | What it does for us | Wired in? |
|---|---|---|
| Make.com | Automation backbone, runs Lexi's booking logic and the outreach email sequence | not covered (no connector; Theo works in it directly) |
| Google Sheets | Prospect tracker, CRM stand-in, booking data | pending, Google connector not yet turned on |
| Google Calendar | Booking backend for Lexi (chosen over Calendly to protect margin) | pending, Google connector not yet turned on |
| Google Drive | Client runbook and documentation storage | pending, Google connector not yet turned on |
| WhatsApp Business / Cloud API | Client-facing channel for Lexi | not covered (no connector) |
| Meta Business Manager | WhatsApp Business profile config | not covered (no connector) |
| Netlify | Hosting for demo pages and single-HTML sites | pending, needs authorization before this workspace can use it |
| domains.co.za | Client hosting and domains (CHALES: R109/month) | not covered (no connector) |
| Claude API | Conversational AI layer inside Lexi, called via Make.com HTTP modules | n/a, called directly by Make.com |
| GSAP / ScrollTrigger | Scroll animation on client sites | n/a, code library, not a connected service |

## Integration queue

1. Google (Sheets, Calendar, Drive) through the Claude connectors, since the prospect list, booking calendar, and runbook all already live there.
2. Netlify, once authorized, so this workspace can help manage deploys directly rather than Theo doing it by hand.
3. Everything else (Make.com, WhatsApp Business, Meta Business Manager, domains.co.za) has no off-the-shelf connector. `/new-capability` can build a custom one if it's ever worth the time; for now Theo works in those directly and this workspace helps with the content and logic that feeds them.
