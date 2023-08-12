import EventEmitter from "events";

class SelectAllCheckboxes extends EventEmitter {
  constructor($checkboxes) {
    super();

    this.$checkboxes = $checkboxes;

    this.isAllSelected = null;
  }

  init() {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.addEventListener("change", () => this.setSelectAll());
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
      this.emit("change", isAllSelected);
      this.isAllSelected = isAllSelected;
    }
  }

  selectAll(selectAll) {
    for (const $checkbox of this.$checkboxes) {
      $checkbox.checked = selectAll;
      $checkbox.dispatchEvent(new Event("change"));
      $checkbox.dispatchEvent(new Event("input"));
    }
  }
}

export default SelectAllCheckboxes;
