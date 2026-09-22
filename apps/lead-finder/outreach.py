"""First WhatsApp message for each lead, led by the pain their own customers named.

Rules: short, sounds like Theo, never says "AI" or "chatbot", never quotes a
customer by name, one clear yes/no ask. One message, then at most one follow-up
a week later, then stop. Edit freely before sending.
"""

from __future__ import annotations

from scoring import Salon, Score

INTRO = "Hi, it's Theo from Uncle T Agency, I'm local here in Cape Town."
PROOF = "My daughter's salon, CHALES Hair Boutique, runs on it."
# One approach only, asking permission (POPIA). A yes means they get the demo video.
ASK = "Can I send you a 90-second video of it working in my daughter's salon? Just reply yes or no."
FOLLOW_UP = ("Hi, Theo from Uncle T Agency again. Just checking you saw my message last week. "
             "Happy to send the 90-second video if you're keen, and if not, no stress, I won't message again.")

HOOKS = {
    "missed_messages": (
        "I was reading {name}'s Google reviews and a few clients mention struggling to get a reply when they want to book. "
        "That usually just means you're busy with a client in the chair. "
        "I set up a WhatsApp receptionist that answers straight away, day or night, and books them into your diary."
    ),
    "double_booking": (
        "I was reading {name}'s Google reviews and saw a booking mix-up or two mentioned. "
        "I set up a WhatsApp receptionist that checks your diary before it confirms anyone, so a slot can never be given out twice."
    ),
    "cancelled_on_me": (
        "I was reading {name}'s Google reviews and saw some appointment changes caused frustration. "
        "I set up a WhatsApp receptionist that handles bookings and reminders, so clients always know where they stand."
    ),
    "waiting": (
        "I was reading {name}'s Google reviews. Clients love the work, and a few mention waiting around. "
        "I set up a WhatsApp receptionist that books proper time slots and sends reminders, so the day runs to time."
    ),
    "hard_to_book": (
        "I was reading {name}'s Google reviews and it's clear you're in demand, a few people struggled to get a slot. "
        "I set up a WhatsApp receptionist that shows clients your open times and books them in, even after hours."
    ),
    "late": (
        "I was reading {name}'s Google reviews. Clients love the work. "
        "I set up a WhatsApp receptionist that books proper time slots and sends reminders, so the day runs to time."
    ),
}
NO_WEBSITE = (
    "I noticed {name} doesn't have its own website yet, so people who Google you only find the Maps listing. "
    "For my first ten salons I'm building the website and a WhatsApp receptionist that books clients in for you, "
    "no setup fee, and you pay nothing until she's booked your first 10 clients."
)
GENERAL = (
    "I help salons like {name} stop losing bookings on WhatsApp. "
    "It's a receptionist that replies instantly, day or night, and books clients straight into your diary."
)


def first_message(s: Salon, sc: Score) -> str:
    name = s.name.strip()
    pain = next((p for p in sc.pain_types if p in HOOKS), None)
    if sc.pitch in ("Lexi", "Lexi + website") and pain:
        body = HOOKS[pain].format(name=name) + " " + PROOF
    elif sc.pitch == "Website":
        body = NO_WEBSITE.format(name=name)
    else:
        body = GENERAL.format(name=name) + " " + PROOF
    return f"{INTRO} {body} {ASK}"


def whatsapp_link(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if digits.startswith("0"):
        digits = "27" + digits[1:]
    return f"https://wa.me/{digits}" if len(digits) >= 11 else ""
