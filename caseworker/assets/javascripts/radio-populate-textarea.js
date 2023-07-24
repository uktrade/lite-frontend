class PopulateTextOnRadioInput {
  constructor($el) {
    this.$radioButtons = $el.querySelectorAll("input[type=radio]");
    this.$textArea = $el.querySelector("textarea");
    this.$lookup = JSON.parse(
      $el.querySelector(`#${this.$textArea.name}`).textContent
    );
  }

  init() {
    this.$radioButtons.forEach((input) => {
      input.addEventListener("change", () => {
        const text = this.$lookup[input.value];
        this.$textArea.value = text;
      });
    });
  }
}

export default function initRadioTextArea() {
  document
    .querySelectorAll("[data-module=radio-textarea]")
    .forEach(($el) => new PopulateTextOnRadioInput($el).init());
}

export { PopulateTextOnRadioInput, initRadioTextArea };
