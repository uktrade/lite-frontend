import accessibleAutocomplete from "accessible-autocomplete";
import SelectedOptions from "./selected-options";

class MultiSelector {
  constructor($el) {
    this.$el = $el;
    this.originalId = $el.id;
    this.accessibleAutocompleteElement = null;
    [this.map, this.values] = this.getOptions();
  }

  getOptions() {
    const map = {};
    const values = [];
    for (const option of this.$el.options) {
      const optionText = option.textContent;
      map[optionText] = option;
      values.push(optionText);
    }
    return [map, values];
  }

  handleOnConfirm(query) {
    const option = this.map[query];
    if (!option) {
      return;
    }
    option.selected = true;
    option.dispatchEvent(new Event("change", { bubbles: true }));

    // We have to set the value like this due to the fact that the accessible
    // autocomplete will re-render and retain its value (because it's a React
    // component) and so we want to let the component re-render first and then
    // set it's value.
    // This works by relying on the fact that the re-render will be happening on
    // the current stack so we'll purposefully push this onto the bottom of the
    // stack to make it run after the re-render.
    // This certainly won't be perfect and may sometimes not work as expected
    // but this is the best we've got without changing the accessible
    // autocomplete itself.
    setTimeout(() => (this.accessibleAutocompleteElement.value = ""), 0);
  }

  getConfigurationOptions() {
    const configurationOptions = {
      id: this.originalId,
      autoselect: true,
      source: this.values,
      displayMenu: "overlay",
      cssNamespace: "lite-autocomplete",
      onConfirm: (query) => this.handleOnConfirm(query),
    };

    return configurationOptions;
  }

  createAutocompleteWrapper() {
    const autocompleteWrapper = document.createElement("div");
    autocompleteWrapper.classList.add("autocomplete__wrapper");

    this.$el.parentNode.insertBefore(autocompleteWrapper, this.$el);
    return autocompleteWrapper;
  }

  init() {
    const autocompleteWrapper = this.createAutocompleteWrapper();
    this.$el.id = `${this.originalId}-select`;
    accessibleAutocomplete({
      ...this.getConfigurationOptions(),
      element: autocompleteWrapper,
    });
    this.accessibleAutocompleteElement = document.querySelector(
      `#${this.originalId}`
    );

    const selectedOptionsWrapper = document.createElement("div");
    selectedOptionsWrapper.classList.add(
      "multi-select__selected-options-wrapper"
    );
    const selectedOptions = new SelectedOptions(
      selectedOptionsWrapper,
      this.$el,
      this.$el.dataset.multiSelectObjectsAsPlural
    );
    selectedOptions.init();
    this.$el.parentNode.insertBefore(selectedOptionsWrapper, this.$el);

    this.$el.style.display = "none";
  }
}

export default MultiSelector;
