import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";
import debounce from "lodash.debounce";

import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";

const initCountryAutocompleteField = async () => {
  const originalInput = document.querySelector("#id_country");
  const autocompleteContainer = document.createElement("div");
  autocompleteContainer.id = "filter_country_container";
  originalInput.parentElement.appendChild(autocompleteContainer);
  originalInput.style = "display:none";
  let nameInput;
  const countryData = await fetch("/api/countries/")
      .then((response) => response.json())
      .then((results) => results["countries"]);
  const getDefaultValue = (originalInput) => {
    const results = countryData.filter((obj) => obj.id == originalInput.value);
    if (results.length) {
        return results[0].name;
    }
    return originalInput.dataset.name || "";
  }

  accessibleAutocomplete({
    element: document.querySelector("#filter_country_container"),
    id: "_id_country",
    source: async (query, populateResults) => {
      if (!query) {
        populateResults([{ id: null, name: "" }]);
        return;
      }
      populateResults(
        countryData.filter((obj) =>
          obj.name.toLowerCase().includes(query.toLowerCase())
        )
      );
    },
    cssNamespace: "lite-autocomplete",
    name: "_id_country",
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
        originalInput.value = confirmed.id;
      }
    },
    defaultValue: getDefaultValue(originalInput),
    showNoOptionsFound: true,
    autoselect: true,
    confirmOnBlur: true,
  });
  nameInput = document.querySelector("#_id_country");
};

const initRegimeEntryAutocompleteField = async () => {
  const originalInput = document.querySelector("#id_regime_entry");
  const autocompleteContainer = document.createElement("div");
  autocompleteContainer.id = "filter_regime_entry_container";
  originalInput.parentElement.appendChild(autocompleteContainer);
  originalInput.style = "display:none";
  let nameInput;
  const regimeEntriesData = await fetch("/api/regime-entries/").then(
    (response) => response.json()
  );
  const getDefaultValue = (originalInput) => {
    const results = regimeEntriesData.filter((obj) => obj.pk == originalInput.value);
    if (results.length) {
        return results[0].name;
    }
    return originalInput.dataset.name || "";
  }
  accessibleAutocomplete({
    element: document.querySelector("#filter_regime_entry_container"),
    id: "_id_regime_entry",
    source: debounce((query, populateResults) => {
      if (!query) {
        populateResults([{ id: null, name: "" }]);
        return;
      }
      populateResults(
        regimeEntriesData.filter((obj) =>
          obj.name.toLowerCase().includes(query.toLowerCase())
        )
      );
    }, 300),
    cssNamespace: "lite-autocomplete",
    name: "_id_regime_entry",
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
        originalInput.value = confirmed.pk;
      }
    },
    defaultValue: getDefaultValue(originalInput),
    showNoOptionsFound: true,
    autoselect: true,
    confirmOnBlur: true,
  });
  nameInput = document.querySelector("#_id_regime_entry");
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

const initCaseFilters = () => {
  initCountryAutocompleteField();
  initRegimeEntryAutocompleteField();

  initFlagsFiltersField();

  showHideFilters();

  $(".lite-filter-toggle-link").on(function () {
    var $filters = $(this).parent().next();
    $filters.toggle();
    $(this).parent().find("> *").toggle();

    return false;
  });
};

initCaseFilters();
