import autoComplete from "@tarekraafat/autocomplete.js";

import {
  getCurrentWord,
  isIndexInPattern,
  replaceAtPosition,
} from "./string-utils";

class ProductSearchSuggestor {
  constructor(autoComplete, $el) {
    this.autoComplete = autoComplete;
    this.$el = $el;
    this.$form = $el.querySelector(".product-search__form");
    this.productFilterLabels = JSON.parse(
      this.$form.dataset.productFilterLabels
    );
    this.searchUrl = this.$form.dataset.searchUrl;
    this.searchInputSelector = ".product-search__search-field";
    this.$searchInput = $el.querySelector(this.searchInputSelector);
    this.wildcardField = "wildcard";
  }

  init() {
    this.setupAutoComplete();
  }

  getQuery() {
    const currentValue = this.$searchInput.value;
    const caretPosition = this.$searchInput.selectionStart;
    if (isIndexInPattern(caretPosition, '[a-z_]+?:".*?"', currentValue)) {
      return "";
    }
    const [currentWord, ,] = getCurrentWord(currentValue, caretPosition);
    return currentWord;
  }

  async getSuggestions(query) {
    const url = `${this.searchUrl}?q=${encodeURIComponent(query)}`;
    const response = await fetch(url, {
      headers: {
        Accept: "application/json",
      },
    });
    const suggestions = await response.json();
    return suggestions;
  }

  async dataSource() {
    const query = this.getQuery();
    return await this.getSuggestions(query);
  }

  getFieldCell(field) {
    if (field === this.wildcardField) {
      return null;
    }

    const fieldCell = document.createElement("td");
    fieldCell.classList.add("product-search__suggest-results-key");
    const label = this.productFilterLabels[field];
    fieldCell.textContent = label;

    return fieldCell;
  }

  getValueCell(value, hasField) {
    const valueCell = document.createElement("td");
    valueCell.classList.add("product-search__suggest-results-value");
    valueCell.textContent = value;
    if (!hasField) {
      valueCell.colSpan = 2;
    }
    return valueCell;
  }

  renderItem(data, source) {
    source.innerHTML = "";

    let hasField = false;
    const fieldCell = this.getFieldCell(data.value.field);
    if (fieldCell) {
      hasField = true;
      source.appendChild(fieldCell);
    }

    const valueCell = this.getValueCell(data.value.value, hasField);
    source.appendChild(valueCell);
  }

  handleSelection(option) {
    const currentValue = this.$searchInput.value;
    const caretPosition = this.$searchInput.selectionStart;
    const [, startIndex, endIndex] = getCurrentWord(
      currentValue,
      caretPosition
    );

    const { field, value } = option.selection.value;
    let newValue;
    if (field === this.wildcardField) {
      newValue = value;
    } else {
      newValue = `${field}:"${value}"`;
    }

    const [updatedValue, ,] = replaceAtPosition(
      currentValue,
      newValue,
      startIndex,
      endIndex
    );

    this.$searchInput.value = updatedValue;
  }

  setupAutoComplete() {
    new this.autoComplete({
      selector: this.searchInputSelector,
      data: {
        src: async () => this.dataSource(),
        key: ["value"],
        cache: false,
      },
      resultsList: {
        element: "table",
        className: "product-search__suggest-results",
      },
      resultItem: {
        element: "tr",
        className: "product-search__suggest-results-row",
        content: (data, source) => this.renderItem(data, source),
      },
      onSelection: (option) => this.handleSelection(option),
      searchEngine: (query, record) => record,
      trigger: {
        event: ["input"],
        condition: () => this.getQuery().trim().length > 1,
      },
      maxResults: 10,
      debounce: 300,
    });
  }
}

const initProductSearchSuggestor = () => {
  document
    .querySelectorAll(".product-search")
    .forEach(($el) => new ProductSearchSuggestor(autoComplete, $el).init());
};

initProductSearchSuggestor();

export { ProductSearchSuggestor };
