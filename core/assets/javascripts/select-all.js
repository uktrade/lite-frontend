export const SELECT_ALL_BUTTON_TEXT = "Select all";
export const DESELECT_ALL_BUTTON_TEXT = "Deselect all";

class SelectAll {
  constructor($checkboxes, $selectAllButton) {
    this.$checkboxes = $checkboxes;
    this.$selectAllButton = $selectAllButton;

    this.isAllSelected = false;
  }

  init() {
    this.$selectAllButton.addEventListener("click", (evt) =>
      this.handleSelectAllButtonClick(evt)
    );
    for (const $checkbox of this.$checkboxes) {
      $checkbox.addEventListener("input", () => this.setSelectAll());
    }
    this.setSelectAll();
  }

  handleSelectAllButtonClick(evt) {
    evt.preventDefault();
    this.setCheckboxesChecked(!this.isAllSelected);
  }

  setCheckboxesChecked(checked) {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.checked = checked;
      $checkbox.dispatchEvent(new Event("input"));
    }
  }

  getNumChecked() {
    let numChecked = 0;
    for (const $checkbox of this.$checkboxes) {
      numChecked += $checkbox.checked ? 1 : 0;
    }
    return numChecked;
  }

  setSelectAll() {
    if (this.getNumChecked() === this.$checkboxes.length) {
      this.$selectAllButton.textContent = DESELECT_ALL_BUTTON_TEXT;
      this.isAllSelected = true;
    } else {
      this.$selectAllButton.textContent = SELECT_ALL_BUTTON_TEXT;
      this.isAllSelected = false;
    }
  }
}

export default SelectAll;
