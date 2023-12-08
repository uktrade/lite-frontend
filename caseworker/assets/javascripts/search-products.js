import autoComplete from "@tarekraafat/autocomplete.js";

class ProductSearchSuggestor {
  constructor($el) {
    this.$el = $el;
    this.searchInputSelector = ".product-search__search-field";
  }

  init() {
    this.setupAutoComplete();
  }

  dataSource() {
    return Promise.resolve([
      {
        field: "consignee_country",
        value: "Country",
      },
      {
        field: "assessment_note",
        value:
          "Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country Country ",
      },
      {
        field: "consignee_country",
        value: "Country",
      },
      {
        field: "consignee_country",
        value: "Country",
      },
      {
        field: "name",
        value: "Cathy",
      },
      {
        field: "name",
        value: "Billy",
      },
    ]);
  }

  renderItem(data, source) {
    source.innerHTML = "";

    const keyCell = document.createElement("td");
    keyCell.classList.add("product-search__suggest-results-key");
    keyCell.textContent = data.value.field;
    source.appendChild(keyCell);

    const valueCell = document.createElement("td");
    valueCell.classList.add("product-search__suggest-results-value");
    valueCell.textContent = data.value.value;
    source.appendChild(valueCell);
  }

  setupAutoComplete() {
    new autoComplete({
      selector: this.searchInputSelector,
      data: {
        src: () => this.dataSource(),
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
