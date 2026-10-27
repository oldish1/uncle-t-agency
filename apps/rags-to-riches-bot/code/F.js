// Confirmation message, calendar event and Nita's alert, built from the saved booking.
const PRICE = { svc_basic: "from R420 to R520", svc_deep: "from R850 to R1,300", svc_moveout: "R1,500" };
const DEPOSIT = { svc_deep: true, svc_moveout: true };      // Nita: Deep and Move Out need 50% upfront
const HOLIDAYS = String(input.holidays || "").split(",").map(s => s.trim()).filter(Boolean);
const LATE = String(input.late_window || "24 hours");
const BANK = String(input.bank_details || "").trim();

const service = String(input.service_id || "");
const label = String(input.service_label || "");
const name = String(input.client_name || "").trim();
const firstName = name.split(" ")[0] || "there";
const prop = String(input.property_type || "");
const unit = String(input.unit_number || "");
const building = String(input.building_name || "");
const code = String(input.access_code || "");
const note = String(input.access_note || "");
const dayIso = String(input.start_iso || "").slice(0, 10);
const holiday = HOLIDAYS.includes(dayIso);
const noCode = /^none/i.test(code);
const dow = new Date(dayIso + "T12:00:00Z").getUTCDay(), weekend = dow === 0 || dow === 6;
const extra = (weekend ? " + R50 weekend rate" : "") + (holiday ? " + R60 public holiday rate" : "");

const where = prop === "Apartment" || building
  ? (building ? building + ", " : "") + "Unit " + unit
  : unit;

const lines = [
  "✅ *Booking received, " + firstName + "!*",
  "",
  "🧹 *" + label + "*",
  "🗓️ " + input.when_label,
  "🏢 " + where,
  noCode ? "🔑 Keys at reception (mailbox)" : "🔑 Access details saved",
  "",
  "💰 Price: " + label + " " + PRICE[service] + ".",
  "Saturdays and Sundays +R50, public holidays +R60.",
  "Nita will confirm the final price after seeing the place. Rates are based on one and two bedroom apartments; any additional bedrooms will be quoted separately."
];
if (DEPOSIT[service]) {
  lines.push("Your booking is confirmed once the *50% deposit* is paid. The rest is due via EFT upon completion of the clean.");
  lines.push(BANK ? "\n🏦 Banking details:\n" + BANK : "Nita will send you the banking details.");
} else {
  lines.push("Payment due via EFT upon completion of the clean.");
}
lines.push("", "A *R150* cancellation fee will be charged if a clean is cancelled less than " + LATE + " before (or on the day).");
lines.push("For any changes to your booking, please contact Ms Adams directly.");

const summary = "🧹 " + label + " · " + where + " · " + name;
const description = [
  "Client: " + name,
  "WhatsApp: " + (/^\d+$/.test(String(input.wa_id || "")) ? "+" + input.wa_id : String(input.wa_id || "") + " (WhatsApp username, no number shared: reply in Luna's chat)"),
  "Service: " + label,
  "Property: " + (prop || "?"),
  "Where: " + where,
  "Access code: " + (noCode ? "none, keys at reception (mailbox)" : code),
  note ? "Access note: " + note : "",
  "Price: " + PRICE[service] + extra + " (TBC by Nita)",
  DEPOSIT[service] ? "Deposit: 50% needed to confirm" : "Payment: on completion",
  "Booked via WhatsApp bot"
].filter(Boolean).join("\n");

return {
  confirm_json: JSON.stringify(lines.join("\n")),
  event_json: JSON.stringify({
    summary: summary, description: description,
    start: { dateTime: input.start_iso, timeZone: "Africa/Johannesburg" },
    end: { dateTime: input.end_iso, timeZone: "Africa/Johannesburg" },
    extendedProperties: { private: { source: "r2r-bot", wa_id: String(input.wa_id || ""), service: service } }
  }),
  alert_params_json: JSON.stringify([name, label, String(input.when_label || ""), where, "+" + String(input.wa_id || "")].map(t => ({ type: "text", text: t || "-" }))),
  where: where
};
