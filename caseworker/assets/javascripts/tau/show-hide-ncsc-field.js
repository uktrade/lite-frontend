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

  getTokenfield() {
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );
    const { tokenfield } = $controlListEntries;
    return tokenfield;
  }

  toggleField() {
    const tokenfield = this.getTokenfield();

    if (tokenfield.getItems().some((string) => string.name.startsWith("ML"))) {
      this.showField();
    } else {
      this.hideField();
      this.ncscBox.querySelector("input").checked = false;
    }
  }

  setOnChangeListener() {
    const tokenfield = this.getTokenfield();

    tokenfield.on("change", () => {
      this.toggleField();
    });
  }

  hideFieldAtLoad() {
    this.toggleField();
  }
}

export default ShowHideNcscField;
