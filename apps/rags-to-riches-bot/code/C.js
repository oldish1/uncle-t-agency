// Capacity count: how many jobs are already on during the new job's hours.
// Reads timed events AND Nita's all-day entries ("615", "2910", "117 & 210", "Off").
const CAPACITY = Number(input.capacity || 2);
const OFF_BLOCKS_DAY = String(input.off_blocks_day || "yes") !== "no"; // waiting on Nita: does "Off" mean nobody works?
let raw = input.events_json;
if (typeof raw === "string") {
  try { raw = JSON.parse(raw || "{}"); } catch (e) { return { ok: false, error: "events_not_json", slot_full: true }; }
}
const items = Array.isArray(raw) ? raw : ((raw && (raw.items || (raw.body && raw.body.items))) || []);
const newStart = Date.parse(input.start_iso);
const newEnd = Date.parse(input.end_iso);
if (isNaN(newStart) || isNaN(newEnd)) return { ok: false, error: "bad_times", slot_full: true };
const day = String(input.start_iso).slice(0, 10);
const live = items.filter(e => e && e.status !== "cancelled" && e.start && e.end);

// All-day entries that cover this day
let allDayJobs = 0, dayOff = false;
live.filter(e => e.start.date && e.start.date <= day && e.end.date > day).forEach(e => {
  const title = String(e.summary || "").trim();
  if (/^(nita\s+)?off\b/i.test(title)) { dayOff = true; return; }
  const jobs = title.split(/&|,|\band\b/i).map(s => s.trim()).filter(Boolean).length;
  allDayJobs += Math.max(1, jobs);
});

// Timed events: the most running at any one moment inside the new job's window
const overlaps = live
  .filter(e => e.start.dateTime && e.end.dateTime)
  .map(e => [Math.max(Date.parse(e.start.dateTime), newStart), Math.min(Date.parse(e.end.dateTime), newEnd)])
  .filter(([s, e]) => e > s);
const points = [];
overlaps.forEach(([s, e]) => { points.push([s, 1]); points.push([e, -1]); });
points.sort((a, b) => a[0] - b[0] || a[1] - b[1]); // an end and a start at the same minute don't clash
let running = 0, peak = 0;
points.forEach(([, step]) => { running += step; if (running > peak) peak = running; });

const busy = peak + allDayJobs;
const blocked = dayOff && OFF_BLOCKS_DAY;
return {
  ok: true,
  error: "",
  slot_full: blocked || busy >= CAPACITY,
  day_off: blocked,
  peak_busy: busy,
  all_day_jobs: allDayJobs,
  places_left: blocked ? 0 : Math.max(0, CAPACITY - busy),
  overlapping_events: overlaps.length
};
