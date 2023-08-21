import EventEmitter from "events";

class SelectAllButton extends EventEmitter {
  constructor($button) {
    super();
    this.$button = $button;

    this.allSelected = false;
  }

  init() {
    this.render();

    this.$button.addEventListener("click", (evt) => this.handleClick(evt));
  }

  render() {
    this.$button.textContent = this.allSelected ? "Deselect all" : "Select all";
  }

  setSelected(allSelected) {
    this.allSelected = allSelected;
    this.render();
  }

  handleClick(evt) {
    evt.preventDefault();
    this.emit("click", !this.allSelected);
  }
}

export default SelectAllButton;
