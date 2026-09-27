// Day picker. Settings come from the "Inbound + config" step.
const SAST = 2;                                   // Cape Town, no daylight saving
const WINDOW_DAYS = Number(input.window_days || 7); // Nita: next week only
const WORKING_DAYS = [0, 1, 2, 3, 4, 5, 6];       // Nita: Mon to Sat, plus Sundays at +R50
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

const rows = [];
for (let off = firstOffset; off <= WINDOW_DAYS && rows.length < 9; off++) {
  const t = today + off * MS, d = new Date(t), iso = d.toISOString().slice(0, 10);
  if (!WORKING_DAYS.includes(d.getUTCDay())) continue;
  const hol = HOLIDAYS.includes(iso);
  rows.push({
    id: "day_" + iso,
    title: DAY[d.getUTCDay()] + " " + d.getUTCDate() + " " + MON[d.getUTCMonth()],
    description: (off === 0 ? "Today" : off === 1 ? "Tomorrow" : "In " + off + " days") + (d.getUTCDay() === 0 ? " · Sunday +R50" : "") + (hol ? " · public holiday +R60" : "")
  });
}
rows.push({ id: "day_later", title: "Later date", description: "More than a week away? Message Nita" });

return { sections_json: JSON.stringify([{ title: "Available days", rows: rows }]), day_count: rows.length - 1 };
