class NoSuggestionsTokenField {
  constructor(controlListEntriesSelector, $noControlListCheckbox) {
    this.controlListEntriesSelector = controlListEntriesSelector;
    this.$noControlListCheckbox = $noControlListCheckbox;
  }

  init() {
    this.$noControlListCheckbox.addEventListener("input", (evt) =>
      this.handleNoControlListCheckboxInput(evt)
    );
  }

  emptyTokenField() {
    // We have to load this here instead of the constructor as originally this will be a multiselect that will get
    // switched out for a tokenset field and so we need to defer doing the setting until then
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );
    const { tokenfield } = $controlListEntries;
    tokenfield.emptyItems();
  }

  displayNoCLEEntry() {
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );

    const $tokenFieldInput =
      $controlListEntries.querySelector(".tokenfield-input");
    $tokenFieldInput.style.display = "none";

    const $notListedSuggestionField =
      $controlListEntries.querySelector(".tokenfield-set ul");
    const newLi = document.createElement("li");
    newLi.classList.add("tokenfield-set-item", "tau-none-item");

    const newSpan = document.createElement("span");
    newSpan.classList.add("item-label");
    newSpan.innerText = "None";

    const newHref = document.createElement("a");
    newHref.classList.add("item-remove");
    newHref.tabIndex = -1;
    newHref.innerText = "×";
    newHref.addEventListener("click", () => {
      this.setCheckbox(false);
    });

    newLi.append(newSpan, newHref);
    $notListedSuggestionField.appendChild(newLi);
  }

  removeNoCLEEntry() {
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );

    const $tokenFieldInput =
      $controlListEntries.querySelector(".tokenfield-input");
    $tokenFieldInput.style.removeProperty("display");

    const $notListedSuggestionItem = $controlListEntries.querySelector(
      ".tokenfield-set .tau-none-item"
    );
    $notListedSuggestionItem?.remove();
  }

  handleNoControlListCheckboxInput() {
    const { checked } = this.$noControlListCheckbox;
    if (checked) {
      this.emptyTokenField();
      this.displayNoCLEEntry();
    } else {
      this.removeNoCLEEntry();
    }
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
