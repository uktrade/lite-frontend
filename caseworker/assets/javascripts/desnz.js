import SelectAllCheckboxes from "core/select-all-checkboxes";
import SelectAllButton from "core/select-all-button";
import ExpandAll, { SHOW_ALL_BUTTON_TEXT } from "core/expand-all";
import Headline from "./assessment-form/headline";
import SelectProducts from "./assessment-form/select-products";
import CheckboxClassToggler from "core/checkbox-class-toggler";
import DisablingButton from "core/disabling-button";

const initSelectAll = (goods) => {
  if (!goods) {
    return;
  }

  const checkboxes = goods.querySelectorAll("[name=goods]");
  const selectAllCheckboxes = new SelectAllCheckboxes(checkboxes);

  const button = document.createElement("button");
  button.classList.add("lite-button--link", "assessment-form__select-all");
  const selectAllButton = new SelectAllButton(button);

  selectAllCheckboxes.on("change", (isAllSelected) => {
    selectAllButton.setSelected(isAllSelected);
  });

  selectAllButton.on("click", (selectAll) => {
    selectAllCheckboxes.selectAll(selectAll);
  });

  selectAllButton.init();
  selectAllCheckboxes.init();

  return button;
};

const initExpandAll = (goods) => {
  if (!goods) {
    return;
  }
  const expandAllButton = document.createElement("button");
  expandAllButton.innerText = SHOW_ALL_BUTTON_TEXT;
  expandAllButton.classList.add("lite-button--link");

  const details = goods.querySelectorAll(".govuk-details");

  new ExpandAll(expandAllButton, details).init();

  return expandAllButton;
};

const initButtonContainer = (goods) => {
  const createDivOptions = document.createElement("div");
  createDivOptions.classList.add("assessment-form__first-column--options");
  goods.insertBefore(
    createDivOptions,
    goods.firstElementChild.nextElementSibling
  );
  return createDivOptions;
};

const addSelectAllExpandAll = () => {
  const goods = document.querySelector("#div_id_goods");
  if (!goods) {
    return;
  }

  const buttonContainer = initButtonContainer(goods);
  const selectAllButton = initSelectAll(goods);
  const expandAllButton = initExpandAll(goods);

  buttonContainer.append(selectAllButton, expandAllButton);
};

const initCheckboxClassToggler = () => {
  const goods = document.querySelector("#div_id_goods");
  if (!goods) {
    return;
  }
  const checkboxes = goods.querySelectorAll("[name=goods]");
  const assessmentColumn = document.querySelector(
    ".assessment-form__second-column"
  );

  new CheckboxClassToggler(
    checkboxes,
    assessmentColumn,
    "assessment-form__second-column--hide"
  ).init();
};

const initAssessmentForm = () => {
  const headlineEl = document.querySelector(".assessment-form__headline");
  const headline = new Headline(headlineEl);

  const goods = document.querySelector("#div_id_goods");
  const checkboxes = goods.querySelectorAll("[name=goods]");
  if (!goods) {
    return;
  }
  const products = JSON.parse(
    document.querySelector("#unassessed-trigger-list-goods-json").textContent
  );
  new SelectProducts(checkboxes, products, (selectedProducts) => {
    headline.setProducts(selectedProducts);
  }).init();
};

const initSaveAndContinueButton = () => {
  const button = document.querySelector("#submit-id-submit");
  if (button) {
    new DisablingButton(button).init();
  }
};

addSelectAllExpandAll();
initCheckboxClassToggler();
initAssessmentForm();
initSaveAndContinueButton();
