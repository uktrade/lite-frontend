import accessibleAutocomplete from "accessible-autocomplete";

class AutoCompleteSelector {
  constructor($el) {
    this.$el = $el;
  }

  init() {
    accessibleAutocomplete.enhanceSelectElement({
      defaultValue: "",
      selectElement: this.$el,
      showAllValues: true,
      cssNamespace: "lite-autocomplete",
    });
  }
}

export default AutoCompleteSelector;
