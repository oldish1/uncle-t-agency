"""Visibility check: where does a client show up in search, and how many of their pages are indexed.

Runs the same fixed searches every time (from data/visibility/<client>.json) through Firecrawl,
so a "before" and an "after" are directly comparable. Writes a dated JSON + markdown snapshot to
outputs/visibility/<client>/.

Usage:  python3 scripts/visibility_check.py chales
        python3 scripts/visibility_check.py chales --compare 2026-11-20
"""
import json, sys, os, time, datetime, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.firecrawl.dev/v1/search"
KEY = os.environ.get("FIRECRAWL_API_KEY", "proxy-injects-this")


def search(q, country, limit=10):
    body = json.dumps({"query": q, "limit": limit, "country": country}).encode()
    req = urllib.request.Request(API, data=body, method="POST",
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            data = json.load(urllib.request.urlopen(req, timeout=60)).get("data", [])
            time.sleep(7)  # stay under Firecrawl's per-minute search limit
            return data
        except urllib.error.HTTPError as e:
            if attempt == 4:
                raise
            time.sleep(30 if e.code == 429 else 5)


def classify(url, cfg):
    u = url.lower()
    if cfg["domain"] in u:
        return "website"
    if any(b in u for b in cfg["brand_terms"]):
        return "social"
    return None


def run(name):
    cfg = json.load(open(os.path.join(ROOT, "data/visibility", f"{name}.json")))
    today = datetime.date.today().isoformat()
    rows = []
    for q in cfg["queries"]:
        res = search(q, cfg["country"])
        site = next((i + 1 for i, r in enumerate(res) if classify(r.get("url", ""), cfg) == "website"), None)
        own = [i + 1 for i, r in enumerate(res) if classify(r.get("url", ""), cfg)]
        rows.append({"query": q, "website_pos": site, "any_own_positions": own,
                     "top3": [r.get("url", "")[:90] for r in res[:3]]})
        print(f"{q:42} website: {site or '-':>3}   own results: {own or '-'}")
    idx = search(f"site:{cfg['domain']}", cfg["country"], 50)
    indexed = sorted({r.get("url", "") for r in idx if cfg["domain"] in r.get("url", "")})
    print(f"\nIndexed pages found: {len(indexed)}")
    snap = {"client": cfg["client"], "date": today, "results": rows, "indexed_pages": indexed}
    out = os.path.join(ROOT, "outputs/visibility", name); os.makedirs(out, exist_ok=True)
    json.dump(snap, open(os.path.join(out, f"{today}.json"), "w"), indent=2)
    return snap


def compare(name, old_date, new):
    old = json.load(open(os.path.join(ROOT, "outputs/visibility", name, f"{old_date}.json")))
    o = {r["query"]: r for r in old["results"]}
    lines = [f"# {new['client']}: visibility, {old_date} vs {new['date']}", "",
             "| Search | Website then | Website now | Own results now |", "|---|---|---|---|"]
    for r in new["results"]:
        p = o.get(r["query"], {})
        lines.append(f"| {r['query']} | {p.get('website_pos') or 'not top 10'} | {r['website_pos'] or 'not top 10'} | {', '.join(map(str, r['any_own_positions'])) or '-'} |")
    lines += ["", f"Indexed pages: {len(old['indexed_pages'])} then, {len(new['indexed_pages'])} now."]
    path = os.path.join(ROOT, "outputs/visibility", name, f"compare-{old_date}-to-{new['date']}.md")
    open(path, "w").write("\n".join(lines) + "\n")
    print("\n" + "\n".join(lines)); print(f"\nSaved {path}")


if __name__ == "__main__":
    name = sys.argv[1]
    snap = run(name)
    if "--compare" in sys.argv:
        compare(name, sys.argv[sys.argv.index("--compare") + 1], snap)
