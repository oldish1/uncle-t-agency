"""Fix13: skip the service menu when a client's first message already names a service.

The Greeting Interceptor route (module 57 alone) becomes:
  320 code: detect a service in the text (runs under 57's original filter)
  321 router
     A (one service found): 322 welcome + rules + "Lovely, a <service>!", then
                            323 re-post a synthetic "tapped <service>" message to Lexi's
                            own webhook, so the normal Service Selected branch runs.
     B (none or several):   57, the normal welcome + service menu (filter moved to 320)
Also fixes the hairdresser emoji in 57's header (missing zero-width joiner).

Usage: build_service_shortcut.py <scenario json> <out file> <lexi webhook url>
The WhatsApp key is copied from module 57 inside this script and never printed.
"""
import copy, json, sys

SRC, OUT, HOOK_URL = sys.argv[1], sys.argv[2], sys.argv[3]
M = "{{1.entry[].changes[].value.messages[]."
V = "{{1.entry[].changes[].value."
HAIRDRESSER = "\U0001F487‍♀️"

t = open(SRC).read()
d = json.loads(t[t.index("{"):])
sc = d.get("scenario", d)
bp = sc["blueprint"]
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
assert 301 in mods, "fix12 (voice notes) must already be live"
assert not any(320 <= i < 330 for i in mods), "ids 320-329 already used"
g = mods[57]
fl, idx = holder[57]
assert len(fl) == 1 and g["filter"]["name"] == "Greeting Interceptor", "greeting route changed shape"
auth = [h for h in g["mapper"]["headers"] if h["name"] == "Authorization"][0]["value"]

# 1. emoji fix in the existing welcome
body = g["mapper"]["jsonStringBodyContent"]
g["mapper"]["jsonStringBodyContent"] = body.replace("\U0001F487♀️", HAIRDRESSER).replace("\U0001F487♀", HAIRDRESSER)

# 2. service detection + synthetic tap payload
SERVICES = {
    "service_1": "Hair Colour & Highlights", "service_2": "Precision Cut",
    "service_3": "Brazilian & Keratin", "service_4": "Botox & Glowtox",
    "service_5": "Nanoplastia", "service_6": "Wash and Blowdry",
    "service_7": "Basin Treatment", "service_8": "Full Color",
    "service_9": "Root Touch Up", "service_10": "Trim",
}
JS = r"""const S = %s;
const txt = ' ' + String(input.text || '').toLowerCase().replace(/[^a-z0-9&' ]+/g, ' ') + ' ';
const has = re => re.test(txt);
const found = new Set();
if (has(/root/)) found.add('service_9');
if (has(/highlight/)) found.add('service_1');
if (!found.has('service_9') && !found.has('service_1') && has(/colou?r|\bdye\b|\btint\b/)) found.add('service_8');
if (has(/\btrim\b/)) found.add('service_10');
else if (has(/precision|hair ?cut|\bcut\b/)) found.add('service_2');
if (has(/brazilian|keratin/)) found.add('service_3');
if (has(/botox|glow ?tox/)) found.add('service_4');
if (has(/nano/)) found.add('service_5');
if (!found.has('service_3') && has(/\bwash|blow ?dry|blow ?out|blowdr/)) found.add('service_6');
if (has(/basin/) || (has(/treatment/) && !found.has('service_3') && !found.has('service_4') && !found.has('service_5'))) found.add('service_7');
if (found.size !== 1) return { found: 'no', id: '', title: '', payload: '' };
const id = [...found][0];
const title = S[id];
const payload = {
  object: 'whatsapp_business_account',
  entry: [{ id: input.entryId, changes: [{ field: 'messages', value: {
    messaging_product: 'whatsapp',
    metadata: { display_phone_number: input.displayPhone, phone_number_id: input.phoneId },
    contacts: [{ profile: { name: input.name }, wa_id: input.waId }],
    messages: [{ from: input.from, id: input.msgId, timestamp: input.ts, type: 'interactive',
      interactive: { type: 'list_reply', list_reply: { id: id, title: title } }, service_shortcut: 'yes' }]
  } }] }]
};
return { found: 'yes', id: id, title: title, payload: JSON.stringify(payload) };""" % json.dumps(SERVICES)

def pos(x, y):
    return {"designer": {"x": x, "y": y}}
gx, gy = g["metadata"]["designer"]["x"], g["metadata"]["designer"]["y"]

detect = {"id": 320, "module": "code:ExecuteCode", "version": 1, "parameters": {},
          "filter": copy.deepcopy(g["filter"]), "metadata": pos(gx, gy),
          "mapper": {"input": [
              {"name": "text", "value": M + "text.body}}"},
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
detect["filter"]["name"] = "Greeting Interceptor"

def http(id_, url, body, headers_auth, stop, x, y, name, filt):
    headers = [{"name": "Authorization", "value": auth}] if headers_auth else []
    headers.append({"name": "Content-Type", "value": "application/json"})
    return {"id": id_, "module": "http:MakeRequest", "version": 4, "filter": filt,
            "metadata": {"designer": {"x": x, "y": y, "name": name}},
            "parameters": {"tlsType": "", "authenticationType": "noAuth"},
            "mapper": {"url": url, "method": "post", "headers": headers, "contentType": "json",
                       "inputMethod": "jsonString", "jsonStringBodyContent": body, "shareCookies": False,
                       "parseResponse": True, "allowRedirects": True, "stopOnHttpError": stop,
                       "requestCompressedContent": True}}

WELCOME = ("Hi! I'm Lexi from Chales Hair Boutique " + HAIRDRESSER + " Lovely, a {{320.result.title}}! "
           "Let me show you the days Chanté has open.\n\n"
           "Chales Hair Boutique Salon Rules:\n- Appointments only — no walk-ins\n"
           "- Inform us 1 hour before if you'll be running late\n"
           "- No extra guests unless they're also getting a service\n- Strictly no children allowed\n"
           "- Space is limited — please wait at reception on arrival")
welcome_body = json.dumps({"messaging_product": "whatsapp", "to": M + "from}}", "type": "text",
                           "text": {"body": WELCOME}}, ensure_ascii=False, indent=2)
yes = {"name": "Service named", "conditions": [[{"a": "{{320.result.found}}", "b": "yes", "o": "text:equal"}]]}
no = {"name": "No single service", "conditions": [[{"a": "{{320.result.found}}", "b": "yes", "o": "text:notequal"}]]}
welcome = http(322, "https://graph.facebook.com/v25.0/1197696726762690/messages", welcome_body, True, True,
               gx + 500, gy - 150, "Welcome + service named", yes)
tap = http(323, HOOK_URL, "{{320.result.payload}}", False, False, gx + 750, gy - 150,
           "Tap that service for the client", None)
g["filter"] = no
g["metadata"]["designer"]["x"] = gx + 500
g["metadata"]["designer"]["y"] = gy + 150
split = {"id": 321, "module": "builtin:BasicRouter", "version": 1, "mapper": None, "parameters": {},
         "metadata": pos(gx + 250, gy), "routes": [{"flow": [welcome, tap]}, {"flow": [g]}]}
fl[idx:idx + 1] = [detect, split]

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
print("modules:", len(ids), "duplicates:", len(ids) - len(set(ids)), "new:", sorted(i for i in ids if 320 <= i < 330))
print("emoji fixed:", HAIRDRESSER in g["mapper"]["jsonStringBodyContent"])
