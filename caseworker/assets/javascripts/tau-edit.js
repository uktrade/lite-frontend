import NoSuggestionsTokenField from "./tau/no-suggestions-token-field";
import CLESuggestions from "./tau/cle-suggestions";
import SuggestionsTokenField from "./tau/suggestions-token-field";
import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";
import initARS from "./tau/ars";

const initAssessmentForm = () => {
  const noControlListCheckboxEl = document.querySelector(
    "[name=does_not_have_control_list_entries]"
  );
  const noSuggestionsTokenField = new NoSuggestionsTokenField(
    "#control_list_entries",
    noControlListCheckboxEl
  );
  noSuggestionsTokenField.init();

  const suggestionsTokenField = new SuggestionsTokenField(
    "#control_list_entries"
  );

  const suggestionsEl = document.createElement("div");
  suggestionsEl.classList.add("tau__cle-suggestions");
  const controlListEntriesLabel = document.querySelector(
    "[for=control_list_entries]"
  );
  controlListEntriesLabel.parentNode.insertBefore(
    suggestionsEl,
    controlListEntriesLabel.nextSibling
  );

  const cleSuggestions = new CLESuggestions(
    suggestionsEl,
    (selectedSuggestions) => {
      suggestionsTokenField.setSuggestions(selectedSuggestions);
      noSuggestionsTokenField.reset();
    }
  );

  const mtcrEntriesEl = document.querySelector("#mtcr_entries");
  progressivelyEnhanceMultipleSelectField(mtcrEntriesEl, (option) => {
    return { id: option.value, name: option.label, classes: [] };
  });

  const products = JSON.parse(
    document.querySelector("#cle-suggestions-json").textContent
  );
  cleSuggestions.setProducts(products);
};

initAssessmentForm();
initARS();
