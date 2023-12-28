class SelectedOptions {
  constructor($el, $multiSelect, multiSelectObjectsAsPlural) {
    this.$el = $el;
    this.$multiSelect = $multiSelect;
    this.multiSelectObjectsAsPlural = multiSelectObjectsAsPlural;
  }

  createContainer() {
    const $container = document.createElement("div");
    $container.ariaLive = "polite";
    $container.classList.add("selected-options");

    return $container;
  }

  init() {
    this.$container = this.createContainer();
    this.$el.appendChild(this.$container);

    this.render();
    this.setupListeners();
  }

  handleChange() {
    this.render();
  }

  setupListeners() {
    this.$multiSelect.addEventListener("change", () => this.handleChange());
  }

  createRemoveButton($option) {
    const $button = document.createElement("button");
    $button.textContent = "Remove";
    $button.classList.add("selected-options__option-remove");
    $button.addEventListener("click", () => {
      $option.selected = false;
      $option.dispatchEvent(new Event("change", { bubbles: true }));
    });

    return $button;
  }

  createListItem($option) {
    const $li = document.createElement("li");
    $li.classList.add("selected-options__option");

    const $span = document.createElement("span");
    $span.textContent = $option.textContent;
    $span.classList.add("selected-options__option-text");
    $li.appendChild($span);

    const $button = this.createRemoveButton($option);
    $li.appendChild($button);

    return $li;
  }

  createSelectedParagraph() {
    const $p = document.createElement("p");
    $p.textContent = `Selected ${this.multiSelectObjectsAsPlural}`;
    $p.classList.add("govuk-visually-hidden");

    return $p;
  }

  createList() {
    const $ul = document.createElement("ul");
    $ul.classList.add("selected-options__options");
    for (const option of this.$multiSelect.selectedOptions) {
      const $li = this.createListItem(option);
      $ul.appendChild($li);
    }

    return $ul;
  }

  hasSelectedItems() {
    return this.$multiSelect.selectedOptions.length > 0;
  }

  render() {
    this.$container.innerHTML = "";
    this.$container.classList.toggle(
      "selected-options--empty",
      !this.hasSelectedItems()
    );

    const $p = this.createSelectedParagraph();
    this.$container.appendChild($p);

    const $ul = this.createList();
    this.$container.appendChild($ul);
  }
}

export default SelectedOptions;
