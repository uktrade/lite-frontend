class TableExpander {
  constructor($element) {
    this.$element = $element;
    this.$showMoreCasesTableBody = this.$element.querySelector(
      ".table-expander__show-more-cases-table-body"
    );
    this.$remainingHits = this.$element.querySelector(
      ".table-expander__remaining-hits"
    );
  }

  init() {
    this.hideTableBody();
    this.createShowMoreCasesLink();
  }

  hideTableBody() {
    this.$remainingHits.classList.add("table-expander__remaining-hits__hidden");
    this.$remainingHits.setAttribute("aria-hidden", "false");
  }

  createShowMoreCasesLink() {
    this.$showMoreCasesLink = this.$element.querySelector(
      ".table-expander__show-more-cases-link"
    );
    this.$showMoreCasesLink.addEventListener("click", (event) =>
      this.handleShowMoreCasesLinkClick(event)
    );
  }

  showRemainingHits() {
    this.$remainingHits.classList.remove(
      "table-expander__remaining-hits__hidden"
    );
    this.$remainingHits.classList.add(
      "table-expander__remaining-hits__animate"
    );
    this.$showMoreCasesTableBody.classList.add(
      "table-expander__show-more-cases-table-body__hidden"
    );
  }

  handleShowMoreCasesLinkClick(event) {
    event.preventDefault();
    this.showRemainingHits();
    this.$showMoreCasesLink.remove();
  }
}

const initTableExpanders = () => {
  document
    .querySelectorAll(".table-expander")
    .forEach(($element) => new TableExpander($element).init());
};

export { initTableExpanders, TableExpander };
