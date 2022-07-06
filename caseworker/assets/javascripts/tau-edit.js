import NoSuggestionsTokenField from "./tau/no-suggestions-token-field";
import CLESuggestions from "./tau/cle-suggestions";
import SuggestionsTokenField from "./tau/suggestions-token-field";

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

  const suggestionsEl = document.querySelector(".tau__cle-suggestions");
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
};

initAssessmentForm();
