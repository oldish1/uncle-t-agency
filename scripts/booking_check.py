#!/usr/bin/env python3
"""Second-pass check for Scout: does this business already have a booking page?

Google's website field is often empty even when a salon uses Fresha, Setmore, Booksy and so on.
For each business this searches the web (Firecrawl) and flags results on a known booking platform
whose address contains the business name. A human should glance at any hint before skipping a lead.

    uv run python scripts/booking_check.py "Hugo The Hair Company" Parow
"""
from __future__ import annotations

import re
import sys

import requests

from utils.config import get_env

PLATFORMS = re.compile(
    r"fresha\.com|setmore\.com|booksy\.com|treatwell|calendly\.com|simplybook|square\.site|timely\.|vagaro|"
    r"schedulicity|heygoldie|phorest|planyo|acuityscheduling|bookings\.|/book\b|salonist|booker\.com",
    re.I,
)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def find_booking_hint(name: str, suburb: str = "", city: str = "cape town") -> str:
    """Return a booking-page URL that looks like this business's, or ''."""
    key = get_env("FIRECRAWL_API_KEY")
    query = f"{name} {suburb} {city} book online"
    resp = requests.post(
        "https://api.firecrawl.dev/v2/search",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"query": query, "limit": 8},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json().get("data", {})
    results = data.get("web", []) if isinstance(data, dict) else data
    want = slug(name)
    words = [slug(w) for w in name.split() if len(w) > 2][:2]
    for r in results:
        url = r.get("url", "")
        if not PLATFORMS.search(url):
            continue
        u = slug(url)
        if want[:14] in u or (len(words) == 2 and all(w in u for w in words)):
            if "bristol" in url.lower() or "-uk" in url.lower():
                continue
            return url
    return ""


if __name__ == "__main__":
    print(find_booking_hint(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "") or "no booking page found")
