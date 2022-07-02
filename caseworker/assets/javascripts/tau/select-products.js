class SelectProducts {
  constructor($checkboxes, products, onSelectProducts) {
    this.$checkboxes = $checkboxes;
    this.onSelectProducts = onSelectProducts;

    this.products = {};
    for (const product of products) {
      this.products[product.id] = product;
    }
  }

  init() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.addEventListener("input", () => {
        this.onSelectProducts(this.getSelectedProducts());
      });
    }
    this.onSelectProducts(this.getSelectedProducts());
  }

  getSelectedProducts() {
    let selectedProducts = [];
    for (const $checkbox of this.$checkboxes) {
      if (!$checkbox.checked) {
        continue;
      }
      const product = this.products[$checkbox.value];
      selectedProducts.push({
        name: product["name"],
        controlListEntries: product["control_list_entries"],
      });
    }
    return selectedProducts;
  }
}

export default SelectProducts;
