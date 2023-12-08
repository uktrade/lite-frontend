import autoComplete from "@tarekraafat/autocomplete.js";

class ProductSearchSuggestor {
  constructor($el) {
    this.$el = $el;
    this.$form = $el.querySelector(".product-search__form");
    this.productFilterLabels = JSON.parse(
      this.$form.dataset.productFilterLabels
    );
    this.searchUrl = this.$form.dataset.searchUrl;
    this.searchInputSelector = ".product-search__search-field";
    this.$searchInput = $el.querySelector(this.searchInputSelector);
  }

  init() {
    this.setupAutoComplete();
  }

  getQuery() {
    return this.$searchInput.value;
  }

  async getSuggestions(query) {
    const url = `${this.searchUrl}?q=${query}`;
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

  renderItem(data, source) {
    source.innerHTML = "";

    let hasKey = false;
    if (data.value.field !== "wildcard") {
      const keyCell = document.createElement("td");
      keyCell.classList.add("product-search__suggest-results-key");
      const label = this.productFilterLabels[data.value.field];
      if (!label) {
        console.warning("No label for value", data.value.field);
      }
      keyCell.textContent = label;
      source.appendChild(keyCell);

      hasKey = true;
    }

    const valueCell = document.createElement("td");
    valueCell.classList.add("product-search__suggest-results-value");
    valueCell.textContent = data.value.value;
    if (!hasKey) {
      valueCell.colSpan = 2;
    }
    source.appendChild(valueCell);
  }

  handleSelection(option) {
    const { field, value } = option.selection.value;
    const newValue = `${field}:"${value}"`;
    const currentValue = this.$searchInput.value;
    this.$searchInput.value = `${currentValue} ${newValue}`;
  }

  setupAutoComplete() {
    new autoComplete({
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
    });
  }
}

const initProductSearchSuggestor = () => {
  document
    .querySelectorAll(".product-search")
    .forEach(($el) => new ProductSearchSuggestor($el).init());
};

initProductSearchSuggestor();

export { ProductSearchSuggestor };
