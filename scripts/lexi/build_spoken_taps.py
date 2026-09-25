"""Fix15: answer the day and time lists by voice note or typing, not only by tapping.

While a client's BookingSession row has a service but no day (or a day but no time), a
text message (typed, or a transcribed voice note) is matched to a day or time.
  340 code:  match the text; build either a synthetic tap ("day_x"/"time_x" list_reply) or,
             if nothing matches, a pass-through copy of the message marked lexi_passthrough
  341 HTTP:  re-post that payload to Lexi's own webhook
A synthetic tap runs the normal Day Selected / Time Selected branches (calendar checks
included). A pass-through goes to Lexi's AI conversation exactly as before, because the
AI route (starting at module 5) now skips only the messages route 340 takes over.

Usage: build_spoken_taps.py <blueprint json> <out file> <lexi webhook url>
"""
import json, sys

SRC, OUT, HOOK_URL = sys.argv[1:4]
M = "{{1.entry[].changes[].value.messages[]."
V = "{{1.entry[].changes[].value."

t = open(SRC).read()
d = json.loads(t[t.index("{"):])
sc = d.get("scenario", d)
bp = sc.get("blueprint", sc)
if isinstance(bp, str):
    bp = json.loads(bp)

mods = {}
def walk(fl):
    for m in fl:
        mods[m["id"]] = m
        for r in m.get("routes", []) or []:
            walk(r.get("flow", []))
walk(bp["flow"])
assert not any(340 <= i < 350 for i in mods), "ids 340-349 already used"
r40 = mods[40]["routes"]
assert r40[3]["flow"][0]["id"] == 5 and not r40[3]["flow"][0].get("filter"), "AI route changed shape"

def c(a, o, b=None):
    x = {"a": a, "o": o}
    if b is not None:
        x["b"] = b
    return x

TYPE, S0, S1, S2, S3 = M + "type}}", "{{86.`__IMTLENGTH__`}}", "{{86.`1`}}", "{{86.`2`}}", "{{86.`3`}}"
PEND, INTENT, PASS = "{{160.`__IMTLENGTH__`}}", "{{152.isIntent}}", M + "lexi_passthrough}}"
base = [c(TYPE, "text:equal", "text"), c(S0, "number:greater", "0"), c(PEND, "number:equal", "0"),
        c(INTENT, "text:notequal", "yes"), c(S1, "exist"), c(PASS, "notexist")]
take = {"name": "Spoken day or time", "conditions": [base + [c(S2, "notexist")], base + [c(S3, "notexist")]]}
skip = {"name": "Not a spoken day/time", "conditions": [
    [c(TYPE, "text:notequal", "text")], [c(S0, "number:equal", "0")], [c(PEND, "number:greater", "0")],
    [c(INTENT, "text:equal", "yes")], [c(S1, "notexist")], [c(PASS, "exist")],
    [c(S2, "exist"), c(S3, "exist")]]}

JS = r"""const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const DAYS = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
const AF = { sondag: 0, maandag: 1, dinsdag: 2, woensdag: 3, donderdag: 4, vrydag: 5, saterdag: 6 };
const clean = s => String(s || '').trim();
const txt = ' ' + clean(input.text).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[’`]/g, "'").replace(/[^a-z0-9:' ]+/g, ' ').replace(/\s+/g, ' ') + ' ';
const now = new Date(Date.now() + 2 * 3600 * 1000);            // SAST, read with getUTC*
const fmt = d => DAYS[d.getUTCDay()] + ' ' + d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()];

// Same five working days Lexi's day list shows (no Sundays or Mondays; today only before 15:00)
function workingDays() {
  const out = []; const cur = new Date(now);
  if (cur.getUTCDay() !== 0 && cur.getUTCDay() !== 1 && cur.getUTCHours() < 15) out.push(new Date(cur));
  cur.setUTCDate(cur.getUTCDate() + 1);
  while (out.length < 5) { if (cur.getUTCDay() !== 0 && cur.getUTCDay() !== 1) out.push(new Date(cur)); cur.setUTCDate(cur.getUTCDate() + 1); }
  return out;
}
function matchDay() {
  const list = workingDays(); const hits = new Set();
  const tomorrow = new Date(now); tomorrow.setUTCDate(tomorrow.getUTCDate() + 1);
  list.forEach((d, i) => {
    const wd = d.getUTCDay();
    if (txt.includes(' ' + DAYS[wd].toLowerCase()) || txt.includes(' ' + DAYS[wd].slice(0, 3).toLowerCase() + ' ')) hits.add(i);
    for (const [w, n] of Object.entries(AF)) if (n === wd && txt.includes(' ' + w)) hits.add(i);
    const dn = d.getUTCDate();
    if (new RegExp(' ' + dn + '(st|nd|rd|th)? ').test(txt) || new RegExp(' ' + dn + ' ' + MONTHS[d.getUTCMonth()].toLowerCase().slice(0, 3)).test(txt)) hits.add(i);
    if (/ (today|vandag) /.test(txt) && d.getUTCDate() === now.getUTCDate() && d.getUTCMonth() === now.getUTCMonth()) hits.add(i);
    if (/ (tomorrow|tmrw|more|môre) /.test(txt) && d.getUTCDate() === tomorrow.getUTCDate() && d.getUTCMonth() === tomorrow.getUTCMonth()) hits.add(i);
  });
  if (hits.size !== 1) return null;
  const i = [...hits][0];
  return { id: 'day_' + (i + 1), title: fmt(list[i]) };
}
const WORDS = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12,
  een: 1, twee: 2, drie: 3, vier: 4, vyf: 5, ses: 6, sewe: 7, agt: 8, nege: 9, tien: 10, elf: 11, twaalf: 12 };
function matchTime(day) {
  let t = txt.replace(/\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|een|twee|drie|vier|vyf|ses|sewe|agt|nege|tien|elf|twaalf)\b/g, w => WORDS[w]);
  t = t.replace(/\bnoon\b|\bmidday\b|\bmiddag\b/g, '12:00 ');
  let h = null, m = 0, ap = '';
  let x;
  if ((x = t.match(/half past (\d{1,2})/))) { h = +x[1]; m = 30; }
  else if ((x = t.match(/half (\d{1,2})/))) { h = +x[1] - 1; m = 30; }          // Afrikaans "half tien" = 9:30
  else if ((x = t.match(/(\d{1,2})[:h.](\d{2})/))) { h = +x[1]; m = +x[2]; }
  else if ((x = t.match(/(?:^| )(\d{1,2}) ?(am|pm|a m|p m|o'?clock|uur)?(?= )/)) && (x[2] || t.trim().split(' ').length <= 5)) { h = +x[1]; }
  if (h === null) return null;
  const apm = t.match(/(\d)\s?(am|a m)\b|\bmorning\b|\boggend\b/) ? 'AM' : t.match(/(\d)\s?(pm|p m)\b|\bafternoon\b|\bmiddag\b/) ? 'PM' : '';
  if (h > 12) { ap = 'PM'; h -= 12; } else if (apm) ap = apm; else ap = (h >= 8 && h <= 11) ? 'AM' : 'PM';
  if (h === 0 || h > 12 || (m !== 0 && m !== 30)) return null;
  const slot = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ' ' + ap;
  const sat = String(day || '').toLowerCase().includes('saturday');
  const slots = sat ? ['08:00 AM','08:30 AM','09:00 AM','09:30 AM','10:00 AM','10:30 AM','11:00 AM','11:30 AM','12:00 PM','12:30 PM','01:00 PM','01:30 PM','02:00 PM','02:30 PM','03:00 PM','03:30 PM','04:00 PM','04:30 PM']
                    : ['08:00 AM','09:00 AM','10:00 AM','11:00 AM','12:00 PM','01:00 PM','02:00 PM','03:00 PM','04:00 PM'];
  if (!slots.includes(slot)) return null;
  return { id: 'time_' + (slots.indexOf(slot) + 1), title: slot };
}
const stage = clean(input.day) ? 'time' : 'day';
const hit = stage === 'day' ? matchDay() : matchTime(input.day);
const msg = { from: input.from, id: input.msgId, timestamp: input.ts };
if (hit) { msg.type = 'interactive'; msg.interactive = { type: 'list_reply', list_reply: hit }; msg.spoken_tap = 'yes'; }
else { msg.type = 'text'; msg.text = { body: clean(input.text) }; msg.lexi_passthrough = 'yes'; }
const payload = { object: 'whatsapp_business_account', entry: [{ id: input.entryId, changes: [{ field: 'messages', value: {
  messaging_product: 'whatsapp',
  metadata: { display_phone_number: input.displayPhone, phone_number_id: input.phoneId },
  contacts: [{ profile: { name: input.name }, wa_id: input.waId }],
  messages: [msg] } }] }] };
return { stage, matched: hit ? 'yes' : 'no', title: hit ? hit.title : '', payload: JSON.stringify(payload) };"""

code = {"id": 340, "module": "code:ExecuteCode", "version": 1, "parameters": {}, "filter": take,
        "metadata": {"designer": {"x": 3800, "y": 3400, "name": "Match spoken day or time"}},
        "mapper": {"input": [
            {"name": "text", "value": M + "text.body}}"},
            {"name": "day", "value": S2},
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
repost = {"id": 341, "module": "http:MakeRequest", "version": 4,
          "metadata": {"designer": {"x": 4050, "y": 3400, "name": "Tap it for the client (or pass to AI)"}},
          "parameters": {"tlsType": "", "authenticationType": "noAuth"},
          "mapper": {"url": HOOK_URL, "method": "post",
                     "headers": [{"name": "Content-Type", "value": "application/json"}],
                     "contentType": "json", "inputMethod": "jsonString",
                     "jsonStringBodyContent": "{{340.result.payload}}", "shareCookies": False,
                     "parseResponse": True, "allowRedirects": True, "stopOnHttpError": False,
                     "requestCompressedContent": True}}

r40[3]["flow"][0]["filter"] = skip
r40.insert(0, {"flow": [code, repost]})

out = {"name": bp.get("name", sc.get("name")), "flow": bp["flow"], "metadata": bp["metadata"]}
for k in ("scheduling", "interface"):
    if k in bp:
        out[k] = bp[k]
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
open(OUT + ".js", "w").write(JS)   # for local testing only

ids = []
def collect(fl):
    for m in fl:
        ids.append(m["id"])
        for e in m.get("onerror", []) or []:
            ids.append(e["id"])
        for r in m.get("routes", []) or []:
            collect(r["flow"])
collect(out["flow"])
print("modules:", len(ids), "duplicates:", len(ids) - len(set(ids)), "new:", sorted(i for i in ids if 340 <= i < 350))
