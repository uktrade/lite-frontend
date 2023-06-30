import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";

import {progressivelyEnhanceMultipleSelectField} from "core/multi-select";

const initAutoCompleteField = async (field, choices, propertyName) => {
  const originalInput = document.querySelector(`#id_${field}`);
  const autocompleteContainer = document.createElement("div");
  autocompleteContainer.id = `filter_${field}_container`;
  originalInput.parentElement.appendChild(autocompleteContainer);
  originalInput.style = "display:none";
  let nameInput;
  const getDefaultValue = (originalInput) => {
    const results = choices.filter(
      (obj) => obj[propertyName] === originalInput.value
    );
    if (results.length) {
      return results[0].name;
    }
    return originalInput.dataset.name || "";
  };

  accessibleAutocomplete({
    element: document.querySelector(`#filter_${field}_container`),
    id: `_id_${field}`,
    source: (query, populateResults) => {
      if (!query) {
        populateResults([{ id: null, name: "" }]);
        return;
      }
      populateResults(
        choices.filter((obj) =>
          obj.name.toLowerCase().includes(query.toLowerCase())
        )
      );
    },
    cssNamespace: "lite-autocomplete",
    name: `_id_${field}`,
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
      if (confirmed) {
        originalInput.value = confirmed[propertyName];
      }
    },
    defaultValue: getDefaultValue(originalInput),
    showNoOptionsFound: true,
    autoselect: true,
    confirmOnBlur: true,
  });
  nameInput = document.querySelector(`_id_${field}`);
};

function initFlagsFiltersField() {
  const flagsField = document.getElementById("flags");
  if (!flagsField) return;

  progressivelyEnhanceMultipleSelectField(flagsField, (option) => {
    return { id: option.value, name: option.label, classes: [] };
  });
}

export function initAssignedQueuesFiltersField() {
  const assignedQueuesField = document.getElementById("assigned-queues");
  if (!assignedQueuesField) return;

  progressivelyEnhanceMultipleSelectField(assignedQueuesField, (option) => {
    return { id: option.value, name: option.label, classes: [] };
  });
}

function initCLEFiltersField() {
  const clesField = document.getElementById("control_list_entry");
  if (!clesField) return;
    progressivelyEnhanceMultipleSelectField(clesField, (option) => {
    return { id: option.value, name: option.label, classes: [] };
  });
}

function initRegimeFiltersField() {
  const regimeField = document.getElementById("regime_entry");
  if (!regimeField) return;

  progressivelyEnhanceMultipleSelectField(regimeField, (option) => {
    return { id: option.value, name: option.label, classes: [] };
  });
}

const initCountryAutocompleteField = () => {
  fetch("/api/countries/")
    .then((response) => response.json())
    .then((results) => results["countries"])
    .then((countries) => initAutoCompleteField("country", countries, "id"));
};

const initCaseFilters = () => {
  initCountryAutocompleteField();
  accessibleAutocomplete.enhanceSelectElement({
    defaultValue: "",
    preserveNullOptions: true,
    selectElement: document.querySelector("#case_officer"),
  });
  accessibleAutocomplete.enhanceSelectElement({
    defaultValue: "",
    preserveNullOptions: true,
    selectElement: document.querySelector("#case_adviser"),
  });
  initFlagsFiltersField();
  initAssignedQueuesFiltersField();
  initCLEFiltersField();
  initRegimeFiltersField();
};

initCaseFilters();
