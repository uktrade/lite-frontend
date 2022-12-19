class Headline {
  constructor($headline) {
    this.$headline = $headline;
  }

  getText(products) {
    if (products.length === 1) {
      const { name } = products[0];
      return `Assessing ${name}`;
    }
    return `Assessing ${products.length} products`;
  }

  setProducts(products) {
    this.$headline.textContent = this.getText(products);
  }
}

export default Headline;
