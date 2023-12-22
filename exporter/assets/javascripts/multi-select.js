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

const handleOnConfirm = (map, query) => {
  const option = map[query];
  if (!option) {
    return;
  }
  option.selected = true;
};

const initMultiSelect = ($el) => {
  const [map, values] = getOptions($el);
  const configurationOptions = {
    id: $el.id,
    autoselect: true,
    source: values,
    onConfirm: (query) => handleOnConfirm(map, query),
  };

  const element = document.createElement("div");
  $el.parentNode.insertBefore(element, $el);

  $el.id = `${$el.id}-select`;

  accessibleAutocomplete({
    ...configurationOptions,
    element: element,
  });
};

const initMultiSelects = () => {
  const multiSelects = document.querySelectorAll("[data-module=multi-select]");
  for (const multiSelect of multiSelects) {
    initMultiSelect(multiSelect);
  }
};

export default initMultiSelects;
