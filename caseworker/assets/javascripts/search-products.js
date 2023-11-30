import "url-search-params-polyfill";
import "fetch-polyfill";
import autoComplete from "@tarekraafat/autocomplete.js";



class ProductSearchSuggestor {

  constructor($el) {
    this.$el = $el;
    this.inputElement = document.getElementById("id_search_string");
    this.pageInputElement = document.getElementById("id_page");
    this.searchButtonElement = document.getElementById("submit-id-submit");
    this.resultsElement = document.getElementById("results-table");
    this.suggestionsInfo = document.getElementById("suggestions-info");
    this.currentSearch = this.inputElement.value || "";
    this.lastSearch = this.inputElement.value || "";
    this.searchPrefix = ""; // string for which we retrieve suggestions

    this.productSuggestUrl = "/search/products/suggest/?format=json&q="

    this.threshold = 1;  // default in autoComplete.js
    this.maxSuggestions = 10;
  }

  init() {
    this.prepareSearchInput(this.inputElement);
    this.setupAutoComplete(this);
  }

  prepareSearchInput(inputElement) {
    // focus at end of the field and make sure there is a space at the end
    inputElement.focus();
    if (!/ $/.test(inputElement.value)) {
      inputElement.value = inputElement.value + " ";
    }
    inputElement.setSelectionRange(
      inputElement.value.length,
      inputElement.value.length
    );
  }

  getProductSuggestionsUrl(search_prefix) {
    const url = this.productSuggestUrl + escape(search_prefix.trim());

    console.log(url);
    return url;
  }

  replaceCharAt(str, index, c) {
    if (index > str.length) {
      return str;
    }

    return str.substring(0, index) + c + str.substring(index + 1);
  }

  stripMatchingCharsAtStart(referenceString, targetString) {
    /*
     * Replaces all matching characters at the beginning with spaces
     * using the referenceString as reference
     */
    var i = 0;
    var j = 0;
    var stripped = targetString;

    if (referenceString.length === 0) {
      return targetString;
    }

    const maxLength = referenceString.length > targetString.length
      ? targetString.length : referenceString.length;

    while (i < maxLength) {
      if (referenceString[i] == targetString[i]) {
        stripped = this.replaceCharAt(stripped, i, " ");
        i++;
        continue;
      }
      break;
    }

    return stripped.trim();
  }

  stripMatchingCharsAtEnd(referenceString, targetString) {
    var i = referenceString.length - 1;
    var j = targetString.length - 1
    var stripped = targetString;

    if (referenceString.length === 0) {
      return targetString;
    }

    while (i > 0) {
      if (referenceString[i] == targetString[j]) {
        stripped = this.replaceCharAt(stripped, j, " ");
        i--;
        j--;
        continue;
      }
      break;
    }

    return stripped.trim();
  }

  getSearchPrefix(lastSearch, currentSearchString) {
    /*
     * Using the current search string entered in the input field and comparing
     * with the last submitted search string it determines what additional characters
     * user is currently typing and retrieves suggestions for that.
     */
    lastSearch = lastSearch.trim();
    currentSearchString = currentSearchString.trim();

    if (lastSearch.length === 0) {
      return currentSearchString;
    }

    console.log(`lastSearch: ${lastSearch}`);
    console.log(`currentSearchString: ${currentSearchString}`);

    const tokens = lastSearch.split(" ");
    let start = tokens[0];
    let end = tokens[tokens.length - 1];

    const matchesAtStart = currentSearchString.startsWith(start);
    const matchesAtEnd = currentSearchString.endsWith(end);

    var stripped = `${currentSearchString}`;  // copy

    if (matchesAtStart && matchesAtEnd) {
      // User entered new chars in between
      stripped = this.stripMatchingCharsAtStart(lastSearch, currentSearchString);
      stripped = this.stripMatchingCharsAtEnd(lastSearch, stripped);
    } else if (matchesAtStart) {
      // User editing at the end
      stripped = this.stripMatchingCharsAtStart(lastSearch, currentSearchString);
    } else if (matchesAtEnd) {
      // User editing at the start
      stripped = this.stripMatchingCharsAtEnd(lastSearch, currentSearchString);
    }

    var searchPrefix = stripped.trim();

    /*
     * If user entered multiple words then use last word.
     * If we are seeing multiple words then it means user has not selected
     * suggestions offered for the first word. If we consider both words then
     * it is unlikely to receive any suggestions for that phrase.
     * It is also possible that the first word could be an operator (AND, OR, NOT etc)
     */
    const prefixTokens = searchPrefix.split(" ");
    searchPrefix = prefixTokens[prefixTokens.length - 1];
    
    console.log(`=> searchPrefix: ${searchPrefix}`);

    return searchPrefix;
  }

  triggerSearch() {
    var inputElement = document.getElementById("id_search_string");
    var lastSearch = inputElement.value || "";
    var query = (lastSearch = inputElement.value);
    var pageNumber = 1;

    setTimeout(function () {
      inputElement.focus();
    });

    var searchParams = new URLSearchParams(window.location.search);
    searchParams.set("search_string", query);
    searchParams.set("page", pageNumber);

    this.searchButtonElement.click();

    history.pushState(
      null,
      "",
      window.location.pathname + "?" + searchParams.toString()
    );
  }

  setupAutoComplete(suggestor) {

    var autocomplete = new autoComplete({
      trigger: {
        event: ["input"],
        condition: function (query) {
          return query.length > autocomplete.threshold && query !== " ";
        },
      },
      data: {
        src: function () {
          const searchPrefix = suggestor.getSearchPrefix(suggestor.lastSearch, suggestor.inputElement.value);
          suggestor.searchPrefix = searchPrefix;

          var suggestUrl = suggestor.getProductSuggestionsUrl(searchPrefix);

          return fetch(suggestUrl)
            .then(function (response) {
              return response.json().then(function (parsed) {
                return parsed;
              });
            });
        },
        key: ["value"],
        cache: false,
      },
      selector: "#id_search_string",
      // threshold: 1,
      debounce: 300,
      resultsList: {
        render: true,
        element: "table",
        // when version 8 is released we can remove this: https://github.com/TarekRaafat/autoComplete.js/issues/105
        container: (source) => {
          source.setAttribute("id", "autoComplete_list");
          document
            .getElementById("id_search_string")
            .addEventListener("autoComplete", function (event) {
              function hideSearchResults() {
                var searchResults = document.getElementById("autoComplete_list");
                while (searchResults.firstChild) {
                  searchResults.removeChild(searchResults.firstChild);
                }
                document.removeEventListener("click", hideSearchResults);
              }
              document.addEventListener("click", hideSearchResults);
            });
        },
      },
      resultItem: {
        content: function (data, source) {
          var value = data.value.value.replace(/\s/g, " ");
          var prefix = '<td class="autoCompleteResultFieldName">' +
            data.value.field.replace(/_/g, " ") + "</td>";
          source.innerHTML = prefix + "<td>" + value + "</td>";
        },
        element: "tr",
      },
      searchEngine: function (query, record) {
        return record;
      },
      maxResults: suggestor.maxSuggestions,
      onSelection: function (option) {
        var appendValue = `${option.selection.value.field}:"${option.selection.value.value}"`
        suggestor.inputElement.value = suggestor.inputElement.value.replace(suggestor.searchPrefix, appendValue);
        suggestor.lastSearch = suggestor.inputElement.value;
        suggestor.inputElement.value = suggestor.inputElement.value + " ";
        console.log(`inputElement: ${suggestor.inputElement.value}`);
        console.log(`lastSearch: ${suggestor.lastSearch}`);
        console.log(`diff: ${suggestor.searchPrefix}`);

        suggestor.triggerSearch();
      },
    });
  }
}


const initProductSearchSuggestor = () => {
  document
    .querySelectorAll(".product-search")
    .forEach(($el) => new ProductSearchSuggestor($el).init());
};

initProductSearchSuggestor();
