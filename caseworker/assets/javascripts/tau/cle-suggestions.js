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

  getSuggestions(products) {
    const suggestions = [];
    const seenSuggestions = new Set();
    for (const product of products) {
      const controlListEntries = product.controlListEntries;
      if (controlListEntries.length === 0) {
        continue;
      }
      const suggestionKey = controlListEntries
        .map((entry) => entry.id)
        .sort()
        .join("|");
      if (seenSuggestions.has(suggestionKey)) {
        continue;
      }
      seenSuggestions.add(suggestionKey);

      const suggestion = controlListEntries;
      suggestions.push(suggestion);
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
