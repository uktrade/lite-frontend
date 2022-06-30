class Headline {
  constructor($headline) {
    this.$headline = $headline;
  }

  getText(products) {
    if (products.length === 1) {
      const product = products[0];
      return `Assessing ${product["name"]}`;
    }
    return `Assessing ${products.length} products`;
  }

  setProducts(products) {
    this.$headline.textContent = this.getText(products);
  }
}

export default Headline;
