import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";

const initARS = () => {
  const prefixInput = document.querySelector("#report_summary_prefix");
  const prefixAutocompleteContainer = document.createElement("div");
  prefixAutocompleteContainer.id = "report_summary_prefix_container";
  prefixInput.parentElement.appendChild(prefixAutocompleteContainer);
  prefixInput.style = "display:none";
  accessibleAutocomplete({
    element: document.querySelector("#report_summary_prefix_container"),
    id: "_report_summary_prefix",
    source: (query, populateResults) => {
      fetch(`/tau/report_summary/prefix?name=${query}`)
        .then((response) => response.json())
        .then((results) => results["report_summary_prefixes"])
        .then((results) => populateResults(results));
    },
    cssNamespace: "lite-autocomplete",
    name: "_report_summary_prefix",
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
    onConfirm: (confirmed) => {
      if (!confirmed) {
        return;
      }
      prefixInput.value = confirmed.id;
    },
    defaultValue: prefixInput.value,
    showNoOptionsFound: true,
    autoselect: false,
    showAllValues: true,
  });

  const subjectInput = document.querySelector("#report_summary_subject");
  const subjectAutocompleteContainer = document.createElement("div");
  subjectAutocompleteContainer.id = "report_summary_subject_container";
  subjectInput.parentElement.appendChild(subjectAutocompleteContainer);
  subjectInput.style = "display:none";
  accessibleAutocomplete({
    element: document.querySelector("#report_summary_subject_container"),
    id: "_report_summary_subject",
    source: (query, populateResults) => {
      fetch(`/tau/report_summary/subject?name=${query}`)
        .then((response) => response.json())
        .then((results) => results["report_summary_subjects"])
        .then((results) => populateResults(results));
    },
    cssNamespace: "lite-autocomplete",
    name: "_report_summary_subject",
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
    onConfirm: (confirmed) => {
      if (!confirmed) {
        return;
      }
      subjectInput.value = confirmed.id;
    },
    defaultValue: subjectInput.value,
    showNoOptionsFound: true,
    autoselect: true,
    showAllValues: true,
  });
};

export default initARS;
