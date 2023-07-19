class PopulateTextOnRadioInput {
  constructor($el) {
    this.$radio_buttons = $el.querySelectorAll("input[type=radio]");
    this.$text_area = $el.querySelector("textarea");
    this.$lookup = JSON.parse(
      $el.querySelector(`#${this.$text_area.name}`).textContent
    );
  }

  init() {
    this.$radio_buttons.forEach((input) => {
      input.addEventListener("change", () => {
        const text = this.$lookup[input.value];
        this.$text_area.value = text;
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
