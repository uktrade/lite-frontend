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

  getSelectedProducts() {
    let selectedProducts = [];
    for (const $checkbox of this.$checkboxes) {
      if ($checkbox.checked) {
        selectedProducts.push({
          name: $checkbox.dataset["productName"],
        });
      }
    }
    return selectedProducts;
  }
}

export default SelectProducts;
