// Several dates, step 4: time tapped. Re-check against the calendar, then build one
// calendar event per date (event_json_1 … event_json_10) and one confirmation.
const SLOTS = { slot_0800: "08:00", slot_1000: "10:00", slot_1100: "11:00", slot_1200: "12:00", slot_1500: "15:00" };
const HOURS = { svc_basic: 3, svc_deep: 3.5, svc_moveout: 4 };
const DUR = { svc_basic: "3+ hrs", svc_deep: "about 3.5 hrs", svc_moveout: "about 4 hrs" };
const LABEL = { svc_basic: "Basic Clean", svc_deep: "Deep Clean", svc_moveout: "Move Out / Move In Clean" };
const PRICE = { svc_basic: "from R420 to R520", svc_deep: "from R850 to R1,300", svc_moveout: "R1,500" };
const DEPOSIT = { svc_deep: true, svc_moveout: true };
const POINTS = { svc_basic: 1, svc_deep: 2, svc_moveout: 2 };
const DAY_CAPACITY = Number(input.day_capacity || 2);
const HOLIDAYS = String(input.holidays || "").split(",").map(s => s.trim()).filter(Boolean);
const LATE = String(input.late_window || "24 hours");
const BANK = String(input.bank_details || "").trim();
const pad = n => String(n).padStart(2, "0");
const heavy = t => /deep|move/i.test(t);
const isOff = t => /^(nita\s+)?off\b/i.test(t);
const sastDay = iso => new Date(Date.parse(iso) + 2 * 3600000).toISOString().slice(0, 10);

const slot = SLOTS[String(input.slot_id || "")];
let lines = [];
try { lines = JSON.parse(String(input.lines_json || "[]")); } catch (e) { lines = []; }
const out = { ok: false, count: 0, confirm_json: JSON.stringify("Sorry, that list has expired. Send *hi* to start again."), last_day: "", last_service: "" };
for (let i = 1; i <= 10; i++) out["event_json_" + i] = "";
if (!slot || !lines.length) return out;

// fresh look at the calendar, in case someone booked meanwhile
let raw = input.events_json;
if (typeof raw === "string") { try { raw = JSON.parse(raw || "{}"); } catch (e) { raw = {}; } }
const items = Array.isArray(raw) ? raw : ((raw && (raw.items || (raw.body && raw.body.items))) || []);
const used = {};
const add = (d, p) => { used[d] = (used[d] || 0) + p; };
items.filter(e => e && e.status !== "cancelled" && e.start && e.end && !/^❌/.test(String(e.summary || ""))).forEach(e => {
  const title = String(e.summary || "").trim();
  if (isOff(title)) return;
  if (e.start.date) {
    for (let t = Date.parse(String(e.start.date).slice(0, 10) + "T00:00:00Z"); t < Date.parse(String(e.end.date).slice(0, 10) + "T00:00:00Z"); t += 86400000)
      title.split(/&|,|\band\b/i).map(x => x.trim()).filter(Boolean).forEach(j => add(new Date(t).toISOString().slice(0, 10), heavy(j) ? 2 : 1));
  } else if (e.start.dateTime) {
    const svc = e.extendedProperties && e.extendedProperties.private && e.extendedProperties.private.service;
    add(sastDay(e.start.dateTime), svc ? (POINTS[svc] || 1) : (heavy(title) ? 2 : 1));
  }
});

const name = String(input.client_name || "").trim();
const firstName = name.split(" ")[0] || "there";
const now = input.now_iso ? new Date(input.now_iso) : new Date();
const booked = [], missed = [];
let n = 0;
lines.forEach(l => {
  const p = POINTS[l.service] || 1;
  const startIso = l.day + "T" + slot + ":00+02:00";
  if (Date.parse(startIso) < now.getTime() + 3600000) { missed.push(l.label + " (that time has passed)"); return; }
  if ((used[l.day] || 0) + p > DAY_CAPACITY) { missed.push(l.label + " (just got booked up)"); return; }
  add(l.day, p);
  const [h, m] = slot.split(":").map(Number);
  const endMin = h * 60 + m + Math.round(HOURS[l.service] * 60);
  const endIso = l.day + "T" + pad(Math.floor(endMin / 60)) + ":" + pad(endMin % 60) + ":00+02:00";
  const where = [l.building, l.unit ? "Unit " + l.unit : ""].filter(Boolean).join(", ") || "Usual place";
  const dow = new Date(l.day + "T12:00:00Z").getUTCDay(), weekend = dow === 0 || dow === 6, hol = HOLIDAYS.includes(l.day);
  const extra = (weekend ? " + R50 weekend rate" : "") + (hol ? " + R60 public holiday rate" : "");
  const noCode = /^none/i.test(l.code);
  n++;
  out["event_json_" + n] = JSON.stringify({
    summary: "🧹 " + LABEL[l.service] + " · " + where + " · " + name,
    description: ["Client: " + name, "WhatsApp: " + (/^\d+$/.test(String(input.wa_id || "")) ? "+" + input.wa_id : String(input.wa_id || "") + " (WhatsApp username, no number shared: reply in Luna's chat)"), "Service: " + LABEL[l.service], "Where: " + where,
      "Access code: " + (l.code ? (noCode ? "none, keys at reception (mailbox)" : l.code) : "not given, check with client"),
      "Client wrote: " + l.raw, "Price: " + PRICE[l.service] + extra + " (TBC by Nita)",
      DEPOSIT[l.service] ? "Deposit: 50% needed to confirm" : "Payment: on completion",
      "Booked via WhatsApp bot (several dates)"].join("\n"),
    start: { dateTime: startIso, timeZone: "Africa/Johannesburg" },
    end: { dateTime: endIso, timeZone: "Africa/Johannesburg" },
    extendedProperties: { private: { source: "r2r-bot", wa_id: String(input.wa_id || ""), service: l.service } }
  });
  booked.push({ l: l, where: where, extra: extra });
  out.last_day = l.day; out.last_service = LABEL[l.service];
});

if (!booked.length) {
  out.confirm_json = JSON.stringify("Sorry, none of those dates could be booked:\n" + missed.map(x => "❌ " + x).join("\n") + "\n\nSend *hi* to pick other days.");
  return out;
}
const svcs = [...new Set(booked.map(b => b.l.service))];
const msg = ["✅ *Bookings received, " + firstName + "!*", ""]
  .concat(booked.map(b => "🧹 " + b.l.label + ", " + slot + " · " + LABEL[b.l.service] + " (" + DUR[b.l.service] + ")\n     🏢 " + b.where))
  .concat(missed.length ? ["", "Couldn't book:"].concat(missed.map(x => "❌ " + x)) : [])
  .concat(["", "💰 Price: " + svcs.map(s => LABEL[s] + " " + PRICE[s]).join("; ") + ".",
    "Saturdays and Sundays +R50, public holidays +R60.",
    "Nita will confirm the final price after seeing each place. Rates are based on one and two bedroom apartments; any additional bedrooms will be quoted separately."]);
if (svcs.some(s => DEPOSIT[s])) {
  msg.push("Deep and Move Out cleans are confirmed once the *50% deposit* is paid. The rest is due via EFT upon completion of the clean.");
  msg.push(BANK ? "\n🏦 Banking details:\n" + BANK : "Nita will send you the banking details.");
} else msg.push("Payment due via EFT upon completion of each clean.");
msg.push("", "A *R150* cancellation fee will be charged if a clean is cancelled less than " + LATE + " before (or on the day).", "Need to change or cancel? Just send *change* or *cancel* here. For anything else, please contact Ms Adams directly.");
let text = msg.join("\n");
if (text.length > 4000) text = text.slice(0, 3990) + "…";
out.ok = true; out.count = n; out.confirm_json = JSON.stringify(text);
out.first_unit = booked[0].l.unit; out.first_building = booked[0].l.building; out.first_code = booked[0].l.code;
return out;
