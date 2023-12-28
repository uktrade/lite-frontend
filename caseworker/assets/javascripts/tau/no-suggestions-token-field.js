import EventEmitter from "events";

class NoSuggestionsTokenField extends EventEmitter {
  constructor($noControlListCheckbox) {
    super();
    this.$noControlListCheckbox = $noControlListCheckbox;
  }

  init() {
    this.$noControlListCheckbox.addEventListener("input", (evt) =>
      this.handleNoControlListCheckboxInput(evt)
    );
  }

  handleNoControlListCheckboxInput() {
    const { checked } = this.$noControlListCheckbox;
    this.emit("change", checked);
  }

  setCheckbox(checked) {
    this.$noControlListCheckbox.checked = checked;
    this.$noControlListCheckbox.dispatchEvent(new Event("input"));
  }

  reset() {
    this.setCheckbox(false);
  }
}

export default NoSuggestionsTokenField;
