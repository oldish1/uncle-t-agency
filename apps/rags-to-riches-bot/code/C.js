// Day capacity check, the way Nita's team works (her answers, 28 Sept):
// a day holds 2 "points". Basic clean = 1 point, Deep clean = 2 (the whole day), Move Out = 2 (assumed, heavy like Deep).
// Reads her all-day entries ("615", "2910", "117 & 210", "603 deep") and bot bookings.
// "Off" means only Nita is off; staff still clean, so it doesn't block the day.
const DAY_CAPACITY = Number(input.day_capacity || 2);
const OFF_BLOCKS_DAY = String(input.off_blocks_day || "no") === "yes";
const POINTS = { svc_basic: 1, svc_deep: 2, svc_moveout: 2 };
const heavy = t => /deep|move/i.test(t);
let raw = input.events_json;
if (typeof raw === "string") {
  try { raw = JSON.parse(raw || "{}"); } catch (e) { return { ok: false, error: "events_not_json", slot_full: true }; }
}
const items = Array.isArray(raw) ? raw : ((raw && (raw.items || (raw.body && raw.body.items))) || []);
const day = String(input.start_iso || "").slice(0, 10);
if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) return { ok: false, error: "bad_times", slot_full: true };
const newPoints = POINTS[String(input.service_id || "")] || 1;
const sastDay = iso => new Date(Date.parse(iso) + 2 * 3600000).toISOString().slice(0, 10);

let used = 0, jobs = 0, dayOff = false;
items.filter(e => e && e.status !== "cancelled" && e.start && e.end).forEach(e => {
  const title = String(e.summary || "").trim();
  if (e.start.date) {
    if (!(e.start.date <= day && e.end.date > day)) return;
    if (/^(nita\s+)?off\b/i.test(title)) { dayOff = true; return; }
    title.split(/&|,|\band\b/i).map(s => s.trim()).filter(Boolean).forEach(j => { jobs++; used += heavy(j) ? 2 : 1; });
  } else if (e.start.dateTime) {
    if (sastDay(e.start.dateTime) !== day) return;
    const svc = e.extendedProperties && e.extendedProperties.private && e.extendedProperties.private.service;
    jobs++; used += svc ? (POINTS[svc] || 1) : (heavy(title) ? 2 : 1);
  }
});

const blocked = dayOff && OFF_BLOCKS_DAY;
return {
  ok: true,
  error: "",
  slot_full: blocked || used + newPoints > DAY_CAPACITY,
  day_off: dayOff,
  points_used: used,
  points_needed: newPoints,
  jobs_that_day: jobs,
  places_left: Math.max(0, DAY_CAPACITY - used)
};
