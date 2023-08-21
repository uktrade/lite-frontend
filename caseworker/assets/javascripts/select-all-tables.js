import SelectAllCheckbox from "core/select-all-checkbox";
import SelectAllCheckboxes from "core/select-all-checkboxes";

const createCheckbox = () => {
  const checkbox = document.createElement("input");

  checkbox.type = "checkbox";
  checkbox.classList.add("govuk-checkboxes__input");

  return checkbox;
};

const createLabel = () => {
  const label = document.createElement("label");

  label.classList.add("govuk-label", "govuk-checkboxes__label");

  return label;
};

const initSelectAllTable = ($table) => {
  const checkboxSelector = $table.dataset.selectAllCheckboxSelector;
  const $checkboxes = $table.querySelectorAll(checkboxSelector);

  const $checkbox = createCheckbox();
  const $label = createLabel();

  const selectAllActionContainerSelector =
    $table.dataset.selectAllActionContainerSelector;
  const checkboxContainer = $table.querySelector(
    selectAllActionContainerSelector
  );

  checkboxContainer.append($checkbox, $label);

  const selectAllCheckboxes = new SelectAllCheckboxes($checkboxes);
  const selectAllCheckbox = new SelectAllCheckbox($checkbox, $label);

  selectAllCheckboxes.on("change", (isAllSelected) => {
    selectAllCheckbox.setSelected(isAllSelected);
  });

  selectAllCheckbox.on("change", (selectAll) => {
    selectAllCheckboxes.selectAll(selectAll);
  });

  selectAllCheckboxes.init();
  selectAllCheckbox.init();
};

const initSelectAllTables = () => {
  const $tables = document.querySelectorAll("[data-module=select-all-table");

  for (const $table of $tables) {
    initSelectAllTable($table);
  }
};

export default initSelectAllTables;
