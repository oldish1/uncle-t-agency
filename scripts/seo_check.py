#!/usr/bin/env python3
"""Quick website check for a local business, used by the /seo skill.

Usage: python3 scripts/seo_check.py https://example.co.za [--json]

Fetches the home page, robots.txt and sitemap.xml and reports what a Google or AI crawler
sees: title, description, headings, schema, phone numbers, hours, analytics, images, and a
few risks (public bank details). Standard library only. Reads nothing private.
"""
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from html import unescape
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; UncleT-SEO-Check/1.0)"
AI_BOTS = ["OAI-SearchBot", "GPTBot", "Claude-SearchBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]


def fetch(url, head=False, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD" if head else "GET")
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            body = b"" if head else r.read()
            return r.status, dict(r.headers), body.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), ""
    except Exception as e:  # network, TLS, DNS
        return 0, {}, f"ERROR {e}"


def text_of(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()


def first(pattern, s, flags=re.S | re.I):
    m = re.search(pattern, s, flags)
    return unescape(m.group(1)).strip() if m else None


def walk(node):
    """Yield every JSON-LD object, including those inside @graph and nested fields."""
    if isinstance(node, dict):
        if "@type" in node:
            yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def check(url):
    if not url.startswith("http"):
        url = "https://" + url
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    out = {"url": url, "problems": [], "good": []}
    bad, good = out["problems"], out["good"]

    status, headers, html = fetch(url)
    out["status"] = status
    if status != 200:
        bad.append(f"Home page did not load (status {status}). {html[:120]}")
        return out

    out["title"] = first(r"<title[^>]*>(.*?)</title>", html)
    out["description"] = first(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html)
    out["canonical"] = first(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', html)
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S | re.I)
    out["h1"] = [text_of(h) for h in h1s]
    out["h2_count"] = len(re.findall(r"<h2[\s>]", html, flags=re.I))
    out["words"] = len(text_of(html).split())
    out["bytes"] = len(html.encode())

    # title / description
    if not out["title"]:
        bad.append("No page title.")
    elif not re.search(r"(?i)bellville|cape town|durbanville|parow|goodwood|mitchell|oakdale|[a-z]{4,} (?:city|town)", out["title"]):
        bad.append("Title has no place name, so Google can't tell where the business is.")
    if not out["description"]:
        bad.append("No meta description.")
    if len(out["h1"]) != 1:
        bad.append(f"Expected one H1, found {len(out['h1'])}.")

    # schema
    blocks = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, flags=re.S | re.I)
    types, hours, phone_schema = [], [], None
    for b in blocks:
        try:
            data = json.loads(b)
        except Exception:
            bad.append("A schema (JSON-LD) block is broken and can't be read.")
            continue
        for node in walk(data):
            t = node.get("@type")
            types += t if isinstance(t, list) else [t]
            phone_schema = phone_schema or node.get("telephone")
            for h in node.get("openingHoursSpecification", []) or []:
                hours.append(f"{h.get('dayOfWeek')} {h.get('opens')}-{h.get('closes')}")
            if node.get("geo") or node.get("@type") == "GeoCoordinates":
                types.append("geo")
            if node.get("aggregateRating"):
                types.append("aggregateRating")
    out["schema_types"] = sorted({t for t in types if t})
    out["schema_hours"] = hours
    out["schema_phone"] = phone_schema
    if not blocks:
        bad.append("No schema markup. Google and AI tools get no clean business details.")
    elif not any(t and ("Salon" in t or "Business" in t or "Store" in t or "Service" in t) for t in out["schema_types"]):
        bad.append("Schema has no LocalBusiness-type entry.")
    else:
        good.append("Local business schema present.")
    if "geo" not in out["schema_types"]:
        bad.append("Schema has no map coordinates (geo).")

    # contact signals
    out["tel_links"] = sorted(set(re.findall(r'href=["\']tel:([^"\']+)', html)))
    out["whatsapp_links"] = sorted(set(re.findall(r'wa\.me/(\d+)', html)))
    visible = text_of(html)
    out["phones_in_text"] = sorted(set(re.findall(r"(?:\+27|0)[\s-]?\d{2}[\s-]?\d{3}[\s-]?\d{4}", visible)))[:8]
    norm = lambda p: re.sub(r"\D", "", p or "")[-9:]
    nums = {norm(p) for p in out["tel_links"] + out["phones_in_text"] + [phone_schema or ""] if norm(p)}
    if len(nums) > 1:
        out["problems"].append("More than one phone number appears (" + ", ".join(sorted(nums)) +
                               "). Fine if on purpose (calls vs booking), but check it matches the Google listing.")
    m = re.search(r"((?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day[^<]{0,80}\d{1,2}:\d{2}[^<]{0,40})", visible)
    out["hours_text"] = m.group(1)[:140] if m else None
    if hours and out["hours_text"]:
        out["hours_note"] = "Compare schema hours with the hours shown on the page and the Google listing."

    # tracking
    analytics = []
    if re.search(r"googletagmanager\.com/gtag/js\?id=G-[A-Z0-9]{6,}|gtag\(['\"]config['\"],\s*['\"]G-[A-Z0-9]{6,}", html):
        analytics.append("Google Analytics 4")
    if "googletagmanager.com/gtm.js" in html:
        analytics.append("Google Tag Manager")
    if re.search(r"plausible\.io|umami|matomo|clarity\.ms|connect\.facebook\.net.*fbevents|fbq\(", html):
        analytics.append("other tracker")
    out["analytics"] = analytics
    if not analytics:
        bad.append("No analytics. Nobody can say how many people visit or tap to book.")

    # map
    out["map_embed"] = bool(re.search(r"google\.com/maps/embed", html))
    if out["map_embed"]:
        m = re.search(r"google\.com/maps/embed\?pb=([^\"']+)", html)
        if m and re.search(r"0x[0-9a-f]+(?:%3A|:)0x1(?:!|$)", m.group(1)):
            bad.append("Map embed has a placeholder place ID, so it shows an address pin, not the business.")
    else:
        bad.append("No Google Maps embed.")

    # images
    imgs = re.findall(r"<img\b[^>]*>", html, flags=re.I)
    no_alt = [i for i in imgs if not re.search(r'alt=["\'][^"\']+', i, flags=re.I)]
    out["images"] = {"count": len(imgs), "missing_alt": len(no_alt)}
    heavy = []
    for src in sorted(set(re.findall(r'<img[^>]+src=["\']([^"\']+)', html, flags=re.I)))[:20]:
        if src.startswith("data:"):
            continue
        s, h, _ = fetch(urljoin(url, src), head=True, timeout=15)
        size = int(h.get("Content-Length", h.get("content-length", 0)) or 0)
        if size > 200_000:
            heavy.append((src, size // 1000))
    out["images"]["over_200kb"] = len(heavy)
    if heavy:
        bad.append(f"{len(heavy)} photos are over 200 KB (largest {max(s for _, s in heavy)} KB). Slow on prepaid data.")
    if re.search(r"IMG[-_]\d{6,}|WA\d{4}", " ".join(re.findall(r'<img[^>]+src=["\']([^"\']+)', html, flags=re.I))):
        bad.append("Photos still have phone or WhatsApp file names (IMG-2026...). Rename them to describe the work.")

    # risks
    if re.search(r"(?i)account\s*(?:number|no)[^a-z]{0,20}\d{7,}", visible):
        bad.append("A bank account number is shown publicly on the page. Remove it and give banking details in chat.")
    if re.search(r"(?i)5[\s-]*star rated", visible):
        bad.append("Page claims '5 star rated'. Make sure real reviews back it up.")

    # robots, sitemap
    rs, _, robots = fetch(base + "/robots.txt", timeout=15)
    out["robots_status"] = rs
    blocked = []
    if rs == 200:
        for bot in AI_BOTS:
            pat = rf"(?is)user-agent:\s*{re.escape(bot)}\s*(?:\r?\n(?!user-agent).*?)*?disallow:\s*/\s*(?:\r?\n|$)"
            if re.search(pat, robots):
                blocked.append(bot)
        if re.search(r"(?im)^user-agent:\s*\*\s*\r?\n(?:.*\r?\n)*?disallow:\s*/\s*$", robots):
            blocked.append("all bots (*)")
    out["ai_bots_blocked"] = blocked
    if blocked:
        bad.append("robots.txt blocks: " + ", ".join(blocked) + ".")
    ss, _, sm = fetch(base + "/sitemap.xml", timeout=15)
    out["sitemap_status"] = ss
    out["sitemap_urls"] = re.findall(r"<loc>(.*?)</loc>", sm) if ss == 200 else []
    if ss != 200:
        bad.append("No sitemap.xml.")
    elif len(out["sitemap_urls"]) <= 1:
        bad.append("Sitemap lists only one page. One page can't rank for every service.")
    else:
        good.append(f"Sitemap lists {len(out['sitemap_urls'])} pages.")
    if not url.startswith("https"):
        bad.append("Site isn't on HTTPS.")
    return out


def render(o):
    lines = [f"# Site check: {o['url']}", ""]
    if o.get("status") != 200:
        return "\n".join(lines + o["problems"])
    lines += [f"Title: {o.get('title')}", f"Description: {o.get('description')}",
              f"H1: {o.get('h1')}  |  H2 count: {o.get('h2_count')}  |  words: {o.get('words')}",
              f"Schema: {o.get('schema_types')}  |  hours in schema: {o.get('schema_hours')}",
              f"Phones: tel {o.get('tel_links')}, text {o.get('phones_in_text')}, schema {o.get('schema_phone')}, WhatsApp {o.get('whatsapp_links')}",
              f"Hours on page: {o.get('hours_text')}", f"Analytics: {o.get('analytics') or 'none'}",
              f"Images: {o.get('images')}", f"Sitemap pages: {len(o.get('sitemap_urls', []))}", "", "## Problems"]
    lines += [f"- {p}" for p in o["problems"]] or ["- none found"]
    lines += ["", "## Good"] + ([f"- {g}" for g in o["good"]] or ["- nothing flagged"])
    return "\n".join(lines)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    result = check(args[0])
    print(json.dumps(result, indent=2) if "--json" in sys.argv else render(result))
