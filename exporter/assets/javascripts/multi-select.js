import accessibleAutocomplete from "accessible-autocomplete";

import MultiSelector from "core/multi-selector";
import SelectedOptions from "core/selected-options";

const initMultiSelects = () => {
  document
    .querySelectorAll("[data-module=multi-select]")
    .forEach(($el) =>
      new MultiSelector(accessibleAutocomplete, SelectedOptions, $el).init()
    );
};

export default initMultiSelects;
