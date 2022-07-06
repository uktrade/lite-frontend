class CheckboxClassToggler {
  constructor($checkboxes, $elementToToggleClass, toggleClass) {
    this.$checkboxes = $checkboxes;
    this.$elementToToggleClass = $elementToToggleClass;
    this.toggleClass = toggleClass;
  }

  init() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.addEventListener("input", (evt) =>
        this.handleCheckboxInput(evt)
      );
    }
    this.setClass();
  }

  handleCheckboxInput() {
    this.setClass();
  }

  getNumChecked() {
    let numChecked = 0;
    for (const $checkbox of this.$checkboxes) {
      numChecked += $checkbox.checked ? 1 : 0;
    }
    return numChecked;
  }

  setClass() {
    const shouldHaveClass = this.getNumChecked() === 0;

    this.$elementToToggleClass.classList.toggle(
      this.toggleClass,
      shouldHaveClass
    );
  }
}

export default CheckboxClassToggler;
