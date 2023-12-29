import "fetch-polyfill";
import accessibleAutocomplete from "accessible-autocomplete";
import MultiSelector from "core/multi-selector";

function initFlagsFiltersField() {
  const flagsField = document.getElementById("flags");
  if (!flagsField) return;
  new MultiSelector(flagsField).init();
}

function initAssignedQueuesFiltersField() {
  const assignedQueuesField = document.getElementById("assigned-queues");
  if (!assignedQueuesField) return;
  new MultiSelector(assignedQueuesField).init();
}

function initCLEFiltersField() {
  const clesField = document.getElementById("control_list_entry");
  if (!clesField) return;
  new MultiSelector(clesField).init();
}

function initRegimeFiltersField() {
  const regimeField = document.getElementById("regime_entry");
  if (!regimeField) return;
  new MultiSelector(regimeField).init();
}

const initCountryAutocompleteField = () => {
  const countriesField = document.getElementById("countries");
  if (!countriesField) return;
  new MultiSelector(countriesField).init();
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
