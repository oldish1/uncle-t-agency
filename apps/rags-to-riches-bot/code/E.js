// Runs IMMEDIATELY after the Claude HTTP module. No aggregator in between.
// Input claude_body: the HTTP module's response body (raw text or parsed, both work).
const step = String(input.step || "");
const savedUnit = String(input.saved_unit || "");
const savedCode = String(input.saved_code || "");

const fail = reason => ({
  ok: false, error: reason, intent: "unclear", is_complete: false,
  unit_number: savedUnit, building_name: "", access_code: savedCode, access_note: "", client_name: "",
  missing: step === "NAME" ? "client_name" : "unit_number,access_code",
  reprompt_json: JSON.stringify(step === "NAME"
    ? "Sorry, I didn't catch that. What name should Nita put the booking under?"
    : "Sorry, I didn't catch that. Please send your apartment number and the lockbox or gate code, e.g. *Unit 1204, code 4471*")
});

let resp = input.claude_body;
if (typeof resp === "string") { try { resp = JSON.parse(resp); } catch (e) { return fail("body_not_json"); } }
if (!resp || resp.type === "error") return fail("api_error");
if (resp.stop_reason === "refusal" || resp.stop_reason === "max_tokens") return fail("stop_" + resp.stop_reason);

const block = (resp.content || []).find(b => b && b.type === "text");
if (!block || !block.text) return fail("no_text");

let text = block.text.trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "");
const first = text.indexOf("{"), last = text.lastIndexOf("}");
if (first === -1 || last <= first) return fail("no_json");
let out;
try { out = JSON.parse(text.slice(first, last + 1)); } catch (e) { return fail("bad_json"); }

const clean = v => String(v == null ? "" : v).replace(/\s+/g, " ").trim().slice(0, 80);
const intent = ["details", "restart", "cancel", "question", "unclear"].includes(out.intent) ? out.intent : "unclear";

// New values win; otherwise keep what the session already had (client may send them in two messages)
const unit = clean(out.unit_number) || savedUnit;
const code = clean(out.access_code) || savedCode;
const name = clean(out.client_name);

let missing = [];
if (step === "UNIT_ACCESS") { if (!unit) missing.push("unit_number"); if (!code) missing.push("access_code"); }
if (step === "NAME") { if (!name) missing.push("client_name"); }
const isComplete = missing.length === 0 && (intent === "details" || intent === "unclear" || intent === "question");

let reprompt = "";
const prefix = intent === "question" ? "Nita will answer that personally when she confirms your booking 🙂\n\n" : "";
if (step === "UNIT_ACCESS") {
  if (missing.length === 2) reprompt = prefix + "Please send your apartment number and the lockbox or gate code, e.g. *Unit 1204, code 4471*";
  else if (missing[0] === "unit_number") reprompt = prefix + "Thanks! And the apartment or unit number?";
  else if (missing[0] === "access_code") reprompt = prefix + "Thanks! And the lockbox or gate code? If there isn't one, just tell me how the team gets in.";
} else if (step === "NAME" && missing.length) {
  reprompt = prefix + "What name should Nita put the booking under?";
}

return {
  ok: true,
  error: "",
  intent: intent,
  is_complete: isComplete,
  unit_number: unit,
  building_name: clean(out.building_name),
  access_code: code,
  access_note: clean(out.access_note),
  client_name: name,
  missing: missing.join(","),
  reprompt_json: JSON.stringify(reprompt)
};
