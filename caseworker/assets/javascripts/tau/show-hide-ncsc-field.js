class ShowHideNcscField {
  // Default NCSC form field is display: none;
  constructor(controlListEntriesSelector, ncscBox) {
    this.ncscBox = ncscBox;
    this.controlListEntriesSelector = controlListEntriesSelector;
  }

  // Methods
  showField() {
    this.ncscBox.style.display = "revert";
  }

  hideField() {
    this.ncscBox.style.display = "none";
  }

  toggleField() {
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );
    const { tokenfield } = $controlListEntries;

    if (tokenfield.getItems().some((string) => string.name.match(/ML/gm))) {
      this.showField();
    } else {
      this.hideField();
      this.ncscBox.querySelector("input").checked = false;
    }
  }

  setOnChangeListener() {
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );
    const { tokenfield } = $controlListEntries;
    tokenfield.on("change", () => {
      this.toggleField();
    });
  }

  hideFieldAtLoad() {
    this.toggleField();
  }
}

export default ShowHideNcscField;
