import EventEmitter from "events";
import accessibleAutocomplete from "accessible-autocomplete";
import SelectedOptions from "./selected-options";

class MultiSelector extends EventEmitter {
  constructor($el) {
    super();

    this.$el = $el;
    this.originalId = $el.id;
    this.accessibleAutocompleteElement = null;
    [this.labelMap, this.valueMap, this.values] = this.getOptions();
  }

  getOptions() {
    const labelMap = {};
    const valueMap = {};
    const values = [];
    for (const option of this.$el.options) {
      labelMap[option.textContent] = option;
      valueMap[option.value] = option;
      values.push(option.textContent);
    }
    return [labelMap, valueMap, values];
  }

  handleOnConfirm(query) {
    const option = this.labelMap[query];
    if (!option) {
      return;
    }
    option.selected = true;
    this.$el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  getConfigurationOptions() {
    const configurationOptions = {
      id: this.originalId,
      autoselect: true,
      source: this.values,
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
      const $option = this.valueMap[value];
      $option.selected = true;
    }

    this.$el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  addOptions(values) {
    for (const value of values) {
      const $option = this.valueMap[value];
      $option.selected = true;
    }

    this.$el.dispatchEvent(new Event("change", { bubbles: true }));
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

    this.$el.addEventListener("change", () =>
      this.emit(
        "change",
        [...this.$el.selectedOptions].map((o) => o.value)
      )
    );

    this.$el.style.display = "none";
  }
}

export default MultiSelector;
