// Change / cancel, step 3a: cancel. Keep the event in Nita's calendar, marked ❌ so Luna stops counting it.
const FEE = String(input.late_fee || "R150");
let b = {};
try { b = JSON.parse(String(input.booking_json || "{}")); } catch (e) { b = {}; }
if (!b.id) return { ok: false, event_id: "", patch_json: "{}", text_json: JSON.stringify("Sorry, that booking has expired. Send *cancel* to try again.") };
const now = input.now_iso ? new Date(input.now_iso) : new Date();
const stamp = new Date(now.getTime() + 2 * 3600000).toISOString().slice(0, 16).replace("T", " ");
const feeNote = b.late ? " · " + FEE + " LATE FEE" : "";
const patch = {
  summary: ("❌ CANCELLED" + feeNote + " · " + String(b.summary || "").replace(/^🧹\s*/, "")).slice(0, 250),
  description: "CANCELLED by client via Luna on " + stamp + (b.late ? "\nLate cancellation (less than 24 hours before): " + FEE + " fee applies." : "\nCancelled in time: no fee.") + "\n\n" + String(b.description || ""),
  transparency: "transparent",
  colorId: "8"
};
let text = "Done, your booking for *" + b.when + "* is cancelled.";
text += b.late ? "\n\nBecause it was less than 24 hours before the clean, the *" + FEE + "* cancellation fee applies. Ms Adams will send you the details." : "\n\nNo fee, thanks for letting us know in time 🙏";
text += "\n\nSend *hi* any time to book again.";
return { ok: true, event_id: b.id, patch_json: JSON.stringify(patch), text_json: JSON.stringify(text) };
