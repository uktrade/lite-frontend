class CLESuggestions {
  constructor($suggestionsContainer, onSelectSuggestions) {
    this.$suggestionsContainer = $suggestionsContainer;
    this.onSelectSuggestions = onSelectSuggestions;
  }

  getSuggestionButton(suggestion) {
    const ratings = suggestion.map((s) => s.rating);
    const cleSuggestionButton = document.createElement("button");
    cleSuggestionButton.classList.add("lite-button--link");
    cleSuggestionButton.textContent = `Select exporter suggestion ${ratings.join(
      ", "
    )}`;
    return cleSuggestionButton;
  }

  getSuggestionKey(controlListEntries) {
    return controlListEntries
      .map(({ id }) => id)
      .sort()
      .join("|");
  }

  getSuggestions(products) {
    const suggestions = [];
    const seenSuggestions = new Set();
    for (const { controlListEntries } of products) {
      const exporterControlListEntries = controlListEntries.exporter;
      if (exporterControlListEntries.length === 0) {
        continue;
      }
      const suggestionKey = this.getSuggestionKey(exporterControlListEntries);
      if (seenSuggestions.has(suggestionKey)) {
        continue;
      }
      seenSuggestions.add(suggestionKey);
      suggestions.push(exporterControlListEntries);
    }
    return suggestions;
  }

  setProducts(products) {
    this.$suggestionsContainer.innerHTML = "";

    const suggestions = this.getSuggestions(products);
    for (const suggestion of suggestions) {
      const cleSuggestionButton = this.getSuggestionButton(suggestion);
      cleSuggestionButton.addEventListener("click", (evt) =>
        this.handleSuggestionButtonClick(evt, suggestion)
      );
      this.$suggestionsContainer.append(cleSuggestionButton);
    }
  }

  handleSuggestionButtonClick(evt, suggestion) {
    evt.preventDefault();
    this.onSelectSuggestions(suggestion);
  }
}

export default CLESuggestions;
