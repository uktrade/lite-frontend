class SelectedOptions {
  constructor($el, $multiSelect) {
    this.$el = $el;
    this.$multiSelect = $multiSelect;
  }

  init() {
    this.$ul = document.createElement("ul");
    this.$el.appendChild(this.$ul);

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
    this.$ul.innerHTML = "";

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

      this.$ul.appendChild(li);
    }
  }
}

export default SelectedOptions;
