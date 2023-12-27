import accessibleAutocomplete from "accessible-autocomplete";

import SelectedOptions from "core/selected-options";

const getOptions = ($el) => {
  const map = {};
  const values = [];
  for (const option of $el.options) {
    const optionText = option.textContent;
    map[optionText] = option;
    values.push(optionText);
  }
  return [map, values];
};

const handleOnConfirm = (accessibleAutocompleteElement, map, query) => {
  const option = map[query];
  if (!option) {
    return;
  }
  option.selected = true;
  option.dispatchEvent(new Event("change", { bubbles: true }));
  setTimeout(() => (accessibleAutocompleteElement.value = ""), 0);
};

const initMultiSelect = ($el) => {
  const id = $el.id;
  let accessibleAutocompleteElement;

  const [map, values] = getOptions($el);
  const configurationOptions = {
    id: id,
    autoselect: true,
    source: values,
    onConfirm: (query) =>
      handleOnConfirm(accessibleAutocompleteElement, map, query),
  };

  const autocompleteWrapper = document.createElement("div");

  $el.parentNode.insertBefore(autocompleteWrapper, $el);
  $el.id = `${id}-select`;
  accessibleAutocomplete({
    ...configurationOptions,
    element: autocompleteWrapper,
  });

  accessibleAutocompleteElement = document.querySelector(`#${id}`);

  const selectedOptionsWrapper = document.createElement("div");
  const selectedHeader = document.createElement("p");
  selectedHeader.classList.add("govuk-visually-hidden");
  selectedHeader.textContent = `Selected ${$el.dataset.multiSelectObjectsAsPlural}`;
  selectedOptionsWrapper.appendChild(selectedHeader);
  $el.parentNode.insertBefore(selectedOptionsWrapper, $el);
  const selectedOptions = new SelectedOptions(selectedOptionsWrapper, $el);
  selectedOptions.init();

  $el.style.display = "none";

  selectedOptionsWrapper.ariaLive = "polite";
};

const initMultiSelects = () => {
  const multiSelects = document.querySelectorAll("[data-module=multi-select]");
  for (const multiSelect of multiSelects) {
    initMultiSelect(multiSelect);
  }
};

export default initMultiSelects;
