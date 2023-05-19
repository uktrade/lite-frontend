import NoSuggestionsTokenField from "./tau/no-suggestions-token-field";
import CLESuggestions from "./tau/cle-suggestions";
import SuggestionsTokenField from "./tau/suggestions-token-field";
import initARS from "./tau/ars";
import initRegimes from "./tau/regimes";
import ShowHideNcscField from "./tau/show-hide-ncsc-field";

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
  suggestionsEl.classList.add("tau-assessment-form__cle-suggestions");
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

  const products = JSON.parse(
    document.querySelector("#cle-suggestions-json").textContent
  );
  cleSuggestions.setProducts(products);

  const ncscBox = document.querySelector(
    "#div_id_is_ncsc_military_information_security"
  );
  if (ncscBox) {
    const ncscFormField = new ShowHideNcscField(
      "#control_list_entries",
      ncscBox
    );

    ncscFormField.toggleField();
    ncscFormField.setOnChangeListener();
  }
};

initAssessmentForm();
initARS();
initRegimes();
