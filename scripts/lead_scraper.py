#!/usr/bin/env python3
"""Lead scraper agent for the AIOS workspace.

Pulls local businesses from Google Maps (via Apify), checks any listed
website for a real booking system (via Firecrawl), and writes a ranked
CSV of outreach targets: no website scores highest, a website with no
booking system next, a website that already has one deprioritised.

Run through the workspace environment:
    uv run python scripts/lead_scraper.py --vertical "hair salon"
    uv run python scripts/lead_scraper.py --vertical "hair salon" --suburbs Bellville,Parow --limit 30

See plans/2026-09-27-lead-scraper-agent.md for the full design.

NOTE on the Apify Google Maps actor's input/output field names: this
was written without a live test call (this container's network policy
was blocking api.apify.com at build time). The field names below are
the documented shape as of writing, but per the plan's own Step 2,
confirm them against a real first run with --raw-sample and adjust if
Apify's actor has changed since.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

from utils.config import get_env

APIFY_BASE_URL = "https://api.apify.com/v2"
GOOGLE_MAPS_ACTOR = "apify~google-maps-scraper"

FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v2"

BOOKING_SIGNALS = [
    "book now",
    "book an appointment",
    "book online",
    "make an appointment",
    "schedule an appointment",
    "book a slot",
    "calendly.com",
    "fresha.com",
    "booksy.com",
    "simplybook.me",
    "setmore.com",
    "square.site",
    "squareup.com/appointments",
    "acuityscheduling.com",
    "timify.com",
    "schedulicity.com",
]

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


class LeadScraperError(RuntimeError):
    """A plain-English failure that's safe to show the founder."""


class ApifyClient:
    def __init__(self, token: str | None = None, timeout: int = 120):
        self.token = token or get_env("APIFY_API_TOKEN")
        self.timeout = timeout

    def run_google_maps_search(
        self, search_strings: list[str], max_places_per_search: int = 30, language: str = "en"
    ) -> list[dict[str, Any]]:
        """Run the Google Maps actor synchronously and return the raw dataset items."""
        url = (
            f"{APIFY_BASE_URL}/acts/{GOOGLE_MAPS_ACTOR}/run-sync-get-dataset-items"
            f"?token={self.token}"
        )
        payload = {
            "searchStringsArray": search_strings,
            "maxCrawledPlacesPerSearch": max_places_per_search,
            "language": language,
            "skipClosedPlaces": False,
        }
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            detail = ""
            if getattr(exc, "response", None) is not None:
                detail = exc.response.text[:500]
            raise LeadScraperError(
                f"Apify Google Maps search failed: {detail or exc}"
            ) from exc
        try:
            return response.json()
        except ValueError as exc:
            raise LeadScraperError("Apify returned a response that was not JSON.") from exc


class FirecrawlBookingChecker:
    """Thin, purpose-built Firecrawl client: only needs a scrape-and-search-text.

    Deliberately not importing FirecrawlClient from firecrawl_tool.py to avoid
    coupling this script's error handling to that file's CLI-oriented shape;
    the API call itself is the same one FirecrawlClient.scrape() makes.
    """

    def __init__(self, api_key: str | None = None, timeout: int = 60):
        self.api_key = api_key or get_env("FIRECRAWL_API_KEY")
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def has_booking_signal(self, url: str) -> bool | None:
        """Return True/False, or None if the site couldn't be scraped at all."""
        try:
            response = requests.post(
                f"{FIRECRAWL_BASE_URL}/scrape",
                headers=self.headers,
                json={"url": url, "formats": ["markdown", "links"]},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError):
            return None
        if data.get("success") is False:
            return None
        page = data.get("data", {})
        markdown = (page.get("markdown") or "").lower()
        links = " ".join(page.get("links") or []).lower()
        haystack = markdown + " " + links
        return any(signal in haystack for signal in BOOKING_SIGNALS)


def load_verticals(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise LeadScraperError(
            f"No vertical config at {config_path}. "
            "Add one to scripts/lead_scraper_verticals.json first."
        )
    return json.loads(config_path.read_text(encoding="utf-8"))


def normalise_phone(raw: str | None) -> str:
    if not raw:
        return ""
    return re.sub(r"\D", "", raw)


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for row in rows:
        phone_key = normalise_phone(row.get("phone"))
        name_key = f"{(row.get('name') or '').strip().lower()}|{(row.get('address') or '').strip().lower()}"
        key = phone_key or name_key
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def score_tier(has_website: bool, has_booking_signal: bool | None) -> str:
    if not has_website:
        return "A - no website"
    if has_booking_signal is False:
        return "B - website, no booking found"
    if has_booking_signal is True:
        return "C - already has booking"
    return "B - website, booking unknown (site unreachable)"


def run(
    vertical: str,
    suburbs: list[str] | None,
    limit_per_suburb: int,
    config_path: Path,
    out_path: Path | None,
    skip_booking_check: bool,
    raw_sample: bool,
) -> Path:
    verticals = load_verticals(config_path)
    if vertical not in verticals:
        available = ", ".join(sorted(verticals))
        raise LeadScraperError(
            f'"{vertical}" isn\'t in {config_path.name}. Available: {available}'
        )
    vertical_config = verticals[vertical]
    target_suburbs = suburbs or vertical_config["suburbs"]
    terms = vertical_config["terms"]

    search_strings = [
        f"{term} {suburb}, Cape Town" for suburb in target_suburbs for term in terms
    ]

    print(f"Searching Google Maps: {len(search_strings)} queries across {len(target_suburbs)} suburb(s)...")
    apify = ApifyClient()
    raw_results = apify.run_google_maps_search(search_strings, max_places_per_search=limit_per_suburb)
    print(f"Apify returned {len(raw_results)} raw results.")

    if raw_sample and raw_results:
        print("\n--- Raw sample (first result, for field-name verification) ---")
        print(json.dumps(raw_results[0], indent=2)[:3000])
        print("--- end sample ---\n")

    rows: list[dict[str, Any]] = []
    for item in raw_results:
        rows.append(
            {
                "name": item.get("title") or item.get("name") or "",
                "phone": item.get("phone") or item.get("phoneUnformatted") or "",
                "address": item.get("address") or "",
                "suburb": "",  # filled in below from which query matched, best-effort
                "rating": item.get("totalScore") or item.get("rating") or "",
                "review_count": item.get("reviewsCount") or item.get("userRatingsTotal") or 0,
                "website_url": item.get("website") or "",
            }
        )

    rows = dedupe(rows)
    print(f"{len(rows)} unique businesses after de-duplication.")

    checker = None if skip_booking_check else FirecrawlBookingChecker()
    firecrawl_calls = 0
    for row in rows:
        has_website = bool(row["website_url"])
        row["has_website"] = "yes" if has_website else "no"
        if has_website and checker is not None:
            firecrawl_calls += 1
            row["has_booking_signal_raw"] = checker.has_booking_signal(row["website_url"])
        else:
            row["has_booking_signal_raw"] = None
        row["has_booking_signal"] = {
            True: "yes",
            False: "no",
            None: "unknown" if has_website else "",
        }[row["has_booking_signal_raw"]]
        row["score_tier"] = score_tier(has_website, row["has_booking_signal_raw"])

    tier_order = {"A - no website": 0, "B - website, no booking found": 1, "B - website, booking unknown (site unreachable)": 2, "C - already has booking": 3}
    rows.sort(key=lambda r: (tier_order.get(r["score_tier"], 9), -(r["review_count"] or 0)))

    if out_path is None:
        date_str = time.strftime("%Y-%m-%d")
        suburb_slug = "all" if not suburbs else "-".join(s.lower().replace(" ", "-").replace("'", "") for s in suburbs)
        vertical_slug = vertical.lower().replace(" ", "-")
        out_path = WORKSPACE_ROOT / "outputs" / "leads" / f"{date_str}-{vertical_slug}-{suburb_slug}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    columns = ["name", "phone", "address", "rating", "review_count", "has_website", "website_url", "has_booking_signal", "score_tier"]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    tier_counts: dict[str, int] = {}
    for row in rows:
        tier_counts[row["score_tier"]] = tier_counts.get(row["score_tier"], 0) + 1

    print(f"\nWrote {len(rows)} rows to {out_path}")
    print(f"Firecrawl checks spent: {firecrawl_calls}")
    for tier, count in sorted(tier_counts.items()):
        print(f"  {tier}: {count}")

    return out_path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vertical", required=True, help='e.g. "hair salon" (must match a key in the config file)')
    parser.add_argument("--suburbs", help="Comma-separated, overrides the config file's default suburb list for this vertical")
    parser.add_argument("--limit", type=int, default=30, help="Max Maps results per search query (default 30)")
    parser.add_argument(
        "--config",
        default=str(WORKSPACE_ROOT / "scripts" / "lead_scraper_verticals.json"),
        help="Path to the vertical config JSON",
    )
    parser.add_argument("-o", "--output", help="Output CSV path, default outputs/leads/<date>-<vertical>-<suburbs>.csv")
    parser.add_argument("--skip-booking-check", action="store_true", help="Skip the Firecrawl booking-link check (faster, cheaper, less accurate ranking)")
    parser.add_argument("--raw-sample", action="store_true", help="Print the first raw Apify result, for verifying field names")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    suburbs = [s.strip() for s in args.suburbs.split(",")] if args.suburbs else None
    try:
        run(
            vertical=args.vertical,
            suburbs=suburbs,
            limit_per_suburb=args.limit,
            config_path=Path(args.config),
            out_path=Path(args.output) if args.output else None,
            skip_booking_check=args.skip_booking_check,
            raw_sample=args.raw_sample,
        )
        return 0
    except (LeadScraperError, RuntimeError) as exc:
        print(f"Lead scraper: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
