// Date + duration builder for the tapped time slot.
const DURATION_HOURS = { svc_basic: 2, svc_deep: 3.5, svc_moveout: 4 };
const SERVICE_LABEL = { svc_basic: "Basic Clean", svc_deep: "Deep Clean", svc_moveout: "Move Out / Move In Clean" };
const SLOTS = { slot_0800: "08:00", slot_1200: "12:00", slot_1500: "15:00" };
const MIN_LEAD_MIN = 60;                 // same-day: slot must start at least this far from now
const DAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const pad = n => String(n).padStart(2, "0");
const bad = (code, text) => ({ ok: false, error: code, error_text_json: JSON.stringify(text) });

const dayIso = String(input.day_id || "").replace(/^day_/, "");
const service = String(input.service_id || "");
const slot = SLOTS[String(input.slot_id || "")];
if (!/^\d{4}-\d{2}-\d{2}$/.test(dayIso) || !DURATION_HOURS[service] || !slot)
  return bad("bad_input", "Sorry, that option has expired. Send *hi* to start a new booking.");

const startIso = dayIso + "T" + slot + ":00+02:00";
const now = input.now_iso ? new Date(input.now_iso) : new Date();
if (Date.parse(startIso) < now.getTime() + MIN_LEAD_MIN * 60000)
  return bad("too_soon", "Sorry, that time has already passed or is too soon. Send *hi* to pick another day or time.");

const [h, m] = slot.split(":").map(Number);
const endMin = h * 60 + m + Math.round(DURATION_HOURS[service] * 60);
const endIso = dayIso + "T" + pad(Math.floor(endMin / 60)) + ":" + pad(endMin % 60) + ":00+02:00";
const d = new Date(dayIso + "T12:00:00Z");
const dayLabel = DAY[d.getUTCDay()] + " " + d.getUTCDate() + " " + MON[d.getUTCMonth()];
const hrs = DURATION_HOURS[service];

return {
  ok: true, error: "", error_text_json: "\"\"",
  service_label: SERVICE_LABEL[service], duration_hours: hrs,
  start_iso: startIso, end_iso: endIso,
  day_label: dayLabel, time_label: slot,
  when_label: dayLabel + ", " + slot + " (about " + hrs + " hrs)",
  day_start: dayIso + "T00:00:00+02:00",
  day_end: dayIso + "T23:59:59+02:00"
};
