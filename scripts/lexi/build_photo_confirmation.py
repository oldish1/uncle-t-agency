"""Fix14: booking confirmation with the salon photo and a Get Directions button.

Module 79 (plain text "You are all set...") becomes a WhatsApp interactive cta_url message:
image header, bold booking details, "Get Directions" button to Google Maps.
  330 code: builds the message JSON safely (client names with quotes can't break it)
  79  sends {{330.result.body}}
  79 onerror: 331 sends the old plain-text confirmation, then 332 Resume, so the
              sheet steps after 79 (80, 82) still run.

Usage: build_photo_confirmation.py <scenario json> <out file> <image url> <maps url>
The WhatsApp key stays inside the blueprint and is never printed.
"""
import copy, json, sys

SRC, OUT, IMG, MAPS = sys.argv[1:5]
M = "{{1.entry[].changes[].value.messages[]."

t = open(SRC).read()
d = json.loads(t[t.index("{"):])
sc = d.get("scenario", d)
bp = sc.get("blueprint", sc)
if isinstance(bp, str):
    bp = json.loads(bp)

mods, holder = {}, {}
def walk(fl):
    for i, m in enumerate(fl):
        mods[m["id"]] = m
        holder[m["id"]] = (fl, i)
        for r in m.get("routes", []) or []:
            walk(r.get("flow", []))
walk(bp["flow"])
assert not any(330 <= i < 340 for i in mods), "ids 330-339 already used"
c = mods[79]
assert c["mapper"]["dataStructureBodyContent"]["text"]["body"].startswith("You are all set"), "confirmation changed"
auth = [h for h in c["mapper"]["headers"] if h["name"] == "Authorization"][0]["value"]
old_mapper = copy.deepcopy(c["mapper"])

JS = r"""const clean = s => String(s || '').replace(/\s+/g, ' ').trim();
const name = clean(input.name);
const first = name.split(' ')[0] || 'there';
const body = [
  `You're all set, *${first}*! ✨`,
  '',
  `\u{1F487}‍♀️ *${clean(input.service)}*`,
  `\u{1F5D3}️ *${clean(input.day)}*`,
  `\u{1F550} *${clean(input.time)}*`,
  '\u{1F4CD} 46 Alexandra Street, Oakdale, Bellville',
  '',
  'See you soon! — Chanté'
].join('\n');
const msg = {
  messaging_product: 'whatsapp', to: input.to, type: 'interactive',
  interactive: {
    type: 'cta_url',
    header: { type: 'image', image: { link: input.image } },
    body: { text: body },
    footer: { text: 'Chales Hair Boutique' },
    action: { name: 'cta_url', parameters: { display_text: 'Get Directions', url: input.maps } }
  }
};
return { body: JSON.stringify(msg) };"""

x, y = c["metadata"]["designer"]["x"], c["metadata"]["designer"]["y"]
build = {"id": 330, "module": "code:ExecuteCode", "version": 1, "parameters": {},
         "metadata": {"designer": {"x": x - 150, "y": y - 200, "name": "Build photo confirmation"}},
         "mapper": {"input": [
             {"name": "to", "value": M + "from}}"},
             {"name": "name", "value": M + "text.body}}"},
             {"name": "service", "value": "{{86.`1`}}"},
             {"name": "day", "value": "{{86.`2`}}"},
             {"name": "time", "value": "{{86.`3`}}"},
             {"name": "image", "value": IMG},
             {"name": "maps", "value": MAPS}],
             "language": "javascript", "inputFormat": "editor", "dependencies": [],
             "codeEditorJavascript": JS}}

c["mapper"] = {"url": old_mapper["url"], "method": "post",
               "headers": [{"name": "Authorization", "value": auth},
                           {"name": "Content-Type", "value": "application/json"}],
               "contentType": "json", "inputMethod": "jsonString",
               "jsonStringBodyContent": "{{330.result.body}}", "shareCookies": False,
               "parseResponse": True, "allowRedirects": True, "stopOnHttpError": True,
               "requestCompressedContent": True}
c["metadata"]["designer"]["name"] = "Photo confirmation"
fallback = {"id": 331, "module": "http:MakeRequest", "version": 4, "mapper": old_mapper,
            "parameters": copy.deepcopy(c["parameters"]),
            "metadata": {"designer": {"x": x, "y": y + 250, "name": "Plain confirmation (backup)"}}}
resume = {"id": 332, "module": "builtin:Resume", "version": 1, "mapper": {}, "parameters": {},
          "metadata": {"designer": {"x": x + 250, "y": y + 250}}}
c["onerror"] = [fallback, resume]

fl, idx = holder[79]
fl.insert(idx, build)

out = {"name": bp.get("name", sc["name"]), "flow": bp["flow"], "metadata": bp["metadata"]}
for k in ("scheduling", "interface"):
    if k in bp:
        out[k] = bp[k]
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)

ids = []
def collect(fl):
    for m in fl:
        ids.append(m["id"])
        for e in m.get("onerror", []) or []:
            ids.append(e["id"])
        for r in m.get("routes", []) or []:
            collect(r["flow"])
collect(out["flow"])
print("modules:", len(ids), "duplicates:", len(ids) - len(set(ids)), "new:", sorted(i for i in ids if 330 <= i < 340))
