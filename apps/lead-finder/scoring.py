"""How a salon earns its score.

Three questions, each worth points:
  need     (0-50)  Do their own customers complain about the thing Lexi fixes?
  website  (0-15)  Do they have no real website, so a site is an easy second sale?
  can_pay  (0-35)  Are they busy and established enough to pay R1,000 a month?

Total is out of 100. Hot = 60+, Warm = 40-59, Cold = under 40.
Every point comes with a plain-English reason so Theo can see why.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

# ── Review language that means "booking or messaging is broken here" ──
# Strong: almost always about missed messages or booking mix-ups.
STRONG_PAIN = {
    "missed_messages": [
        r"no repl(y|ies)", r"never repl(y|ied)", r"didn'?t repl(y|ied)", r"did not repl(y|ied)",
        r"not repl(y|ying)", r"ignored? my (message|msg|text|whatsapp)", r"left (me )?on read",
        r"couldn'?t get (hold|through)", r"could not get (hold|through)", r"can'?t get hold",
        r"(never|didn'?t|doesn'?t|don'?t) answer", r"no answer", r"unreachable",
        r"took (days|forever|ages) to (reply|respond|answer)", r"slow to (reply|respond)",
        r"phone (is )?(always )?off", r"never pick(s|ed)? up",
        # Afrikaans / Kaaps
        r"antwoord (nie|nooit)", r"nie geantwoord", r"nooit terug", r"nie terug gekontak",
    ],
    "double_booking": [
        r"double[- ]?book", r"over[- ]?book", r"booked (someone|somebody) else",
        r"gave my (slot|appointment|booking) (away|to)", r"no record of my (booking|appointment)",
        r"forgot (about )?my (booking|appointment)", r"(booking|appointment) (was|got) (lost|mixed)",
        r"mix[- ]?up with (my|the) (booking|appointment)", r"dubbel bespreek",
    ],
    "cancelled_on_me": [
        r"cancell?ed (on me|last minute|my appointment)", r"last[- ]minute cancel",
        r"stood (me )?up", r"no[- ]show(ed)? (by|from) (the|her|him)", r"rescheduled (me )?(twice|again|last minute)",
    ],
}
# Medium: often about booking pain, sometimes about something else.
MEDIUM_PAIN = {
    "waiting": [r"had to wait", r"kept (me )?waiting", r"waited (for )?(over|more than)? ?(an|\d+) (hour|hr)", r"gewag"],
    "hard_to_book": [r"hard to (book|get an appointment)", r"difficult to (book|get)", r"fully booked", r"no (available )?slots"],
    "late": [r"(arrived|came|started) late", r"was late", r"running late"],
}
# Owner replies that admit the problem.
OWNER_APOLOGY = [
    r"sorry (we|i) (missed|didn'?t see|didn'?t get)", r"apologi(es|[sz]e) for the (delay|late reply|miscommunication|mix[- ]?up)",
    r"sorry for the (delay|late reply|confusion|mix[- ]?up)", r"(message|whatsapp) (got|was) missed",
]

# Online booking tools. If they already use one, Lexi is a harder sell.
BOOKING_PLATFORMS = {
    "fresha": "Fresha", "booksy": "Booksy", "setmore": "Setmore", "gettimely": "Timely",
    "vagaro": "Vagaro", "salonist": "Salonist", "simplybook": "SimplyBook", "calendly": "Calendly",
    "squareup.com/appointments": "Square", "book.squareup": "Square", "salonized": "Salonized",
    "phorest": "Phorest", "treatwell": "Treatwell", "shedul": "Fresha", "zolmi": "Zolmi",
    "appointy": "Appointy", "acuityscheduling": "Acuity", "planity": "Planity",
}
SOCIAL_ONLY_HOSTS = ["facebook.com", "fb.com", "instagram.com", "linktr.ee", "tiktok.com", "wa.me", "api.whatsapp.com", "beacons.ai", "bio.link"]

# Chains and franchises: they have head-office systems and head-office buyers.
CHAINS = ["sorbet", "carlton hair", "candi & co", "candi and co", "placecol", "lamelle", "mugg & bean",
          "headlines hair", "hair & beyond", "sally beauty", "clicks", "dis-chem", "the nail bar @", "sportsmans warehouse"]

SA_MOBILE = re.compile(r"^(\+?27|0)\s?[678]\d")


@dataclass
class Review:
    text: str
    rating: float | None = None
    when: str | None = None          # ISO date
    owner_reply: str | None = None


@dataclass
class Salon:
    place_id: str
    name: str
    address: str = ""
    area: str = ""
    phone: str = ""
    website: str = ""
    rating: float | None = None
    review_count: int = 0
    status: str = "OPERATIONAL"
    maps_url: str = ""
    category: str = ""
    reviews: list[Review] = field(default_factory=list)
    site: dict = field(default_factory=dict)   # filled by site_check


@dataclass
class Score:
    need: int = 0
    website: int = 0
    can_pay: int = 0
    reasons: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)   # short review quotes
    pain_types: list[str] = field(default_factory=list)
    booking_tool: str = ""
    excluded: str = ""

    @property
    def total(self) -> int:
        return self.need + self.website + self.can_pay

    @property
    def tier(self) -> str:
        if self.excluded:
            return "Skip"
        if self.total >= 60:
            return "Hot"
        if self.total >= 40:
            return "Warm"
        return "Cold"

    @property
    def pitch(self) -> str:
        lexi = self.need >= 15 and not self.booking_tool
        site = self.website >= 12
        if lexi and site:
            return "Lexi + website"
        if lexi:
            return "Lexi"
        if site:
            return "Website"
        return "Nurture"


def _find(patterns: list[str], text: str) -> str | None:
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return m.group(0)
    return None


def _quote(text: str, hit: str, width: int = 90) -> str:
    """A short slice of the review around the matching words."""
    i = text.lower().find(hit.lower())
    start = max(0, i - width // 2)
    snippet = text[start:start + width].strip().replace("\n", " ")
    return ("…" if start else "") + snippet + ("…" if start + width < len(text) else "")


def _days_ago(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).days


def is_social_only(url: str) -> bool:
    return any(h in url.lower() for h in SOCIAL_ONLY_HOSTS)


def score(s: Salon) -> Score:
    sc = Score()
    lname = s.name.lower()

    # ── Hard skips ──
    if s.status and s.status != "OPERATIONAL":
        sc.excluded = "not trading (Google says closed)"
    elif any(c in lname for c in CHAINS):
        sc.excluded = "chain or franchise"
    if sc.excluded:
        sc.reasons.append(f"Skipped: {sc.excluded}")
        return sc

    # ── Need: what their customers say ──
    strong_hits = 0
    medium_hits = 0
    apologies = 0
    for r in s.reviews:
        text = r.text or ""
        hit_type, hit = None, None
        for kind, pats in STRONG_PAIN.items():
            hit = _find(pats, text)
            if hit:
                hit_type = kind
                break
        if hit:
            strong_hits += 1
            if hit_type not in sc.pain_types:
                sc.pain_types.append(hit_type)
            if len(sc.evidence) < 3:
                sc.evidence.append(_quote(text, hit))
        else:
            for kind, pats in MEDIUM_PAIN.items():
                hit = _find(pats, text)
                if hit:
                    medium_hits += 1
                    if kind not in sc.pain_types:
                        sc.pain_types.append(kind)
                    if len(sc.evidence) < 3:
                        sc.evidence.append(_quote(text, hit))
                    break
        if r.owner_reply and _find(OWNER_APOLOGY, r.owner_reply):
            apologies += 1

    if apologies:
        sc.need += min(10, apologies * 5)
        sc.reasons.append(f"Owner has apologised {apologies}x in review replies for a missed message or mix-up")
    review_pts = min(35, strong_hits * 12 + medium_hits * 5)
    if strong_hits:
        sc.reasons.append(f"{strong_hits} review(s) complain about missed messages, double bookings or cancellations")
    if medium_hits:
        sc.reasons.append(f"{medium_hits} review(s) mention waiting, lateness or struggling to get a slot")
    sc.need += review_pts

    # How they take bookings, from their website
    site = s.site or {}
    tool = site.get("booking_tool") or ""
    if tool:
        sc.booking_tool = tool
        sc.need -= 15
        sc.reasons.append(f"Already uses {tool} for online booking (harder Lexi sell)")
    else:
        if s.website and not site.get("unreachable") and not site.get("unchecked"):
            sc.need += 5
            sc.reasons.append("No online booking system on their website")
        elif not s.website:
            sc.need += 5
            sc.reasons.append("No website, so bookings must come by phone or WhatsApp")
    if site.get("whatsapp_booking") or any("whatsapp" in (r.text or "").lower() for r in s.reviews):
        sc.need += 5
        sc.reasons.append("Clients already book through WhatsApp")
    if s.phone and SA_MOBILE.match(s.phone.replace(" ", "")):
        sc.need += 3
        sc.reasons.append("Listed number is a cellphone, so the owner is likely answering it themselves")
    sc.need = max(0, min(50, sc.need))

    # ── Website opportunity ──
    if not s.website:
        sc.website = 15
        sc.reasons.append("No website listed on Google")
    elif is_social_only(s.website):
        sc.website = 12
        sc.reasons.append("Their 'website' is only a Facebook/Instagram/link page")
    elif site.get("unreachable"):
        sc.website = 10
        sc.reasons.append("Website listed on Google doesn't load")

    # ── Can they pay: busy, established, well rated ──
    n = s.review_count or 0
    if n >= 400:
        vol, why = 12, f"{n} Google reviews (very big, may already have systems)"
    elif n >= 100:
        vol, why = 20, f"{n} Google reviews, a busy salon"
    elif n >= 30:
        vol, why = 15, f"{n} Google reviews, steady trade"
    elif n >= 10:
        vol, why = 8, f"{n} Google reviews, small but active"
    else:
        vol, why = 0, f"Only {n} Google reviews, may be too small or new"
    sc.can_pay += vol
    sc.reasons.append(why)

    if s.rating is not None:
        if s.rating >= 4.5:
            sc.can_pay += 8
        elif s.rating >= 4.0:
            sc.can_pay += 6
        elif s.rating >= 3.5:
            sc.can_pay += 3
        sc.reasons.append(f"Rated {s.rating}★")

    recent = [d for d in (_days_ago(r.when) for r in s.reviews) if d is not None]
    if recent and min(recent) <= 120:
        sc.can_pay += 7
        sc.reasons.append(f"Newest review is {min(recent)} days old, still trading actively")

    return sc
