import { populateTextOnRadioInput } from "./radio-populate-textarea.js";

// this JSON is added to the template through {{ form.refusal_text|json_script:"refusal_text" }}
var refusal_text = JSON.parse(
  document.getElementById("refusal_text").textContent
);
populateTextOnRadioInput(
  "input[name=refusal_picks]",
  "#id_refusal_reasons",
  refusal_text
);
