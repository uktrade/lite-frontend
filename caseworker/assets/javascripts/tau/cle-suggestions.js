import EventEmitter from "events";

class UniqueSuggestionsCollector {
  constructor() {
    this.suggestions = [];
    this.seenExporterSuggestions = new Set();
    this.seenAssessedSuggestions = new Set();
  }

  getSuggestionKey(suggestion) {
    return suggestion.sort().join("|");
  }

  addSuggestion(suggestionSet, suggestion, suggestionText) {
    const suggestionKey = this.getSuggestionKey(suggestion);
    if (suggestionSet.has(suggestionKey)) {
      return;
    }
    suggestionSet.add(suggestionKey);
    this.suggestions.push([suggestion, suggestionText]);
  }

  addExporterSuggestion(exporterSuggestion, exporterSuggestionText) {
    this.addSuggestion(
      this.seenExporterSuggestions,
      exporterSuggestion,
      exporterSuggestionText
    );
  }

  addAssessedSuggestion(assessedSuggestion, assessedSuggestionText) {
    this.addSuggestion(
      this.seenAssessedSuggestions,
      assessedSuggestion,
      assessedSuggestionText
    );
  }
}

class CLESuggestions extends EventEmitter {
  constructor($suggestionsContainer) {
    super();
    this.$suggestionsContainer = $suggestionsContainer;
  }

  getSuggestionButton(suggestionText) {
    const cleSuggestionButton = document.createElement("button");
    cleSuggestionButton.classList.add("lite-button--link");
    cleSuggestionButton.textContent = suggestionText;
    return cleSuggestionButton;
  }

  getSuggestionText(suggestion) {
    return suggestion.join(", ");
  }

  getExporterSuggestionText(suggestion) {
    const suggestionText = this.getSuggestionText(suggestion);
    return `Select exporter suggestion ${suggestionText}`;
  }

  getAssessedSuggestionText(suggestion) {
    const suggestionText = this.getSuggestionText(suggestion);
    return `Copy previous assessment ${suggestionText}`;
  }

  getSuggestions(products) {
    const uniqueSuggestionsCollector = new UniqueSuggestionsCollector();

    for (const { controlListEntries } of products) {
      const { exporter: exporterSuggestion, precedents: assessedSuggestions } =
        controlListEntries;

      if (exporterSuggestion && exporterSuggestion.length > 0) {
        uniqueSuggestionsCollector.addExporterSuggestion(
          exporterSuggestion,
          this.getExporterSuggestionText(exporterSuggestion)
        );
      }

      if (assessedSuggestions) {
        for (const assessedSuggestion of assessedSuggestions) {
          if (!assessedSuggestion.length) {
            continue;
          }
          uniqueSuggestionsCollector.addAssessedSuggestion(
            assessedSuggestion,
            this.getAssessedSuggestionText(assessedSuggestion)
          );
        }
      }
    }
    return uniqueSuggestionsCollector.suggestions;
  }

  setProducts(products) {
    this.$suggestionsContainer.innerHTML = "";

    const suggestions = this.getSuggestions(products);
    for (const [suggestion, suggestionText] of suggestions) {
      const cleSuggestionButton = this.getSuggestionButton(suggestionText);
      cleSuggestionButton.addEventListener("click", (evt) =>
        this.handleSuggestionButtonClick(evt, suggestion)
      );
      this.$suggestionsContainer.append(cleSuggestionButton);
    }
  }

  handleSuggestionButtonClick(evt, suggestion) {
    evt.preventDefault();
    this.emit("change", suggestion);
  }
}

export default CLESuggestions;
