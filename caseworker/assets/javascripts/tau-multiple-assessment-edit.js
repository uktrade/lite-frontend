import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";
import debounce from "lodash.debounce";
import MultiSelector from "core/multi-selector";

const initAutocompleteField = (
  originalInput,
  summaryFieldType,
  summaryFieldPluralised,
  getDefaultValue
) => {
  const autocompleteContainer = document.createElement("div");
  autocompleteContainer.id = `${originalInput.id}_container`;
  originalInput.parentElement.appendChild(autocompleteContainer);
  originalInput.style = "display:none";
  let nameInput;
  accessibleAutocomplete({
    element: document.querySelector(`#${autocompleteContainer.id}`),
    id: `_${originalInput.id}`,
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
    name: `_${originalInput.id}`,
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
  nameInput = document.querySelector(`#_${originalInput.id}`);
};

const initARS = () => {
  const reportSummaryPrefixes = document.querySelectorAll(
    ".report-summary-prefix"
  );
  for (const reportSummaryPrefix of reportSummaryPrefixes) {
    initAutocompleteField(
      reportSummaryPrefix,
      "prefix",
      "prefixes",
      (originalInput) => originalInput.dataset.name || ""
    );
  }

  const reportSummarySubjects = document.querySelectorAll(
    ".report-summary-subject"
  );
  for (const reportSummarySubject of reportSummarySubjects) {
    initAutocompleteField(
      reportSummarySubject,
      "subject",
      "subjects",
      (originalInput) => originalInput.dataset.name
    );
  }
};

const initCLEs = () => {
  const cleMultiSelects = document.querySelectorAll(".control-list-entries");
  for (const cleMultiSelect of cleMultiSelects) {
    const multiSelector = new MultiSelector(cleMultiSelect);
    multiSelector.init();
  }
};

const initRegimes = () => {
  const regimeEntryFields = document.querySelectorAll(".regime-entries");
  for (const regimeEntryField of regimeEntryFields) {
    const multiSelector = new MultiSelector(regimeEntryField);
    multiSelector.init();
  }
};

initARS();
initRegimes();
initCLEs();
