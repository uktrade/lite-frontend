class SelectProducts {
  constructor($checkboxes, callback) {
    this.$checkboxes = $checkboxes;
    this.callback = callback;
  }

  init() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.addEventListener("input", () => {
        this.callback(this.getSelectedProducts());
      });
    }
    this.callback(this.getSelectedProducts());
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
