import AutoCompleteSelector from "core/autocomplete-selector";

const initAutoCompleteSelects = () => {
  document
    .querySelectorAll("[data-module=autocomplete-select]")
    .forEach(($el) => new AutoCompleteSelector($el).init());
};

export default initAutoCompleteSelects;
