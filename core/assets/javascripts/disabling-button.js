class DisablingButton {
  constructor($button) {
    this.$button = $button;
  }

  init() {
    this.$button.addEventListener("click", (evt) => this.handleClick(evt));
  }

  handleClick() {
    // Immediately setting the button to disabled stops any forms from being
    // submitted so we push this onto the stack for the next cycle to let the
    // form submit but then we disable the button
    setTimeout(() => (this.$button.disabled = true), 0);
  }
}

const initDisablingButton = () => {
  document
    .querySelectorAll("[data-module=disabling-button]")
    .forEach(($el) => new DisablingButton($el).init());
};

export default DisablingButton;
export { initDisablingButton };
