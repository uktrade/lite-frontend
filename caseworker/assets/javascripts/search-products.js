import autoComplete from "@tarekraafat/autocomplete.js";

import { getCurrentPhrase } from "./string-utils";

/**
 * Retrieves product search suggestions and displays them as the user types
 * in the search input.
 *
 * It will provide suggestions for the phrase that is being currently typed by
 * the user.
 *
 * This is a wrapper around @tarekraafat/autocomplete.js.
 */
class ProductSearchSuggestor {
  constructor(autoComplete, $el) {
    this.autoComplete = autoComplete;
    this.$el = $el;
    this.$form = $el.querySelector(".query-search__form");
    this.productFilterLabels = JSON.parse(
      this.$form.dataset.productFilterLabels
    );
    this.searchUrl = this.$form.dataset.searchUrl;
    this.searchInputSelector = ".query-search__search-field";
    this.$searchInput = $el.querySelector(this.searchInputSelector);
    this.wildcardField = "wildcard";

    this.facetPattern = '[a-z_]+?:".*?"';
    this.operatorPattern = "( AND | OR | NOT )";
  }

  init() {
    this.setupAutoComplete();
  }

  getCurrentPhrase() {
    const currentValue = this.$searchInput.value;
    const caretPosition = this.$searchInput.selectionStart;

    return getCurrentPhrase(currentValue, caretPosition, [
      this.facetPattern,
      this.operatorPattern,
    ]);
  }

  getQuery() {
    const [currentPhrase, ,] = this.getCurrentPhrase();
    return currentPhrase;
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
    fieldCell.classList.add("query-search__suggest-results-key");
    const label = this.productFilterLabels[field];
    fieldCell.textContent = label;

    return fieldCell;
  }

  getValueCell(value, hasField) {
    const valueCell = document.createElement("td");
    valueCell.classList.add("query-search__suggest-results-value");
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
    const [, startIndex, endIndex] = this.getCurrentPhrase();

    const { field, value } = option.selection.value;
    let newValue;
    if (field === this.wildcardField) {
      newValue = `${value} `;
    } else {
      newValue = `${field}:"${value}" `;
    }

    this.$searchInput.setRangeText(newValue, startIndex, endIndex, "end");
    this.$searchInput.focus();
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
        className: "query-search__suggest-results",
      },
      resultItem: {
        element: "tr",
        className: "query-search__suggest-results-row",
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
    .querySelectorAll(".query-search")
    .forEach(($el) => new ProductSearchSuggestor(autoComplete, $el).init());
};

initProductSearchSuggestor();

export { ProductSearchSuggestor };
