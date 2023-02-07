class ListExpander {
  constructor($el) {
    this.$el = $el;
    this.$list = this.$el.querySelector(".expander__expand-list");
    this.liElems = this.$list.querySelectorAll(".expander__expand-list__item");
    this.visibleElems = parseInt(
      this.$el.getAttribute("data-expander-visible-elems"),
      10
    );
  }

  init() {
    if (this.liElems.length <= this.visibleElems) {
      return;
    }
    this.hideListElems();
    this.createExpandButton();
  }

  hideListElems() {
    this.liElems.forEach(($li, currentIndex, listObj) => {
      if (currentIndex < this.visibleElems) {
        return;
      }
      $li.classList.add("expander__expand-list__item__hidden");
    });
  }

  createExpandButton() {
    this.$el.insertAdjacentHTML(
      "beforeend",
      `<button class="expander__expand-button" type="button" aria-label="Show more"></button>`
    );
    this.$expandButton = this.$el.querySelector(".expander__expand-button");
    this.$expandButton.innerHTML =
      `<span>` + this.visibleElems + ` of ` + this.liElems.length + `</span>`;
    this.$expandButton.addEventListener("click", (evt) =>
      this.handleExpandButtonClick(evt)
    );
  }

  showListElems() {
    this.liElems.forEach(($li, currentIndex, listObj) => {
      if (currentIndex < this.visibleElems) {
        return;
      }
      $li.classList.remove("expander__expand-list__item__hidden");
      $li.classList.add("expander__expand-list__item__animate");
    });
  }

  handleExpandButtonClick(evt) {
    evt.preventDefault();
    this.showListElems();
    this.$expandButton.remove();
  }
}

const initExpanders = () => {
  document
    .querySelectorAll(".expander")
    .forEach(($el) => new ListExpander($el).init());
};

export { initExpanders, ListExpander };
