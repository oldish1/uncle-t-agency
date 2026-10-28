// Change / cancel, step 2: one booking tapped. Work out if it's less than 24 hours away (late fee).
const DAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const LABEL = { svc_basic: "Basic Clean", svc_deep: "Deep Clean", svc_moveout: "Move Out / In Clean" };
const FEE = String(input.late_fee || "R150");
const LATE_HOURS = Number(input.late_hours || 24);
let e = input.event_json;
if (typeof e === "string") { try { e = JSON.parse(e || "{}"); } catch (x) { e = {}; } }
if (e && e.body && !e.id) e = e.body;
if (!e || !e.id || !e.start || !e.start.dateTime || e.status === "cancelled" || /^❌/.test(String(e.summary || "")))
  return { ok: false, text_json: JSON.stringify("Sorry, I can't find that booking any more. Send *change* or *cancel* to try again."), booking_json: "" };
const now = input.now_iso ? new Date(input.now_iso) : new Date();
const start = Date.parse(e.start.dateTime);
const hours = (start - now.getTime()) / 3600000;
const late = hours < LATE_HOURS;
const d = new Date(start + 2 * 3600000), pad = n => String(n).padStart(2, "0");
const when = DAY[d.getUTCDay()] + " " + d.getUTCDate() + " " + MON[d.getUTCMonth()] + ", " + pad(d.getUTCHours()) + ":" + pad(d.getUTCMinutes());
const svc = (e.extendedProperties && e.extendedProperties.private && e.extendedProperties.private.service) || "svc_basic";
const where = String(e.summary || "").split(" · ")[1] || "";
let text = "Your booking:\n🧹 " + (LABEL[svc] || "Clean") + "\n🗓️ " + when + (where ? "\n🏢 " + where : "") + "\n\nWhat would you like to do?";
if (late) text += "\n\n⚠️ This clean is less than " + LATE_HOURS + " hours away, so a *" + FEE + "* fee applies if you change or cancel it.";
return { ok: true, late: late ? "yes" : "no", when: when,
  text_json: JSON.stringify(text),
  booking_json: JSON.stringify({ id: e.id, summary: e.summary || "", description: e.description || "", start: e.start.dateTime, end: e.end && e.end.dateTime, service: svc, when: when, late: late }) };
