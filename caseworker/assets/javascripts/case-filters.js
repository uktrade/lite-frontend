import accessibleAutocomplete from "accessible-autocomplete";
import MultiSelector from "core/multi-selector";

const initCaseFilters = () => {
  const $singleSelects = document.querySelectorAll(".single-select-filter");
  for (const $singleSelect of $singleSelects) {
    accessibleAutocomplete.enhanceSelectElement({
      defaultValue: "",
      preserveNullOptions: true,
      selectElement: $singleSelect,
    });
  }

  const $multiSelects = document.querySelectorAll(".multi-select-filter");
  for (const $multiSelect of $multiSelects) {
    new MultiSelector($multiSelect).init();
  }
};

initCaseFilters();
