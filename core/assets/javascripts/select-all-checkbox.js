import EventEmitter from "events";

class SelectAllCheckbox extends EventEmitter {
  constructor($checkbox, $label) {
    super();

    this.$checkbox = $checkbox;
    this.$label = $label;

    this.allSelected = false;
  }

  init() {
    this.render();

    this.$checkbox.addEventListener("change", () => this.handleInput());
  }

  render() {
    this.$label.textContent = this.allSelected ? "Deselect all" : "Select all";
    this.$checkbox.checked = this.allSelected;
  }

  setSelected(allSelected) {
    this.allSelected = allSelected;
    this.render();
  }

  handleInput() {
    this.emit("change", !this.allSelected);
  }
}

export default SelectAllCheckbox;
