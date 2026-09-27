// Confirmation message, calendar event and Nita's alert, built from the saved booking.
const PRICE = { svc_basic: "usually R420 to R520", svc_deep: "usually R850 to R1,300", svc_moveout: "R1,500" };
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
  "💰 Price: " + PRICE[service] + (holiday ? " + R60 public holiday rate" : "") + ". Nita will confirm the final price after seeing the place.",
  "Payment is by EFT."
];
if (DEPOSIT[service]) {
  lines.push("Your booking is confirmed once the *50% deposit* is paid. The rest is due when the clean is done.");
  lines.push(BANK ? "\n🏦 Banking details:\n" + BANK : "Nita will send you the banking details.");
} else {
  lines.push("Payment is due when the clean is done.");
}
lines.push("", "Cancelling less than " + LATE + " before (or on the day) carries a *R150* late-cancellation fee.");
lines.push("To cancel or change, please message Nita directly.");

const summary = "🧹 " + label + " · " + where + " · " + name;
const description = [
  "Client: " + name,
  "WhatsApp: +" + String(input.wa_id || ""),
  "Service: " + label,
  "Property: " + (prop || "?"),
  "Where: " + where,
  "Access code: " + (noCode ? "none, keys at reception (mailbox)" : code),
  note ? "Access note: " + note : "",
  "Price: " + PRICE[service] + (holiday ? " + R60 public holiday" : "") + " (TBC by Nita)",
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
