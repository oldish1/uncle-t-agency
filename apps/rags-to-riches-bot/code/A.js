// Day picker. Settings come from the "Inbound + config" step.
const SAST = 2;                                   // Cape Town, no daylight saving
const WINDOW_DAYS = Number(input.window_days || 7); // Nita: next week only
const WORKING_DAYS = [0, 1, 2, 3, 4, 5, 6];       // Nita: every day; Saturdays and Sundays +R50
const CUTOFF = String(input.same_day_cutoff || "07:00"); // same-day bookings allowed before this time
const HOLIDAYS = String(input.holidays || "").split(",").map(s => s.trim()).filter(Boolean);
const DAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const MS = 86400000;

const now = input.now_iso ? new Date(input.now_iso) : new Date();
const sast = new Date(now.getTime() + SAST * 3600000);
const today = Date.UTC(sast.getUTCFullYear(), sast.getUTCMonth(), sast.getUTCDate());
const nowHHMM = String(sast.getUTCHours()).padStart(2, "0") + ":" + String(sast.getUTCMinutes()).padStart(2, "0");
const firstOffset = nowHHMM < CUTOFF ? 0 : 1;

const WEEKS_AHEAD = Number(input.weeks_ahead || 8);  // "Later date" reaches about 2 months out
const label = d => DAY[d.getUTCDay()] + " " + d.getUTCDate() + " " + MON[d.getUTCMonth()];
const short = d => d.getUTCDate() + " " + MON[d.getUTCMonth()];
const dayRow = off => {
  const t = today + off * MS, d = new Date(t), iso = d.toISOString().slice(0, 10);
  if (!WORKING_DAYS.includes(d.getUTCDay())) return null;
  const hol = HOLIDAYS.includes(iso);
  return {
    id: "day_" + iso,
    title: label(d),
    description: (off === 0 ? "Today" : off === 1 ? "Tomorrow" : "In " + off + " days") + (d.getUTCDay() === 0 || d.getUTCDay() === 6 ? " · Weekend +R50" : "") + (hol ? " · public holiday +R60" : "")
  };
};
const later = { id: "day_later", title: "Later date", description: "Further ahead? Pick a week" };
const out = (title, rows) => ({ sections_json: JSON.stringify([{ title: title, rows: rows }]), day_count: rows.filter(r => /^day_\d/.test(r.id)).length });

// "Later date" tapped: list the weeks after the first week.
if (String(input.mode || "") === "weeks") {
  const rows = [];
  for (let w = 0; w < WEEKS_AHEAD && rows.length < 10; w++) {
    const startOff = WINDOW_DAYS + 1 + w * 7, a = new Date(today + startOff * MS), b = new Date(today + (startOff + 6) * MS);
    rows.push({ id: "day_wk_" + a.toISOString().slice(0, 10), title: short(a) + " – " + short(b), description: w === 0 ? "The week after next" : "In " + Math.round(startOff / 7) + " weeks" });
  }
  return out("Pick a week", rows);
}

// A week tapped: list the days in that week.
const wk = String(input.week_id || "").replace(/^day_wk_/, "");
if (/^\d{4}-\d{2}-\d{2}$/.test(wk)) {
  const startOff = Math.round((Date.parse(wk + "T00:00:00Z") - today) / MS);
  const rows = [];
  for (let off = Math.max(startOff, firstOffset); off < startOff + 7; off++) { const r = dayRow(off); if (r) rows.push(r); }
  rows.push({ id: "day_later", title: "Other week", description: "Back to the list of weeks" });
  return out("Available days", rows);
}

const rows = [];
for (let off = firstOffset; off <= WINDOW_DAYS && rows.length < 9; off++) { const r = dayRow(off); if (r) rows.push(r); }
rows.push(later);
rows.push({ id: "day_multi", title: "Several dates", description: "Send a list of dates (and places) in one go" });
return out("Available days", rows);
