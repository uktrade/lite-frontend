class SelectedOptions {
  constructor($el, $multiSelect, multiSelectObjectsAsPlural) {
    this.$el = $el;
    this.$multiSelect = $multiSelect;
    this.multiSelectObjectsAsPlural = multiSelectObjectsAsPlural;

    this.fakeOption = null;
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
    this.fakeOption = null;
    this.render();
  }

  setupListeners() {
    this.$multiSelect.addEventListener("change", () => this.handleChange());
  }

  createRemoveButton(onRemove) {
    const $iconDiv = document.createElement("div");
    $iconDiv.classList = "selected-options__option-remove-icon";
    $iconDiv.ariaHidden = true;
    $iconDiv.textContent = "×";

    const $textNode = document.createTextNode("Remove");

    const $button = document.createElement("button");
    $button.appendChild($iconDiv);
    $button.appendChild($textNode);

    $button.classList.add("selected-options__option-remove");
    $button.addEventListener("click", () => onRemove());

    return $button;
  }

  createListItem(text, onRemove) {
    const $li = document.createElement("li");
    $li.classList.add("selected-options__option");

    const $span = document.createElement("span");
    $span.textContent = text;
    $span.classList.add("selected-options__option-text");
    $li.appendChild($span);

    const $button = this.createRemoveButton(onRemove);
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

    for (const $option of this.$multiSelect.selectedOptions) {
      const $li = this.createListItem($option.textContent, () => {
        $option.selected = false;
        $option.dispatchEvent(new Event("change", { bubbles: true }));
      });
      $ul.appendChild($li);
    }

    if (this.fakeOption) {
      const [text, onRemove] = this.fakeOption;
      const $li = this.createListItem(text, () => {
        onRemove();
        this.fakeOption = null;
        this.render();
      });
      $ul.appendChild($li);
    }

    return $ul;
  }

  hasSelectedItems() {
    return this.$multiSelect.selectedOptions.length > 0 || this.fakeOption;
  }

  setFakeOption(text, onRemove) {
    this.fakeOption = [text, onRemove];
    this.render();
  }

  resetFakeOption() {
    this.fakeOption = null;
    this.render();
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
