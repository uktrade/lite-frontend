import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";

import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";

const initAutoCompleteField = async (field, choices, propertyName) => {
    const originalInput = document.querySelector(`#id_${field}`);
    const autocompleteContainer = document.createElement("div");
    autocompleteContainer.id = `filter_${field}_container`;
    originalInput.parentElement.appendChild(autocompleteContainer);
    originalInput.style = "display:none";
    let nameInput;
    const getDefaultValue = (originalInput) => {
        const results = choices.filter((obj) => obj[propertyName] === originalInput.value);
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

function showHideFilters() {
  $(".case-filters").each(function () {
    var $filters = $(this).parent();
    $filters.hide();
    $filters.prev().find("#show-filters-link").show();
    $filters.prev().find("#hide-filters-link").hide();

    $(this)
      .find("input, select")
      .each(function () {
        if (
          $(this).val() != "" &&
          $(this).val() != "Select" &&
          $(this).val() != "blank" &&
          $(this).attr("type") != "hidden" &&
          $(this).attr("type") != "submit" &&
          ($(this).attr("type") != "checkbox" ||
            ($(this).attr("type") == "checkbox" && $(this).attr("checked")))
        ) {
          $filters.show();
          $filters.prev().find("#show-filters-link").hide();
          $filters.prev().find("#hide-filters-link").show();
          $(this).parents(".govuk-details").attr("open", "");
        }
      });
  });
}

const initCountryAutocompleteField = () => {
    fetch("/api/countries/")
        .then((response) => response.json())
        .then((results) => results["countries"])
        .then((countries) => initAutoCompleteField('country', countries, 'id'));
};

const initRegimeEntryAutocompleteField = () => {
    fetch("/api/regime-entries/")
        .then((response) => response.json())
        .then((regime_entries) => initAutoCompleteField('regime_entry', regime_entries, 'pk'));
};

const initCaseFilters = () => {
  initCountryAutocompleteField();
  initRegimeEntryAutocompleteField();
  initFlagsFiltersField();

  showHideFilters();
};

initCaseFilters();
