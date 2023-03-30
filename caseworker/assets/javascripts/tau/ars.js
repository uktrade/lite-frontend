import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";
import debounce from "lodash.debounce";

const initAutocompleteField = (
  summaryFieldType,
  summaryFieldPluralised,
  getDefaultValue
) => {
  const originalInput = document.querySelector(
    `#report_summary_${summaryFieldType}`
  );
  const autocompleteContainer = document.createElement("div");
  autocompleteContainer.id = `report_summary_${summaryFieldType}_container`;
  originalInput.parentElement.appendChild(autocompleteContainer);
  originalInput.style = "display:none";
  let nameInput;
  accessibleAutocomplete({
    element: document.querySelector(
      `#report_summary_${summaryFieldType}_container`
    ),
    id: `_report_summary_${summaryFieldType}`,
    source: debounce((query, populateResults) => {
      if (!query) {
        populateResults([{ id: null, name: "" }]);
        return;
      }
      fetch(`/tau/report_summary/${summaryFieldType}?name=${query}`)
        .then((response) => response.json())
        .then((results) => results[`report_summary_${summaryFieldPluralised}`])
        .then((results) => populateResults(results));
    }, 300),
    cssNamespace: "lite-autocomplete",
    name: `_report_summary_${summaryFieldType}`,
    templates: {
      inputValue: (suggestion) => suggestion?.name ?? "",
      suggestion: (suggestion) => {
        if (typeof suggestion == "string") {
          return suggestion;
        }
        return `
          <div class="govuk-body govuk-!-margin-bottom-0">${suggestion.name}</div>
        `;
      },
    },
    onConfirm: (confirmed) => {
      if (!confirmed && !nameInput.value) {
        originalInput.value = "";
      } else if (confirmed) {
        originalInput.value = confirmed.id;
      }
    },
    defaultValue: getDefaultValue(originalInput),
    showNoOptionsFound: true,
    autoselect: true,
    confirmOnBlur: true,
  });
  nameInput = document.querySelector(`#_report_summary_${summaryFieldType}`);
};

const initARS = () => {
  initAutocompleteField(
    "prefix",
    "prefixes",
    (originalInput) => originalInput.dataset.name || ""
  );
  initAutocompleteField(
    "subject",
    "subjects",
    (originalInput) => originalInput.dataset.name
  );
};

export default initARS;
