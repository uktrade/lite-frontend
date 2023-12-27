class SelectedOptions {
  constructor($el, $multiSelect, multiSelectObjectsAsPlural) {
    this.$el = $el;
    this.$multiSelect = $multiSelect;
    this.multiSelectObjectsAsPlural = multiSelectObjectsAsPlural;
  }

  init() {
    this.$container = document.createElement("div");
    this.$container.ariaLive = "polite";

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

  render() {
    this.$container.innerHTML = "";

    const $p = document.createElement("p");
    $p.textContent = `Selected ${this.multiSelectObjectsAsPlural}`;
    $p.classList.add("govuk-visually-hidden");
    this.$container.appendChild($p);

    const $ul = document.createElement("ul");
    this.$container.appendChild($ul);

    for (const option of this.$multiSelect.selectedOptions) {
      const li = document.createElement("li");

      const span = document.createElement("span");
      span.textContent = option.textContent;
      li.appendChild(span);

      const button = document.createElement("button");
      button.textContent = "Remove";
      li.appendChild(button);
      button.addEventListener("click", () => {
        option.selected = false;
        option.dispatchEvent(new Event("change", { bubbles: true }));
      });

      $ul.appendChild(li);
    }
  }
}

export default SelectedOptions;
