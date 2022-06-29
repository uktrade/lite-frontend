export const SELECT_ALL_BUTTON_TEXT = "Select all";
export const DESELECT_ALL_BUTTON_TEXT = "Deselect all";

class SelectAll {
  constructor($selectAllButton, $checkboxes) {
    this.$selectAllButton = $selectAllButton;
    this.$checkboxes = $checkboxes;

    this.isAllSelected = false;
  }

  init() {
    this.$selectAllButton.addEventListener("click", (evt) =>
      this.handleSelectAllButtonClick(evt)
    );
    this.$checkboxes.forEach(($checkbox) => {
      $checkbox.addEventListener("input", () => this.setSelectAll());
    });
    this.setSelectAll();
  }

  handleSelectAllButtonClick(evt) {
    evt.preventDefault();
    this.setCheckboxesChecked(!this.isAllSelected);
  }

  setCheckboxesChecked(checked) {
    this.$checkboxes.forEach(($checkbox) => {
      $checkbox.checked = checked;
      $checkbox.dispatchEvent(new Event("input"));
    });
  }

  getNumChecked() {
    return [...this.$checkboxes].reduce((previousValue, checkbox) => {
      return (previousValue += checkbox.checked ? 1 : 0);
    }, 0);
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
