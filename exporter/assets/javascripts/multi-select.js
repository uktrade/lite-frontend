import accessibleAutocomplete from "accessible-autocomplete";

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

  const element = document.createElement("div");
  $el.parentNode.insertBefore(element, $el);

  $el.id = `${id}-select`;

  accessibleAutocomplete({
    ...configurationOptions,
    element: element,
  });

  accessibleAutocompleteElement = document.querySelector(`#${id}`);
};

const initMultiSelects = () => {
  const multiSelects = document.querySelectorAll("[data-module=multi-select]");
  for (const multiSelect of multiSelects) {
    initMultiSelect(multiSelect);
  }
};

export default initMultiSelects;
