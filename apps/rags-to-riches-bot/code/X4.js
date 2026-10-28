// Change / cancel, step 3b: new day + time chosen. Re-check that day (not counting this booking) and move it.
const SLOTS = { rsl_0800: "08:00", rsl_1200: "12:00", rsl_1500: "15:00" };
const HOURS = { svc_basic: 3, svc_deep: 3.5, svc_moveout: 4 };
const DUR = { svc_basic: "3+ hrs", svc_deep: "about 3.5 hrs", svc_moveout: "about 4 hrs" };
const POINTS = { svc_basic: 1, svc_deep: 2, svc_moveout: 2 };
const DAY_CAPACITY = Number(input.day_capacity || 2);
const FEE = String(input.late_fee || "R150");
const DAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const pad = n => String(n).padStart(2, "0");
const heavy = t => /deep|move/i.test(t);
const isOff = t => /^(nita\s+)?off\b/i.test(t);
const bad = t => ({ ok: false, full: false, event_id: "", patch_json: "{}", text_json: JSON.stringify(t) });
let b = {};
try { b = JSON.parse(String(input.booking_json || "{}")); } catch (e) { b = {}; }
const day = String(input.day_id || "").replace(/^rs_day_/, "");
const slot = SLOTS[String(input.slot_id || "")];
if (!b.id || !/^\d{4}-\d{2}-\d{2}$/.test(day) || !slot) return bad("Sorry, that option has expired. Send *change* to try again.");
const svc = HOURS[b.service] ? b.service : "svc_basic";
const startIso = day + "T" + slot + ":00+02:00";
const now = input.now_iso ? new Date(input.now_iso) : new Date();
if (Date.parse(startIso) < now.getTime() + 3600000) return bad("Sorry, that time has already passed or is too soon. Send *change* to pick another time.");
let raw = input.events_json;
if (typeof raw === "string") { try { raw = JSON.parse(raw || "{}"); } catch (e) { raw = {}; } }
const items = Array.isArray(raw) ? raw : ((raw && (raw.items || (raw.body && raw.body.items))) || []);
let used = 0;
items.filter(e => e && e.id !== b.id && e.status !== "cancelled" && e.start && e.end && !/^❌/.test(String(e.summary || ""))).forEach(e => {
  const title = String(e.summary || "").trim();
  if (isOff(title)) return;
  if (e.start.date) {
    if (!(String(e.start.date).slice(0, 10) <= day && String(e.end.date).slice(0, 10) > day)) return;
    title.split(/&|,|\band\b/i).map(x => x.trim()).filter(Boolean).forEach(j => { used += heavy(j) ? 2 : 1; });
  } else if (e.start.dateTime) {
    if (new Date(Date.parse(e.start.dateTime) + 2 * 3600000).toISOString().slice(0, 10) !== day) return;
    const s = e.extendedProperties && e.extendedProperties.private && e.extendedProperties.private.service;
    used += s ? (POINTS[s] || 1) : (heavy(title) ? 2 : 1);
  }
});
const d = new Date(day + "T12:00:00Z");
const when = DAY[d.getUTCDay()] + " " + d.getUTCDate() + " " + MON[d.getUTCMonth()] + ", " + slot;
if (used + (POINTS[svc] || 1) > DAY_CAPACITY)
  return { ok: false, full: true, event_id: "", patch_json: "{}", text_json: JSON.stringify("Sorry, *" + DAY[d.getUTCDay()] + " " + d.getUTCDate() + " " + MON[d.getUTCMonth()] + "* is fully booked 😕 Send *change* to pick another day. Your booking for " + b.when + " stays as it is.") };
const [h, m] = slot.split(":").map(Number);
const endMin = h * 60 + m + Math.round(HOURS[svc] * 60);
const endIso = day + "T" + pad(Math.floor(endMin / 60)) + ":" + pad(endMin % 60) + ":00+02:00";
const stamp = new Date(now.getTime() + 2 * 3600000).toISOString().slice(0, 16).replace("T", " ");
const patch = {
  start: { dateTime: startIso, timeZone: "Africa/Johannesburg" },
  end: { dateTime: endIso, timeZone: "Africa/Johannesburg" },
  description: "MOVED by client via Luna on " + stamp + ": was " + b.when + "." + (b.late ? "\nLate change (less than 24 hours before): " + FEE + " fee applies." : "") + "\n\n" + String(b.description || "").replace(/^MOVED by client[^\n]*\n(Late change[^\n]*\n)?\n?/, "")
};
if (b.late) patch.summary = String(b.summary || "").replace(/ · R\d+ LATE CHANGE$/, "") + " · " + FEE + " LATE CHANGE";
let text = "✅ Done! Your booking is moved to *" + when + "* (" + DUR[svc] + ").\n\n(It was " + b.when + ".)";
if (b.late) text += "\n\nBecause the change was less than 24 hours before the clean, the *" + FEE + "* fee applies. Ms Adams will send you the details.";
return { ok: true, full: false, event_id: b.id, patch_json: JSON.stringify(patch), text_json: JSON.stringify(text), new_when: when };
