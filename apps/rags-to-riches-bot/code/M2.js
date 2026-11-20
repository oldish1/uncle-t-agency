// Several dates, step 2: check Claude's reading of the list and tidy each line.
const SAST = 2, MS = 86400000;
const MAX_DAYS = Number(input.max_days || 62);   // about 2 months ahead
const MAX_LINES = 10;                            // one booking per line, 10 at a time
const CUTOFF = String(input.same_day_cutoff || "07:00");
const SVC = { basic: "svc_basic", deep: "svc_deep", moveout: "svc_moveout" };
const DAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const clean = v => String(v == null ? "" : v).replace(/\s+/g, " ").trim().slice(0, 80);
const fail = (why, text) => ({ ok: false, error: why, intent: "unclear", has_lines: false, lines_json: "[]",
  client_name: "", min_day: "", max_day: "", reprompt_json: JSON.stringify(text) });
const ASK = "Sorry, I couldn't read the dates 😕 Please send them one per line, e.g.\n_26 Oct 2910 Bree_\n_30 Oct 409_";

let resp = input.claude_body;
if (typeof resp === "string") { try { resp = JSON.parse(resp); } catch (e) { return fail("body_not_json", ASK); } }
if (!resp || resp.type === "error") return fail("api_error", ASK);
const block = (resp.content || []).find(b => b && b.type === "text");
if (!block || !block.text) return fail("no_text", ASK);
let t = block.text.trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "");
let out;
try { out = JSON.parse(t.slice(t.indexOf("{"), t.lastIndexOf("}") + 1)); } catch (e) { return fail("bad_json", ASK); }

const intent = ["details", "restart", "cancel", "question", "unclear"].includes(out.intent) ? out.intent : "unclear";
const now = input.now_iso ? new Date(input.now_iso) : new Date();
const sast = new Date(now.getTime() + SAST * 3600000);
const todayIso = sast.toISOString().slice(0, 10);
const hhmm = sast.toISOString().slice(11, 16);
const first = Date.parse(todayIso + "T00:00:00Z") + (hhmm < CUTOFF ? 0 : MS);
const last = Date.parse(todayIso + "T00:00:00Z") + MAX_DAYS * MS;
const label = iso => { const d = new Date(iso + "T12:00:00Z"); return DAY[d.getUTCDay()] + " " + d.getUTCDate() + " " + MON[d.getUTCMonth()]; };

const savedUnit = clean(input.saved_unit), savedBuilding = clean(input.saved_building), savedCode = clean(input.saved_code);
const lines = [], problems = [];
(Array.isArray(out.bookings) ? out.bookings : []).forEach(b => {
  const raw = clean(b.raw) || clean(b.date);
  const iso = String(b.date || "");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(iso) || isNaN(Date.parse(iso))) { problems.push("❓ " + raw + " (couldn't read the date)"); return; }
  const t0 = Date.parse(iso + "T00:00:00Z");
  if (t0 < first) { problems.push("❓ " + label(iso) + " (too soon or already past)"); return; }
  if (t0 > last) { problems.push("❓ " + label(iso) + " (more than 2 months ahead, please message Nita)"); return; }
  if (lines.length >= MAX_LINES) { problems.push("❓ " + label(iso) + " (10 dates at a time, please send the rest after)"); return; }
  let unit = clean(b.unit_number), building = clean(b.building_name), code = clean(b.access_code);
  if (!unit && !building) { unit = savedUnit; building = savedBuilding; }
  // "Bree" on its own = her usual Bree apartment
  else if (!unit && building && savedUnit && savedBuilding &&
           (savedBuilding.toLowerCase().includes(building.toLowerCase()) || building.toLowerCase().includes(savedBuilding.toLowerCase()))) { unit = savedUnit; building = savedBuilding; }
  if (!code && unit && unit === savedUnit) code = savedCode;
  lines.push({ day: iso, label: label(iso), service: SVC[b.service] || String(input.default_service || "svc_basic"),
    unit: unit, building: building, code: code, raw: raw });
});
lines.sort((a, b) => a.day < b.day ? -1 : a.day > b.day ? 1 : 0);

const name = clean(out.client_name) || clean(input.saved_name);
let reprompt = "";
if (intent === "details" || intent === "unclear" || intent === "question") {
  if (!lines.length) reprompt = (problems.length ? problems.join("\n") + "\n\n" : "") + ASK;
  else if (!name) reprompt = "Thanks! What name should Nita put these bookings under? Please send the list again with your name on the first line 🙂";
}
return {
  ok: true, error: "", intent: intent,
  has_lines: lines.length > 0 && !!name,
  lines_json: JSON.stringify(lines),
  problems_text: problems.join("\n"),
  client_name: name,
  min_day: lines.length ? lines[0].day + "T00:00:00+02:00" : "",
  max_day: lines.length ? lines[lines.length - 1].day + "T23:59:59+02:00" : "",
  reprompt_json: JSON.stringify(reprompt)
};
