import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";

const initARS = () => {
  const input = document.querySelector("#report_summary");
  const autocompleteContainer = document.createElement("div");
  autocompleteContainer.id = "report_summary_container";
  input.parentElement.appendChild(autocompleteContainer);
  input.remove();
  accessibleAutocomplete({
    element: document.querySelector("#report_summary_container"),
    id: "report_summary",
    source: (query, populateResults) => {
      fetch(`/team/picklists/.json?type=report_summary&name=${query}`)
        .then((response) => response.json())
        .then((results) => results["results"])
        .then((results) => populateResults(results));
    },
    cssNamespace: "lite-autocomplete",
    name: "report_summary",
    templates: {
      inputValue: (suggestion) => suggestion?.name ?? "",
      suggestion: (suggestion) => {
        if (typeof suggestion == "string") {
          return suggestion;
        }
        return `
          <div class="govuk-body govuk-!-margin-bottom-0">
            ${suggestion.name}
          </div>
        `;
      },
    },
    defaultValue: input.value,
    showNoOptionsFound: false,
  });
};

export default initARS;
