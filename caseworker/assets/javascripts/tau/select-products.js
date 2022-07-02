class SelectProducts {
  constructor($checkboxes, onSelectProducts) {
    this.$checkboxes = $checkboxes;
    this.onSelectProducts = onSelectProducts;
  }

  init() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.addEventListener("input", () => {
        this.onSelectProducts(this.getSelectedProducts());
      });
    }
    this.onSelectProducts(this.getSelectedProducts());
  }

  parseJSONFromElement(elementSelector) {
    const element = document.querySelector(elementSelector);
    return JSON.parse(element.textContent);
  }

  getSelectedProducts() {
    let selectedProducts = [];
    for (const $checkbox of this.$checkboxes) {
      if (!$checkbox.checked) {
        continue;
      }

      const scriptId = $checkbox.dataset["scriptId"];
      const name = this.parseJSONFromElement(`#${scriptId}-name`);
      const controlListEntries = this.parseJSONFromElement(
        `#${scriptId}-control-list-entries`
      );
      selectedProducts.push({ name, controlListEntries });
    }
    return selectedProducts;
  }
}

export default SelectProducts;
