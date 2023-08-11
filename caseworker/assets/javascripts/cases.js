import SelectAllCheckbox from "core/select-all-checkbox";
import SelectAllCheckboxes from "core/select-all-checkboxes";

const initSelectAll = () => {
  const table = document.querySelector("#table-cases");
  const checkboxes = table.querySelectorAll(
    "#table-cases input[type=checkbox]"
  );

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.classList.add("govuk-checkboxes__input");
  const label = document.createElement("label");
  label.classList.add("govuk-label", "govuk-checkboxes__label");
  const checkboxContainer = table.querySelector(
    "thead .govuk-table__cell--checkbox"
  );
  checkboxContainer.append(checkbox, label);

  const selectAllCheckboxes = new SelectAllCheckboxes(checkboxes);
  const selectAllCheckbox = new SelectAllCheckbox(checkbox, label);

  selectAllCheckboxes.on("change", (isAllSelected) => {
    selectAllCheckbox.setSelected(isAllSelected);
  });

  selectAllCheckbox.on("change", (selectAll) => {
    selectAllCheckboxes.selectAll(selectAll);
  });

  selectAllCheckboxes.init();
  selectAllCheckbox.init();
};

initSelectAll();
