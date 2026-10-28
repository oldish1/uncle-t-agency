// Change / cancel, step 1: list the client's upcoming bookings from Nita's calendar.
const DAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const LABEL = { svc_basic: "Basic Clean", svc_deep: "Deep Clean", svc_moveout: "Move Out / In" };
let raw = input.events_json;
if (typeof raw === "string") { try { raw = JSON.parse(raw || "{}"); } catch (e) { raw = {}; } }
const items = Array.isArray(raw) ? raw : ((raw && (raw.items || (raw.body && raw.body.items))) || []);
const sast = iso => new Date(Date.parse(iso) + 2 * 3600000);
const pad = n => String(n).padStart(2, "0");
const rows = items
  .filter(e => e && e.status !== "cancelled" && e.start && e.start.dateTime && !/^❌/.test(String(e.summary || "")))
  .sort((a, b) => Date.parse(a.start.dateTime) - Date.parse(b.start.dateTime))
  .slice(0, 10)
  .map(e => {
    const d = sast(e.start.dateTime);
    const svc = e.extendedProperties && e.extendedProperties.private && e.extendedProperties.private.service;
    const where = String(e.summary || "").split(" · ")[1] || "";
    return { id: "bk_" + e.id,
      title: (DAY[d.getUTCDay()] + " " + d.getUTCDate() + " " + MON[d.getUTCMonth()] + ", " + pad(d.getUTCHours()) + ":" + pad(d.getUTCMinutes())).slice(0, 24),
      description: ((LABEL[svc] || "Clean") + (where ? " · " + where : "")).slice(0, 72) };
  });
return {
  count: rows.length,
  sections_json: JSON.stringify([{ title: "Your bookings", rows: rows }]),
  none_json: JSON.stringify("I can't find any upcoming bookings for this number 🤔 If you booked another way, please contact Ms Adams directly.")
};
