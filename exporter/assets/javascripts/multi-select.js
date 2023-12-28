import MultiSelector from "core/multi-selector";

const initMultiSelects = () => {
  document
    .querySelectorAll("[data-module=multi-select]")
    .forEach(($el) => new MultiSelector($el).init());
};

export default initMultiSelects;
