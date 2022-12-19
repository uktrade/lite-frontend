import SelectAll, { SELECT_ALL_BUTTON_TEXT } from "core/select-all";
import ExpandAll, { SHOW_ALL_BUTTON_TEXT } from "core/expand-all";
import Headline from "./tau/headline";
import SelectProducts from "./tau/select-products";
import CheckboxClassToggler from "core/checkbox-class-toggler";
import DisablingButton from "core/disabling-button";

const initSelectAll = (goods) => {
  const selectAllButton = document.createElement("button");
  selectAllButton.innerText = SELECT_ALL_BUTTON_TEXT;
  selectAllButton.classList.add("lite-button--link", "tau__select-all");

  const checkboxes = goods.querySelectorAll("[name=goods]");

  new SelectAll(selectAllButton, checkboxes).init();

  return selectAllButton;
};

const initExpandAll = (goods) => {
  const expandAllButton = document.createElement("button");
  expandAllButton.innerText = SHOW_ALL_BUTTON_TEXT;
  expandAllButton.classList.add("lite-button--link");

  const details = goods.querySelectorAll(".govuk-details");

  new ExpandAll(expandAllButton, details).init();

  return expandAllButton;
};

const initButtonContainer = (goods) => {
  const createDivOptions = document.createElement("div");
  createDivOptions.classList.add("tau__first-column--options");
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
  const assessmentColumn = document.querySelector(".tau__second-column");

  new CheckboxClassToggler(
    checkboxes,
    assessmentColumn,
    "tau__second-column--hide"
  ).init();
};

const initAssessmentForm = () => {
  const headlineEl = document.querySelector(".beis__headline");
  const headline = new Headline(headlineEl);

  const goods = document.querySelector("#div_id_goods");
  const checkboxes = goods.querySelectorAll("[name=goods]");
  const products = JSON.parse(
    document.querySelector("#unassessed-trigger-list-goods-json").textContent
  );
  new SelectProducts(checkboxes, products, (selectedProducts) => {
    headline.setProducts(selectedProducts);
  }).init();
};

const initSaveAndContinueButton = () => {
  const button = document.querySelector("#submit-id-submit");
  new DisablingButton(button).init();
};

addSelectAllExpandAll();
initCheckboxClassToggler();
initAssessmentForm();
initSaveAndContinueButton();
