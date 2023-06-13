import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";

import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";
import { enableToggle } from "./toggle";

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

export default function initFlagsFiltersField() {
  const flagsField = document.getElementById("flags");
  if (!flagsField) return;

  const flagsTokenField = progressivelyEnhanceMultipleSelectField(
    flagsField,
    (option) => {
      return { id: option.value, name: option.label, classes: [] };
    }
  );
}

export function initAssignedQueuesFiltersField() {
  const assignedQueuesField = document.getElementById("assigned-queues");
  if (!assignedQueuesField) return;

  const assignedQueuesTokenField = progressivelyEnhanceMultipleSelectField(
    assignedQueuesField,
    (option) => {
      return { id: option.value, name: option.label, classes: [] };
    }
  );
}

function filterIsPopulated(filterGroupName) {
  let filterGroup = document.getElementById(filterGroupName);
  let filters = filterGroup.querySelectorAll("input,select");
  for (const filter of filters) {
    if (
      (filter.value !== "" &&
        filter.value !== "Select" &&
        filter.value !== "blank" &&
        filter.type !== "hidden" &&
        filter.type !== "submit" &&
        filter.type !== "checkbox") ||
      (filter.type === "checkbox" && filter.attributes["checked"])
    ) {
      return true;
    }
  }

  return false;
}

function expandBasicFilters() {
  let caseFilters = document.getElementById("case-filters");
  let showLink = document.getElementById("show-filters-link");
  let hideLink = document.getElementById("hide-filters-link");
}

function expandAdvancedFilters() {
  let advancedFilterDetails = document.getElementById(
    "advanced-filter-details"
  );
  advancedFilterDetails.setAttribute("open", "");
}

function showHideFilters() {
  let expandBasic = filterIsPopulated("basic-filter-fields");
  let expandAdvanced = filterIsPopulated("advanced-filter-fields");

  if (expandBasic || expandAdvanced) expandBasicFilters();
  if (expandAdvanced) expandAdvancedFilters();
}

const initCountryAutocompleteField = () => {
  fetch("/api/countries/")
    .then((response) => response.json())
    .then((results) => results["countries"])
    .then((countries) => initAutoCompleteField("country", countries, "id"));
};

const initRegimeEntryAutocompleteField = () => {
  fetch("/api/regime-entries/")
    .then((response) => response.json())
    .then((regime_entries) =>
      initAutoCompleteField("regime_entry", regime_entries, "pk")
    );
};

const initCaseFilters = () => {
  initCountryAutocompleteField();
  initRegimeEntryAutocompleteField();
  initFlagsFiltersField();
  initAssignedQueuesFiltersField();
  showHideFilters();
};

initCaseFilters();
