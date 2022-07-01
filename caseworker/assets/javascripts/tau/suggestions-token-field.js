class SuggestionsTokenField {
  constructor(controlListEntriesSelector) {
    this.controlListEntriesSelector = controlListEntriesSelector;
  }

  setSuggestions(suggestions) {
    // We have to load this here instead of the constructor as originally this will be a multiselect that will get
    // switched out for a tokenset field and so we need to defer doing the setting until then
    const $controlListEntries = document.querySelector(
      this.controlListEntriesSelector
    );
    const $tokenFieldInput =
      $controlListEntries.querySelector(".tokenfield-input");
    for (const suggestion of suggestions) {
      $tokenFieldInput.value = suggestion.rating;
      $tokenFieldInput.click();
      const $tokenFieldSuggestList = $controlListEntries.querySelector(
        ".tokenfield-suggest-item"
      );
      $tokenFieldSuggestList.click();
    }
  }
}

export default SuggestionsTokenField;
