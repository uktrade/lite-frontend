export const SHOW_ALL_BUTTON_TEXT = "Show all";
export const HIDE_ALL_BUTTON_TEXT = "Hide all";

export default class ExpandAll {
  constructor($expandAllButton, $details) {
    this.$expandAllButton = $expandAllButton;
    this.$details = $details;

    this.isAllExpanded = false;
  }

  init() {
    this.$expandAllButton.addEventListener("click", (evt) =>
      this.handleExpandAllButtonClick(evt)
    );
    for (const $detail of this.$details) {
      $detail.addEventListener("toggle", () => this.setExpandAll());
    }
    this.setExpandAll();
  }

  handleExpandAllButtonClick(evt) {
    evt.preventDefault();
    this.setDetailsOpen(!this.isAllExpanded);
  }

  setDetailsOpen(open) {
    for (const $detail of this.$details) {
      $detail.open = open;
      $detail.dispatchEvent(new Event("toggle"));
    }
  }

  getNumOpened() {
    let numOpened = 0;
    for (const $detail of this.$details) {
      numOpened += $detail.open ? 1 : 0;
    }
    return numOpened;
  }

  setExpandAll() {
    if (this.getNumOpened() === this.$details.length) {
      this.$expandAllButton.textContent = HIDE_ALL_BUTTON_TEXT;
      this.isAllExpanded = true;
    } else {
      this.$expandAllButton.textContent = SHOW_ALL_BUTTON_TEXT;
      this.isAllExpanded = false;
    }
  }
}
