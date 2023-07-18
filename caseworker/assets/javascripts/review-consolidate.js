import { PopulateTextOnRadioInput } from "./radio-populate-textarea.js";

// this JSON is added to the template through {{ form.refusal_text|json_script:"refusal_text" }}
const refusal_text = JSON.parse(
  document.getElementById("refusal_text").textContent
);
PopulateTextOnRadioInput(
  "input[name=refusal_picks]",
  "#id_refusal_reasons",
  refusal_text
).init();
