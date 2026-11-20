// Several dates, step 3: check each date against Nita's calendar (same rules as C.js)
// and build the "here's what I can book" message.
const DAY_CAPACITY = Number(input.day_capacity || 2);
const OFF_BLOCKS_DAY = String(input.off_blocks_day || "no") === "yes";
const POINTS = { svc_basic: 1, svc_deep: 2, svc_moveout: 2 };
const LABEL = { svc_basic: "Basic Clean", svc_deep: "Deep Clean", svc_moveout: "Move Out / In" };
const heavy = t => /deep|move/i.test(t);
const sastDay = iso => new Date(Date.parse(iso) + 2 * 3600000).toISOString().slice(0, 10);
const isOff = t => /^(nita\s+)?off\b/i.test(t);

let raw = input.events_json;
if (typeof raw === "string") { try { raw = JSON.parse(raw || "{}"); } catch (e) { raw = {}; } }
const items = Array.isArray(raw) ? raw : ((raw && (raw.items || (raw.body && raw.body.items))) || []);
let lines = [];
try { lines = JSON.parse(String(input.lines_json || "[]")); } catch (e) { lines = []; }

// points already used on each day, and days Nita marked Off
const used = {}, off = {};
const add = (day, p) => { used[day] = (used[day] || 0) + p; };
items.filter(e => e && e.status !== "cancelled" && e.start && e.end && !/^❌/.test(String(e.summary || ""))).forEach(e => {
  const title = String(e.summary || "").trim();
  if (e.start.date) {
    const s = String(e.start.date).slice(0, 10), en = String(e.end.date).slice(0, 10);
    for (let t = Date.parse(s + "T00:00:00Z"); t < Date.parse(en + "T00:00:00Z"); t += 86400000) {
      const day = new Date(t).toISOString().slice(0, 10);
      if (isOff(title)) { off[day] = true; continue; }
      title.split(/&|,|\band\b/i).map(x => x.trim()).filter(Boolean).forEach(j => add(day, heavy(j) ? 2 : 1));
    }
  } else if (e.start.dateTime) {
    const day = sastDay(e.start.dateTime);
    if (isOff(title)) { off[day] = true; return; }
    const svc = e.extendedProperties && e.extendedProperties.private && e.extendedProperties.private.service;
    add(day, svc ? (POINTS[svc] || 1) : (heavy(title) ? 2 : 1));
  }
});

const where = l => [l.building, l.unit ? "Unit " + l.unit : ""].filter(Boolean).join(", ") || "your usual place";
const okLines = [], msg = [];
lines.forEach(l => {
  const p = POINTS[l.service] || 1;
  const full = (off[l.day] && OFF_BLOCKS_DAY) || (used[l.day] || 0) + p > DAY_CAPACITY;
  if (full) { msg.push("❌ " + l.label + " · " + where(l) + " (fully booked)"); return; }
  add(l.day, p);   // two of her own dates on one day count against each other too
  okLines.push(l);
  msg.push("✅ " + l.label + " · " + LABEL[l.service] + " · " + where(l));
});

const extra = String(input.problems_text || "");
let text = "Here's what I can book for you:\n\n" + msg.join("\n") + (extra ? "\n" + extra : "");
if (okLines.length) {
  text += "\n\n" + (okLines.length < lines.length || extra ? "I'll book the ✅ dates. For the others, send *hi* afterwards to pick another day.\n\n" : "") +
    "What time should the team arrive? (Same time for all " + okLines.length + (okLines.length === 1 ? " date" : " dates") + ")";
} else {
  text += "\n\nSorry, none of those dates are free 😕 Send me different dates, or *menu* to start again.";
}
if (text.length > 1000) text = text.slice(0, 990) + "…";
return { ok_count: okLines.length, ok_lines_json: JSON.stringify(okLines), text_json: JSON.stringify(text) };
