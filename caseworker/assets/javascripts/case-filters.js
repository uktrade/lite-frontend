import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";
import debounce from "lodash.debounce";

const initCountryAutocompleteField = (
  getDefaultValue
) => {
  const originalInput = document.querySelector(
    '#id_country'
  );
  const autocompleteContainer = document.createElement("div");
  autocompleteContainer.id = 'filter_country_container';
  originalInput.parentElement.appendChild(autocompleteContainer);
  originalInput.style = "display:none";
  let nameInput;
  accessibleAutocomplete({
    element: document.querySelector(
      '#filter_country_container'
    ),
    id: '_id_country',
    source: debounce((query, populateResults) => {
      if (!query) {
        populateResults([{ id: null, name: "" }]);
        return;
      }
      fetch('/api/countries/')
        .then((response) => response.json())
        .then((results) => results['countries'])
        .then((results) => results.filter((obj)=> obj.name.toLowerCase().includes(query.toLowerCase())))
        .then((results) => populateResults(results));
    }, 300),
    cssNamespace: "lite-autocomplete",
    name: '_id_country',
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
  nameInput = document.querySelector('#_id_country');
};

const initRegimeEntryAutocompleteField = (
    getDefaultValue
  ) => {
    const originalInput = document.querySelector(
      '#id_regime_entry'
    );
    const autocompleteContainer = document.createElement("div");
    autocompleteContainer.id = 'filter_regime_entry_container';
    originalInput.parentElement.appendChild(autocompleteContainer);
    originalInput.style = "display:none";
    let nameInput;
    accessibleAutocomplete({
      element: document.querySelector(
        '#filter_regime_entry_container'
      ),
      id: '_id_regime_entry',
      source: debounce((query, populateResults) => {
        if (!query) {
          populateResults([{ id: null, name: "" }]);
          return;
        }
        fetch('/api/regime-entries/')
          .then((response) => response.json())
          .then((results) => results.filter((obj)=> obj.name.toLowerCase().includes(query.toLowerCase())))
          .then((results) => populateResults(results));
      }, 300),
      cssNamespace: "lite-autocomplete",
      name: '_id_regime_entry',
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
    nameInput = document.querySelector('#_id_regime_entry');
  };

const initCaseFilters = () => {
    initCountryAutocompleteField(
        (originalInput) => originalInput.dataset.name || ""
    );
    initRegimeEntryAutocompleteField(
        (originalInput) => originalInput.dataset.name || ""
    );
};

initCaseFilters();
