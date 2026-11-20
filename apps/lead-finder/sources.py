"""Where the salons come from.

google  Google Places API (official). Needs GOOGLE_PLACES_API_KEY. Returns up to
        5 reviews per salon. Free monthly allowance covers a full Cape Town sweep.
apify   Apify's Google Maps scraper. Needs APIFY_API_TOKEN. Slower and paid per
        result, but pulls 30+ reviews per salon, so pain shows up far more often.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from utils.config import get_env  # noqa: E402

from scoring import Review, Salon  # noqa: E402

PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
PLACES_FIELDS = ",".join([
    "places.id", "places.displayName", "places.formattedAddress", "places.nationalPhoneNumber",
    "places.websiteUri", "places.rating", "places.userRatingCount", "places.businessStatus",
    "places.googleMapsUri", "places.primaryTypeDisplayName", "places.reviews", "nextPageToken",
])


class SourceError(RuntimeError):
    """Plain-English failure that's safe to show Theo."""


def from_places_json(p: dict, area: str) -> Salon:
    reviews = []
    for r in p.get("reviews", []) or []:
        text = (r.get("originalText") or r.get("text") or {}).get("text", "")
        reviews.append(Review(text=text, rating=r.get("rating"), when=r.get("publishTime")))
    return Salon(
        place_id=p.get("id", ""),
        name=(p.get("displayName") or {}).get("text", ""),
        address=p.get("formattedAddress", ""),
        area=area,
        phone=p.get("nationalPhoneNumber", ""),
        website=p.get("websiteUri", ""),
        rating=p.get("rating"),
        review_count=p.get("userRatingCount", 0) or 0,
        status=p.get("businessStatus", "OPERATIONAL"),
        maps_url=p.get("googleMapsUri", ""),
        category=(p.get("primaryTypeDisplayName") or {}).get("text", ""),
        reviews=reviews,
    )


def google_search(query: str, area: str, max_pages: int = 2) -> list[Salon]:
    key = get_env("GOOGLE_PLACES_API_KEY")
    headers = {"X-Goog-Api-Key": key, "X-Goog-FieldMask": PLACES_FIELDS, "Content-Type": "application/json"}
    body = {"textQuery": f"{query} in {area}, Cape Town", "regionCode": "ZA", "languageCode": "en", "pageSize": 20}
    out: list[Salon] = []
    for _ in range(max_pages):
        resp = requests.post(PLACES_URL, headers=headers, json=body, timeout=30)
        if resp.status_code == 403:
            raise SourceError("Google turned the key away. The Places API (New) probably isn't switched on for this key yet.")
        if resp.status_code == 400 and "API key not valid" in resp.text:
            raise SourceError("That Google key isn't valid. Copy it again from Google Cloud, Credentials.")
        if not resp.ok:
            raise SourceError(f"Google search failed ({resp.status_code}) for '{query}' in {area}.")
        data = resp.json()
        out += [from_places_json(p, area) for p in data.get("places", [])]
        token = data.get("nextPageToken")
        if not token:
            break
        body = {**body, "pageToken": token}
        time.sleep(1)
    return out


def from_apify_json(p: dict, area: str) -> Salon:
    reviews = [
        Review(text=r.get("text") or "", rating=r.get("stars"), when=r.get("publishedAtDate"),
               owner_reply=r.get("responseFromOwnerText"))
        for r in p.get("reviews", []) or []
    ]
    return Salon(
        place_id=p.get("placeId", "") or p.get("url", ""),
        name=p.get("title", ""),
        address=p.get("address", ""),
        area=area,
        phone=p.get("phone", "") or "",
        website=p.get("website", "") or "",
        rating=p.get("totalScore"),
        review_count=p.get("reviewsCount", 0) or 0,
        status="CLOSED_PERMANENTLY" if p.get("permanentlyClosed") else ("CLOSED_TEMPORARILY" if p.get("temporarilyClosed") else "OPERATIONAL"),
        maps_url=p.get("url", ""),
        category=p.get("categoryName", "") or "",
        reviews=reviews,
    )


def apify_search(queries: list[str], area: str, per_query: int = 20, max_reviews: int = 30) -> list[Salon]:
    token = get_env("APIFY_API_TOKEN")
    url = f"https://api.apify.com/v2/acts/compass~crawler-google-places/run-sync-get-dataset-items?token={token}"
    payload = {
        "searchStringsArray": queries,
        "locationQuery": f"{area}, Cape Town, South Africa",
        "maxCrawledPlacesPerSearch": per_query,
        "language": "en",
        "maxReviews": max_reviews,
        "reviewsSort": "newest",
        "scrapeReviewsPersonalData": False,
    }
    resp = requests.post(url, json=payload, timeout=600)
    if resp.status_code == 401:
        raise SourceError("Apify didn't accept the token. Copy it again from Apify, Settings, Integrations.")
    if not resp.ok:
        raise SourceError(f"Apify run failed ({resp.status_code}) for {area}.")
    return [from_apify_json(p, area) for p in resp.json()]
