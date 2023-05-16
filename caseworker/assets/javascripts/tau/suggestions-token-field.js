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
    const { tokenfield } = $controlListEntries;
    tokenfield.addItems(
      suggestions.map((rating) => ({
        id: rating,
        name: rating,
      }))
    );
  }
}

export default SuggestionsTokenField;
