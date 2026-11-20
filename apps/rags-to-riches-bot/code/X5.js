// Change: the client typed a new date instead of tapping one ("14 Nov", "14/11", "Friday 14 November").
const MONS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
const t = String(input.text || "").toLowerCase();
const now = input.now_iso ? new Date(input.now_iso) : new Date();
const today = new Date(now.getTime() + 2 * 3600000);
const y0 = today.getUTCFullYear();
let d = null, mo = null, m;
if ((m = t.match(/(\d{1,2})\s*(?:st|nd|rd|th)?\s*(?:of\s+)?([a-z]{3,})/)) && MONS.indexOf(m[2].slice(0, 3)) >= 0) { d = +m[1]; mo = MONS.indexOf(m[2].slice(0, 3)); }
else if ((m = t.match(/([a-z]{3,})\s+(\d{1,2})/)) && MONS.indexOf(m[1].slice(0, 3)) >= 0) { d = +m[2]; mo = MONS.indexOf(m[1].slice(0, 3)); }
else if ((m = t.match(/\b(\d{1,2})[\/\-.](\d{1,2})\b/))) { d = +m[1]; mo = +m[2] - 1; }
if (d === null || mo < 0 || mo > 11 || d < 1 || d > 31) return { ok: false, day_id: "", day_label: "" };
let iso = new Date(Date.UTC(y0, mo, d)).toISOString().slice(0, 10);
if (iso < today.toISOString().slice(0, 10)) iso = new Date(Date.UTC(y0 + 1, mo, d)).toISOString().slice(0, 10);
const dt = new Date(iso + "T12:00:00Z");
if (dt.getUTCDate() !== d) return { ok: false, day_id: "", day_label: "" };
const DAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
return { ok: true, day_id: "rs_day_" + iso, day_label: DAY[dt.getUTCDay()] + " " + d + " " + MON[mo] };
