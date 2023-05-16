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

  setOnChangeListener() {
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );
    const { tokenfield } = $controlListEntries;
    tokenfield.on("change", (event) => {
      if (event.getItems().some((string) => string.name.match(/ML/gm))) {
        this.showField();
      } else {
        this.hideField();
      }
    });
  }

  hideFieldAtLoad() {
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );
    const { tokenfield } = $controlListEntries;

    if (
      tokenfield
        .showSuggestions()
        .getItems()
        .some((string) => string.name.match(/ML/gm))
    ) {
      this.showField();
    }
  }
}

export default ShowHideNcscField;
