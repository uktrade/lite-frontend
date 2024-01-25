import EventEmitter from "events";
import accessibleAutocomplete from "accessible-autocomplete";
import SelectedOptions from "./selected-options";

class MultiSelector extends EventEmitter {
  constructor($el, queryEngine) {
    super();

    this.$el = $el;
    this.originalId = $el.id;
    this.accessibleAutocompleteElement = null;
    [this.labelMap, this.valueMap, this.values] = this.getOptions();
    this.queryEngine = queryEngine || null;
  }

  getOptions() {
    const labelMap = new Map();
    const valueMap = new Map();
    const values = [];
    for (const option of this.$el.options) {
      labelMap.set(option.textContent, option);
      valueMap.set(option.value, option);
      values.push(option.textContent);
    }
    return [labelMap, valueMap, values];
  }

  handleOnConfirm(query) {
    const option = this.labelMap.get(query);
    if (!option) {
      return;
    }
    option.selected = true;
    this.$el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  getConfigurationOptions() {
    let source = this.values;
    if (this.queryEngine) {
      source = (query, populateResults) => {
        populateResults(this.queryEngine(query, this.values));
      };
    }
    const configurationOptions = {
      id: this.originalId,
      autoselect: true,
      source: source,
      displayMenu: "overlay",
      cssNamespace: "lite-autocomplete",
      templates: {
        inputValue: () => "",
      },
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

  setOptions(values) {
    for (const $option of [...this.$el.selectedOptions]) {
      $option.selected = false;
    }

    for (const value of values) {
      const $option = this.valueMap.get(value);
      $option.selected = true;
    }

    this.$el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  addOptions(values) {
    for (const value of values) {
      const $option = this.valueMap.get(value);
      $option.selected = true;
    }

    this.$el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  emitChangeEvent() {
    this.emit(
      "change",
      [...this.$el.selectedOptions].map((o) => o.value)
    );
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
    this.selectedOptions = selectedOptions;

    this.$el.parentNode.insertBefore(selectedOptionsWrapper, this.$el);

    this.$el.addEventListener("change", () => this.emitChangeEvent());
    this.emitChangeEvent();

    this.$el.style.display = "none";
  }
}

const startsWith = (query, values) => {
  const val = query.toLowerCase();
  return values
    .filter((v) => v.toLowerCase().includes(val))
    .sort((a, b) => {
      const aStarts = a.toLowerCase().startsWith(val);
      const bStarts = b.toLowerCase().startsWith(val);
      if (aStarts && bStarts) return a.localeCompare(b);
      if (aStarts && !bStarts) return -1;
      if (!aStarts && bStarts) return 1;
      return a.localeCompare(b);
    });
};

export default MultiSelector;

export { startsWith };
