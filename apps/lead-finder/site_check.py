"""Open a salon's website and see how they take bookings."""

from __future__ import annotations

import re

import requests

from scoring import BOOKING_PLATFORMS, is_social_only

HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36"}
WHATSAPP = re.compile(r"(wa\.me/|api\.whatsapp\.com|whatsapp to book|book (via|on|through) whatsapp)", re.I)


def read_html(html: str) -> dict:
    low = html.lower()
    tool = next((name for key, name in BOOKING_PLATFORMS.items() if key in low), "")
    return {"booking_tool": tool, "whatsapp_booking": bool(WHATSAPP.search(html))}


def check(url: str) -> dict:
    if not url or is_social_only(url):
        return {}
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
    except requests.exceptions.ProxyError:
        return {"unchecked": True}      # our network blocked it, says nothing about their site
    except requests.RequestException:
        return {"unreachable": True}
    if resp.status_code >= 400:
        return {"unreachable": True}
    return read_html(resp.text)
