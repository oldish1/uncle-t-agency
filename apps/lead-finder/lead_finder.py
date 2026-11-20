#!/usr/bin/env python3
"""Salon lead finder: finds Cape Town salons whose own customers complain about
the problems Lexi fixes, checks they're busy enough to pay, and drafts the
first WhatsApp message for each.

    python apps/lead-finder/lead_finder.py                      # full sweep, Google
    python apps/lead-finder/lead_finder.py --source apify       # deeper reviews
    python apps/lead-finder/lead_finder.py --areas Bellville Parow --queries "hair salon"
    python apps/lead-finder/lead_finder.py --from-raw data/leads/raw-2026-09-22.json   # re-score, no API calls

Writes outputs/leads/<date>/report.md (read this) and leads.csv (import into Sheets).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import outreach  # noqa: E402
import site_check  # noqa: E402
import sources  # noqa: E402
from scoring import Review, Salon, Score, score  # noqa: E402

AREAS = ["Bellville", "Parow", "Goodwood", "Mitchells Plain", "Kuils River", "Brackenfell", "Elsies River",
         "Athlone", "Durbanville", "Kraaifontein", "Belhar", "Delft"]
QUERIES = ["hair salon", "braiding salon", "nail salon", "lash and brow"]
# Already talking to these, flag them instead of pitching cold.
IN_PIPELINE = ["chales", "zanzibar", "sistergirl", "reeva", "jem hair", "no love lost"]

SEEN_FILE = ROOT / "data" / "leads" / "seen.json"


def collect(source: str, areas: list[str], queries: list[str]) -> list[Salon]:
    found: dict[str, Salon] = {}
    for area in areas:
        try:
            if source == "apify":
                batch = sources.apify_search(queries, area)
            else:
                batch = [s for q in queries for s in sources.google_search(q, area)]
        except sources.SourceError as e:
            print(f"  ! {e}")
            if not found:
                raise SystemExit(1)
            continue
        for s in batch:
            key = s.place_id or f"{s.name}|{s.phone}"
            found.setdefault(key, s)
        print(f"  {area}: {len(found)} salons so far")
    return list(found.values())


def load_raw(path: Path) -> list[Salon]:
    data = json.loads(path.read_text())
    out = []
    for d in data:
        d["reviews"] = [Review(**r) for r in d.get("reviews", [])]
        out.append(Salon(**d))
    return out


def load_seen() -> set[str]:
    try:
        return set(json.loads(SEEN_FILE.read_text()))
    except (OSError, ValueError):
        return set()


def write_outputs(ranked: list[tuple[Salon, Score]], out_dir: Path, top: int, seen: set[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "leads.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Tier", "Score", "Pitch", "Salon", "Area", "Phone", "WhatsApp", "Rating", "Reviews",
                    "Website", "Booking tool", "Need", "Website gap", "Can pay", "New?", "Why", "Evidence",
                    "First message", "Maps"])
        for s, sc in ranked:
            w.writerow([sc.tier, sc.total, sc.pitch, s.name, s.area, s.phone, outreach.whatsapp_link(s.phone),
                        s.rating or "", s.review_count, s.website, sc.booking_tool, sc.need, sc.website,
                        sc.can_pay, "" if s.place_id in seen else "new", " | ".join(sc.reasons),
                        " | ".join(sc.evidence), outreach.first_message(s, sc) if sc.tier != "Skip" else "",
                        s.maps_url])

    tiers = {t: sum(1 for _, sc in ranked if sc.tier == t) for t in ("Hot", "Warm", "Cold", "Skip")}
    lines = [
        f"# Salon leads, {datetime.now():%d %B %Y}",
        "",
        f"{len(ranked)} salons checked. **{tiers['Hot']} hot**, {tiers['Warm']} warm, "
        f"{tiers['Cold']} cold, {tiers['Skip']} skipped (chains, closed, or already in the pipeline).",
        "",
        "Score is out of 100: need for Lexi (50) + website gap (15) + can they pay (35). "
        "Full list with every salon is in `leads.csv`, ready to import into Google Sheets.",
        "",
    ]
    for i, (s, sc) in enumerate([r for r in ranked if r[1].tier in ("Hot", "Warm")][:top], 1):
        wa = outreach.whatsapp_link(s.phone)
        new = "" if s.place_id in seen else " · new this run"
        lines += [
            f"## {i}. {s.name} ({sc.total}/100, {sc.tier}){new}",
            "",
            f"**Pitch:** {sc.pitch} · **Area:** {s.area} · **Rating:** {s.rating or '?'}★ from {s.review_count} reviews",
            f"**Phone:** {s.phone or 'none listed'}" + (f" · [Open WhatsApp]({wa})" if wa else "")
            + (f" · [Google Maps]({s.maps_url})" if s.maps_url else ""),
            f"**Website:** {s.website or 'none'}" + (f" (uses {sc.booking_tool})" if sc.booking_tool else ""),
            "",
            "Why they're on the list:",
            *[f"- {r}" for r in sc.reasons],
        ]
        if sc.evidence:
            lines += ["", "What their customers wrote:", *[f"> {q}" for q in sc.evidence]]
        lines += ["", "First message (edit before sending):", "", "```", outreach.first_message(s, sc), "```",
                  "", "If no reply after a week, send this once, then stop:", "", "```", outreach.FOLLOW_UP, "```", ""]
    (out_dir / "report.md").write_text("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser(description="Find Cape Town salons that need Lexi and can pay for it.")
    ap.add_argument("--source", choices=["google", "apify"], default="google")
    ap.add_argument("--areas", nargs="+", default=AREAS)
    ap.add_argument("--queries", nargs="+", default=QUERIES)
    ap.add_argument("--top", type=int, default=25, help="how many leads to write up in the report")
    ap.add_argument("--from-raw", type=Path, help="re-score a saved sweep without calling any API")
    ap.add_argument("--no-site-check", action="store_true", help="skip opening each salon's website")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    today = f"{datetime.now():%Y-%m-%d}"
    if args.from_raw:
        salons = load_raw(args.from_raw)
        print(f"Loaded {len(salons)} salons from {args.from_raw}")
    else:
        print(f"Searching {len(args.areas)} areas for: {', '.join(args.queries)}")
        salons = collect(args.source, args.areas, args.queries)
        if not args.no_site_check:
            print("Checking websites for booking systems…")
            for s in salons:
                s.site = site_check.check(s.website)
        raw = ROOT / "data" / "leads" / f"raw-{today}.json"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_text(json.dumps([asdict(s) for s in salons], indent=1, ensure_ascii=False))

    ranked = []
    for s in salons:
        sc = score(s)
        if not sc.excluded and any(p in s.name.lower() for p in IN_PIPELINE):
            sc.excluded = "already in the pipeline"
            sc.reasons.insert(0, "Skipped: already in the pipeline")
        ranked.append((s, sc))
    ranked.sort(key=lambda r: (r[1].tier != "Skip", r[1].total), reverse=True)

    seen = load_seen()
    out_dir = args.out or ROOT / "outputs" / "leads" / today
    write_outputs(ranked, out_dir, args.top, seen)
    if not args.from_raw:
        SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        SEEN_FILE.write_text(json.dumps(sorted(seen | {s.place_id for s in salons if s.place_id})))

    hot = [s.name for s, sc in ranked if sc.tier == "Hot"]
    print(f"\nDone. {len(hot)} hot leads{': ' + ', '.join(hot[:5]) if hot else ''}")
    print(f"Report: {out_dir / 'report.md'}")


if __name__ == "__main__":
    main()
