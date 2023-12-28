import EventEmitter from "events";

class SelectProducts extends EventEmitter {
  constructor($checkboxes, products) {
    super();

    this.$checkboxes = $checkboxes;
    this.products = {};
    for (const product of products) {
      this.products[product.id] = product;
    }
  }

  init() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.addEventListener("input", () => {
        this.emit("change", this.getSelectedProducts());
      });
    }
    this.emit("change", this.getSelectedProducts());
  }

  getSelectedProducts() {
    let selectedProducts = [];
    for (const $checkbox of this.$checkboxes) {
      if (!$checkbox.checked) {
        continue;
      }
      selectedProducts.push(this.products[$checkbox.value]);
    }
    return selectedProducts;
  }
}

export default SelectProducts;
