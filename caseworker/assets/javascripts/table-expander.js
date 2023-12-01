class TableExpander {
  constructor($element) {
    this.$element = $element;
    this.$distinctHits = this.$element.querySelector(
      ".table-expander__distinct-hits"
    );
    this.$remainingHits = this.$element.querySelector(
      ".table-expander__remaining-hits"
    );
  }

  init() {
    this.hideRemainingHitsTableBody();
    this.createShowMoreCasesButton();
  }

  hideRemainingHitsTableBody() {
    this.$remainingHits.classList.add("table-expander__remaining-hits__hidden");
    this.$remainingHits.setAttribute("aria-hidden", "false");
  }

  getNumCols() {
    this.$head = this.$element.querySelector(".govuk-table__head");
    this.$headRow = this.$head.querySelector(".govuk-table__row");
    const numCols = this.$headRow.querySelectorAll(
      ".govuk-table__header"
    ).length;
    return numCols;
  }

  createShowMoreCasesButton() {
    const numCols = this.getNumCols();
    this.$distinctHits.insertAdjacentHTML(
      "afterend",
      `<tbody class="govuk-table__body table-expander__show-more-cases-table-body"><tr class="govuk-table__row"><td class="govuk-table__cell govuk-body" colspan="` +
        numCols +
        `"><button class="table-expander__show-more-cases-button lite-button--link">+ Show more cases for this product</button></td></tr></tbody>`
    );

    this.$showMoreCasesTableBody = this.$element.querySelector(
      ".table-expander__show-more-cases-table-body"
    );

    this.$showMoreCasesButton = this.$element.querySelector(
      ".table-expander__show-more-cases-button"
    );

    this.$showMoreCasesButton.addEventListener("click", (event) =>
      this.handleShowMoreCasesButtonClick(event)
    );
  }

  showRemainingHits() {
    this.$remainingHits.classList.remove(
      "table-expander__remaining-hits__hidden"
    );
    this.$showMoreCasesTableBody.classList.add(
      "table-expander__show-more-cases-table-body__hidden"
    );
  }

  handleShowMoreCasesButtonClick(event) {
    event.preventDefault();
    this.showRemainingHits();
    this.$showMoreCasesButton.remove();
  }
}

const initTableExpanders = () => {
  document
    .querySelectorAll(".table-expander")
    .forEach(($element) => new TableExpander($element).init());
};

export { initTableExpanders, TableExpander };
