"""Build Lexi's voice-note route into the live blueprint.

Reads the fetched scenario JSON, adds a router at the front:
  route A (voice notes)  -> ack, fetch media, download, transcribe, re-post as text
  route B (everything else) -> the existing flow, untouched
Writes the import file to private/. The WhatsApp key is copied from module 240
inside this script and never printed.
"""
import copy, json, sys

SRC, TRANSCRIBE_JSON, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HOOK_URL = sys.argv[4]  # Lexi's own webhook address (kept out of the repo)
M = "{{1.entry[].changes[].value.messages[]."
PROMPT = ("Chales Hair Boutique, a hair salon in Cape Town. Services: Wash and Blowdry, Trim, Precision Cut, "
          "Root Touch Up, Full Color, Hair Colour and Highlights, Brazilian and Keratin, Nanoplastia, "
          "Botox and Glowtox, Basin Treatment. Clients book, cancel or reschedule appointments.")

t = open(SRC).read()
d = json.loads(t[t.index("{"):])
sc = d.get("scenario", d)
bp = sc["blueprint"]
if isinstance(bp, str):
    bp = json.loads(bp)

mods = {}
def walk(fl):
    for m in fl:
        mods[m["id"]] = m
        for r in m.get("routes", []) or []:
            walk(r.get("flow", []))
walk(bp["flow"])
assert bp["flow"][0]["id"] == 1 and bp["flow"][1]["id"] == 2, "unexpected start of flow"
assert max(mods) < 301, "ids 301+ already used"
auth = [h for h in mods[240]["mapper"]["headers"] if h["name"] == "Authorization"][0]["value"]

def pos(x, y):
    return {"designer": {"x": x, "y": y}}

def http(id_, url, method="get", body=None, parse=True, headers_auth=True, stop=True, x=0, y=0, name=None):
    headers = [{"name": "Authorization", "value": auth}] if headers_auth else []
    mapper = {"url": url, "method": method, "headers": headers, "shareCookies": False,
              "parseResponse": parse, "allowRedirects": True, "stopOnHttpError": stop,
              "requestCompressedContent": True}
    if body is not None:
        headers.append({"name": "Content-Type", "value": "application/json"})
        mapper.update({"contentType": "json", "inputMethod": "jsonString", "jsonStringBodyContent": body})
    md = pos(x, y)
    if name:
        md["designer"]["name"] = name
    return {"id": id_, "module": "http:MakeRequest", "version": 4, "mapper": mapper,
            "metadata": md, "parameters": {"tlsType": "", "authenticationType": "noAuth"}}

def send_text(id_, text, x, y, name):
    body = json.dumps({"messaging_product": "whatsapp", "to": M + "from}}",
                       "type": "text", "text": {"body": text}}, ensure_ascii=False, indent=2)
    return http(id_, "https://graph.facebook.com/v25.0/1197696726762690/messages", "post", body,
                x=x, y=y, name=name)

SORRY = "Sorry, I couldn't quite catch that voice note \U0001F648 Could you type it for me instead?"
next_id = [310]
def on_error(x, y):
    a = next_id[0]; next_id[0] += 2
    return [send_text(a, SORRY, x, y + 250, "Voice note failed - ask to type"),
            {"id": a + 1, "module": "builtin:Ignore", "version": 1, "mapper": None,
             "parameters": {}, "metadata": pos(x + 250, y + 250)}]

Y = 600
ack = send_text(302, "Got your voice note \U0001F3A7 give me a sec...", 300, Y, "Voice note - ack")
ack["filter"] = {"name": "Voice note", "conditions": [[{"a": M + "type}}", "b": "audio", "o": "text:equal"}]]}

media = http(303, "https://graph.facebook.com/v25.0/" + M + "audio.id}}", x=550, y=Y, name="Voice note - get link")
media["onerror"] = on_error(550, Y)
download = http(304, "{{303.data.url}}", parse=False, x=800, y=Y, name="Voice note - download")
download["onerror"] = on_error(800, Y)

tr = json.load(open(TRANSCRIBE_JSON))  # exact module config copied from the helper scenario
tr = copy.deepcopy(tr)
tr["id"] = 305
tr["metadata"] = pos(1050, Y)
tr.pop("filter", None)
tr["mapper"].update({"fileName": "voice.ogg", "fileData": "{{304.data}}", "temperature": "0", "prompt": PROMPT})
tr["onerror"] = on_error(1050, Y)

JS = r"""function pick(a, b) {
  for (const v of [a, b]) {
    if (!v) continue;
    let s = String(v).trim();
    if (s.startsWith('{')) { try { const o = JSON.parse(s); s = String(o.text || '').trim(); } catch (e) { s = ''; } }
    if (s && !s.startsWith('[object')) return s;
  }
  return '';
}
const t = pick(input.transcript, input.transcriptRaw);
if (!t) return { ok: 'no', payload: '', transcript: '' };
const payload = {
  object: 'whatsapp_business_account',
  entry: [{ id: input.entryId, changes: [{ field: 'messages', value: {
    messaging_product: 'whatsapp',
    metadata: { display_phone_number: input.displayPhone, phone_number_id: input.phoneId },
    contacts: [{ profile: { name: input.name }, wa_id: input.waId }],
    messages: [{ from: input.from, id: input.msgId, timestamp: input.ts, type: 'text', text: { body: t }, voice_note: 'yes' }]
  } }] }]
};
return { ok: 'yes', payload: JSON.stringify(payload), transcript: t };"""
V = "{{1.entry[].changes[].value."
code = {"id": 306, "module": "code:ExecuteCode", "version": 1, "parameters": {}, "metadata": pos(1300, Y),
        "mapper": {"input": [
            {"name": "transcript", "value": "{{305.text.text}}"},
            {"name": "transcriptRaw", "value": "{{305.text}}"},
            {"name": "entryId", "value": "{{1.entry[].id}}"},
            {"name": "displayPhone", "value": V + "metadata.display_phone_number}}"},
            {"name": "phoneId", "value": V + "metadata.phone_number_id}}"},
            {"name": "name", "value": V + "contacts[].profile.name}}"},
            {"name": "waId", "value": V + "contacts[].wa_id}}"},
            {"name": "from", "value": M + "from}}"},
            {"name": "msgId", "value": M + "id}}"},
            {"name": "ts", "value": M + "timestamp}}"}],
            "language": "javascript", "inputFormat": "editor", "dependencies": [],
            "codeEditorJavascript": JS}}

repost = http(308, HOOK_URL, "post", "{{306.result.payload}}", headers_auth=False, stop=False,
              x=1800, y=Y - 150, name="Voice note - hand to Lexi as text")
repost["filter"] = {"name": "Got words", "conditions": [[{"a": "{{306.result.ok}}", "b": "yes", "o": "text:equal"}]]}
empty = send_text(309, SORRY, 1800, Y + 150, "Voice note empty - ask to type")
empty["filter"] = {"name": "No words", "conditions": [[{"a": "{{306.result.ok}}", "b": "yes", "o": "text:notequal"}]]}
split = {"id": 307, "module": "builtin:BasicRouter", "version": 1, "mapper": None, "parameters": {},
         "metadata": pos(1550, Y), "routes": [{"flow": [repost]}, {"flow": [empty]}]}

route_a = [ack, media, download, tr, code, split]
route_b = bp["flow"][1:]
front = {"id": 301, "module": "builtin:BasicRouter", "version": 1, "mapper": None, "parameters": {},
         "metadata": pos(150, 2250), "routes": [{"flow": route_a}, {"flow": route_b}]}
bp["flow"] = [bp["flow"][0], front]

out = {"name": bp.get("name", sc["name"]), "flow": bp["flow"], "metadata": bp["metadata"]}
for k in ("scheduling", "interface"):
    if k in bp:
        out[k] = bp[k]
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)

# sanity report without secrets
ids = []
def collect(fl):
    for m in fl:
        ids.append(m["id"])
        for e in m.get("onerror", []) or []:
            ids.append(e["id"])
        for r in m.get("routes", []) or []:
            collect(r["flow"])
collect(out["flow"])
print("modules:", len(ids), "duplicates:", len(ids) - len(set(ids)))
print("new:", sorted(i for i in ids if i >= 301))
