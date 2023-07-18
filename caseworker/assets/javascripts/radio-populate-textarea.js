class PopulateTextOnRadioInput {
  constructor($radio_selector, $text_selector, $lookup) {
    this.$radio_buttons = document.querySelectorAll($radio_selector);
    this.$text_area = document.querySelector($text_selector);
    this.$lookup = $lookup;
  }

  init() {
    this.$radio_buttons.forEach((input) => {
      input.addEventListener("change", (event) => {
        const text = this.$lookup[input];
        this.$text_area.value = text;
      });
    });
  }
}

export { PopulateTextOnRadioInput };
