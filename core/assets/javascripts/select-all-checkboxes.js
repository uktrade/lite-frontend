class SelectAllCheckboxes {
  constructor($checkboxes, allSelectedCallback) {
    this.$checkboxes = $checkboxes;
    this.allSelectedCallback = allSelectedCallback;

    this.isAllSelected = null;
  }

  init() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.addEventListener("input", () => this.setSelectAll());
    }
    this.setSelectAll();
  }

  getNumChecked() {
    let numChecked = 0;
    for (const $checkbox of this.$checkboxes) {
      numChecked += $checkbox.checked ? 1 : 0;
    }
    return numChecked;
  }

  setSelectAll() {
    const isAllSelected = this.getNumChecked() === this.$checkboxes.length;
    if (this.isAllSelected !== isAllSelected) {
      this.allSelectedCallback(isAllSelected);
      this.isAllSelected = isAllSelected;
    }
  }

  selectAll() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.checked = true;
      $checkbox.dispatchEvent(new Event("input"));
    }
  }

  deselectAll() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.checked = false;
      $checkbox.dispatchEvent(new Event("input"));
    }
  }
}

export default SelectAllCheckboxes;
