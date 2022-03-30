import "url-search-params-polyfill";
import "fetch-polyfill";
import autoComplete from "@tarekraafat/autocomplete.js";
import Lightpick from "./lightpick.js";

(function () {
  var inputElement = document.getElementById("id_search_string");
  var pageInputElement = document.getElementById("id_page");
  var searchButtonElement = document.getElementById("search-button");
  var resultsElement = document.getElementById("results-table");
  var currentSearch = inputElement.value || "";
  var lastSearch = inputElement.value || "";

  // focus at end of the field and make sure there is a space at the end
  inputElement.focus();
  if (!/ $/.test(inputElement.value)) {
    inputElement.value = inputElement.value + " ";
  }
  inputElement.setSelectionRange(
    inputElement.value.length,
    inputElement.value.length
  );

  var autocomplete = new autoComplete({
    trigger: {
      event: ["input"],
      condition: function (query) {
        return query.length > autocomplete.threshold && query !== " ";
      },
    },
    data: {
      src: function () {
        currentSearch = inputElement.value.replace(lastSearch, "").trim();
        var query = currentSearch.toLowerCase();
        return fetch(
          "/search/products/suggest/?format=json&q=" + escape(query)
        ).then(function (response) {
          return response.json().then(function (parsed) {
            // cheap prefix match "incor" for "spire"
            if (currentSearch.indexOf("spi") > -1) {
              parsed = [{ field: "database", value: "SPIRE" }].concat(parsed);
              // cheap prefix match "incor" for "lite"
            } else if (currentSearch.indexOf("lit") > -1) {
              parsed = [{ field: "database", value: "LITE" }].concat(parsed);
              // cheap prefix match "incor" for "incorporated"
            } else if (currentSearch.indexOf("incor") > -1) {
              parsed = [
                { field: "incorporated", value: "true" },
                { field: "incorporated", value: "false" },
              ].concat(parsed);
            }
            return parsed;
          });
        });
      },
      key: ["value"],
      cache: false,
    },
    selector: "#id_search_string",
    threshold: 1,
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
    maxResults: 5,
    onSelection: function (feedback) {
      if (feedback.selection.value.field == "wildcard") {
        var appendValue = feedback.selection.value.value;
      } else {
        var appendValue =
          feedback.selection.value.field +
          ':"' +
          feedback.selection.value.value +
          '"';
      }
      inputElement.value = inputElement.value.replace(
        currentSearch,
        appendValue + " "
      );
      pageInputElement.value = 1;
      handleSearch();
    },
  });

  function handleSearch() {
    var query = (lastSearch = inputElement.value);
    var pageNumber = pageInputElement.value;
    setTimeout(function () {
      inputElement.focus();
    });
    fetch(
      "/search/products/?search_string=" + escape(query) + "&page=" + pageNumber
    ).then(function (response) {
      var html = response.text().then(function (html) {
        var div = document.createElement("div");
        div.innerHTML = html.trim();
        document.getElementsByClassName("results-area")[0].innerHTML =
          div.getElementsByClassName("results-area")[0].innerHTML;
        listenToPaginationClick();
      });
    });
    var searchParams = new URLSearchParams(window.location.search);
    searchParams.set("search_string", query);
    searchParams.set("page", pageNumber);
    history.pushState(
      null,
      "",
      window.location.pathname + "?" + searchParams.toString()
    );
  }

  function listenToPaginationClick() {
    // the pagination element is replaced on search, so need to re-add event listeners when that happens
    var elements = document.getElementsByClassName("lite-pagination__link");
    for (var i = 0; i < elements.length; i++) {
      var element = elements.item(i);
      element.addEventListener("click", function (event) {
        event.preventDefault();
        pageInputElement.value = event.target.getAttribute("data-number");
        handleSearch();
      });
    }
  }

  searchButtonElement.addEventListener("click", function (event) {
    event.preventDefault();
    pageInputElement.value = 1;
    handleSearch();
  });

  listenToPaginationClick();

  function handleExpandClick() {
    event.preventDefault();
    var selector = this.getAttribute("data-target-selector");
    document.getElementById(selector).classList.remove("hide-rows");
    this.remove();
  }

  var elements = document.querySelectorAll(".js-expand-inner-hits");
  for (var i = 0; i < elements.length; i++) {
    elements.item(i).addEventListener("click", handleExpandClick);
  }
})();
