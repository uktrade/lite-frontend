import accessibleAutocomplete from "accessible-autocomplete";

class AutoCompleteSelector {
  constructor($el) {
    this.$el = $el;
  }

  init() {
    accessibleAutocomplete.enhanceSelectElement({
      defaultValue: false,
      selectElement: this.$el,
      showAllValues: true,
    });
  }
}

export default AutoCompleteSelector;
