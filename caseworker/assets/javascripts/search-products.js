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
    this.currentSearch = this.inputElement.value || "";
    this.lastSearch = this.inputElement.value || "";

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

  getProductSuggestionsUrl(query_string, search_prefix) {
    var url = this.productSuggestUrl + escape(query_string) + '&suggest=' + escape(search_prefix.trim());

    console.log(url);

    return url;
  }

  getDifference(lastSearch, currentSearchString) {
    /*
     * Returns the difference of these two strings which is used to get suggestions
     * User can either continuously select suggestions or add more search terms so
     * to correctly determine which term we need to use for suggestions determine
     * the difference of previous search with the current input data
     * 
     * lastSearch is usually a subset of currentSearchString but user may have edited it
     */

    // name:"sensor" rif
    //
    var i = 0;
    var diffStr = "";

    lastSearch = lastSearch.trim();
    currentSearchString = currentSearchString.trim();

    console.log(`getDifference(), lastSearch: ${this.lastSearch} (${lastSearch.length}), currentSearchString: ${currentSearchString} (${currentSearchString.length})`);

    if (lastSearch.length == 0) {
      return currentSearchString;
    }

    // unlikely but can happen if all input is deleted
    // then reset lastSearch as well
    if (currentSearchString.length == (this.threshold + 1)) {
      console.log("Resetting lastSearch");
      this.lastSearch = "";
      return diffStr;
    }

    // if user starts deleting existing input instead of entering new characters
    if (lastSearch.length < currentSearchString.length) {
      while (i < lastSearch.length) {
        if (lastSearch[i] == currentSearchString[i]) {
          i++;
          continue;
        } else {
          break;
        }
      }

      diffStr += currentSearchString.slice(i, currentSearchString.length);
    }

    diffStr = diffStr.trim()
    console.log(`Difference: ${diffStr}`);

    return diffStr;
  }

  triggerSearch() {
    var inputElement = document.getElementById("id_search_string");
    var lastSearch = inputElement.value || "";
    var query = (lastSearch = inputElement.value);
    // var pageNumber = pageInputElement.value;
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
          var query = suggestor.inputElement.value.replace(suggestor.lastSearch, "").trim();
          var search_prefix = suggestor.getDifference(suggestor.lastSearch, suggestor.inputElement.value);

          var suggestUrl = suggestor.getProductSuggestionsUrl(query, search_prefix);

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
          var prefix = "";
          if (data.value.field != "wildcard") {
            prefix +=
              '<td class="autoCompleteResultFieldName">' +
              data.value.field.replace(/_/g, " ") +
              "</td>";
          }
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
        // suggestor.inputElement.value = suggestor.inputElement.value.replace(currentPrefix, appendValue);
        suggestor.inputElement.value = suggestor.lastSearch + appendValue + " ";
        suggestor.lastSearch = suggestor.inputElement.value;
        console.log(`inputElement: ${suggestor.inputElement.value}`);
        console.log(`lastSearch: ${suggestor.lastSearch}`);
        // pageInputElement.value = 1;

        // only for testing
        // suggestor.triggerSearch();
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
