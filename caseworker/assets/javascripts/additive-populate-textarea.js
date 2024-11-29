class PopulateTextOnRadioInput {
  constructor($el) {
    this.$addButtons = $el.querySelectorAll("a[data-additive-key]");
    this.$textArea = $el.querySelector("textarea");
    this.$lookup = JSON.parse(
      $el.querySelector(`#${this.$textArea.name}`).textContent,
    );
  }

  init() {
    this.$addButtons.forEach((input) => {
      input.addEventListener("click", (event) => {
        event.preventDefault();
        const text = this.$lookup[input.getAttribute("data-additive-key")];
        if (this.$textArea.value == "") {
          this.$textArea.value = text;
        } else {
          this.$textArea.value = text + "\n\n--------\n" + this.$textArea.value;
        }
      });
    });
  }
}

export default function initAdditiveTextArea() {
  document
    .querySelectorAll("[data-module=additive-textarea]")
    .forEach(($el) => new PopulateTextOnRadioInput($el).init());
}

export { PopulateTextOnRadioInput, initAdditiveTextArea };
