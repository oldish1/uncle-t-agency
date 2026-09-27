// ===== CONFIG =====
const CAPACITY = 2;   // v1 assumption: max jobs running at the same moment
// ==================
let raw = input.events_json;
if (typeof raw === "string") {
  try { raw = JSON.parse(raw || "{}"); } catch (e) { return { ok: false, error: "events_not_json", slot_full: true }; }
}
// Accepts the API body ({items:[...]}), a body wrapper ({body:{items}}) or a bare array
const items = Array.isArray(raw) ? raw : ((raw && (raw.items || (raw.body && raw.body.items))) || []);

const newStart = Date.parse(input.start_iso);
const newEnd = Date.parse(input.end_iso);
if (isNaN(newStart) || isNaN(newEnd)) return { ok: false, error: "bad_times", slot_full: true };

// Timed, non-cancelled events only. All-day events are ignored in v1.
const overlaps = items
  .filter(e => e && e.status !== "cancelled" && e.start && e.start.dateTime && e.end && e.end.dateTime)
  .map(e => [Math.max(Date.parse(e.start.dateTime), newStart), Math.min(Date.parse(e.end.dateTime), newEnd)])
  .filter(([s, e]) => e > s);

// Sweep: the most jobs already running at any single moment inside the new job's window
const points = [];
overlaps.forEach(([s, e]) => { points.push([s, 1]); points.push([e, -1]); });
points.sort((a, b) => a[0] - b[0] || a[1] - b[1]); // an end and a start at the same minute don't clash
let running = 0, peak = 0;
points.forEach(([, step]) => { running += step; if (running > peak) peak = running; });

return {
  ok: true,
  error: "",
  slot_full: peak >= CAPACITY,
  peak_busy: peak,
  places_left: Math.max(0, CAPACITY - peak),
  overlapping_events: overlaps.length
};
