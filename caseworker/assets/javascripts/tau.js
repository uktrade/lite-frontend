import SelectAllCheckboxes from "core/select-all-checkboxes";
import SelectAllButton from "core/select-all-button";
import ExpandAll, { SHOW_ALL_BUTTON_TEXT } from "core/expand-all";
import CheckboxClassToggler from "core/checkbox-class-toggler";
import DisablingButton from "core/disabling-button";
import Headline from "./assessment-form/headline";
import SelectProducts from "./assessment-form/select-products";
import CLESuggestions from "./tau/cle-suggestions";
import NoSuggestionsTokenField from "./tau/no-suggestions-token-field";
import MultiSelector from "core/multi-selector";
import initARS from "./tau/ars";
import initRegimes from "./tau/regimes";

const initSelectAll = (goods) => {
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
  const cleMultiSelect = document.querySelector("[name=control_list_entries]");
  const multiSelector = new MultiSelector(cleMultiSelect);
  multiSelector.init();

  const headlineEl = document.querySelector(".assessment-form__headline");
  const headline = new Headline(headlineEl);

  const noControlListCheckboxEl = document.querySelector(
    "[name=does_not_have_control_list_entries]"
  );
  const noSuggestionsTokenField = new NoSuggestionsTokenField(
    noControlListCheckboxEl
  );
  noSuggestionsTokenField.on("change", (checked) => {
    if (checked) {
      multiSelector.setOptions([]);
      multiSelector.setFakeOption("Not on the control list", () => {
        noSuggestionsTokenField.reset();
      });
    } else {
      multiSelector.resetFakeOption();
    }
  });
  noSuggestionsTokenField.init();
  multiSelector.on("change", (selected) => {
    if (selected.length === 0) {
      return;
    }
    noSuggestionsTokenField.reset();
  });

  const suggestionsEl = document.createElement("div");
  suggestionsEl.classList.add("tau-assessment-form__cle-suggestions");
  const controlListEntriesLabel = document.querySelector(
    "[for=id_control_list_entries]"
  );
  controlListEntriesLabel.parentNode.insertBefore(
    suggestionsEl,
    controlListEntriesLabel.nextSibling
  );
  const cleSuggestions = new CLESuggestions(suggestionsEl);
  cleSuggestions.on("change", (selectedSuggestions) => {
    multiSelector.addOptions(selectedSuggestions);
    noSuggestionsTokenField.reset();
  });

  const goods = document.querySelector("#div_id_goods");
  const checkboxes = goods.querySelectorAll("[name=goods]");
  const products = JSON.parse(
    document.querySelector("#cle-suggestions-json").textContent
  );

  const selectProducts = new SelectProducts(checkboxes, products);
  selectProducts.on("change", (selectedProducts) => {
    headline.setProducts(selectedProducts);
    cleSuggestions.setProducts(selectedProducts);
  });
  selectProducts.init();
};

const initSaveAndContinueButton = () => {
  const button = document.querySelector("#submit-id-submit");
  if (!button) {
    return;
  }
  new DisablingButton(button).init();
};

addSelectAllExpandAll();
initCheckboxClassToggler();
initAssessmentForm();
initSaveAndContinueButton();
initARS();
initRegimes();
