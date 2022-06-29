import SelectAll, { SELECT_ALL_BUTTON_TEXT } from "core/select-all";

const SHOW_ALL = "Show all";
const HIDE_ALL = "Hide all";

// Helper functions below this comment
// ------------
const initSelectAll = (goods) => {
  const selectAllButton = document.createElement("button");
  selectAllButton.innerText = SELECT_ALL_BUTTON_TEXT;
  selectAllButton.classList.add("lite-button--link", "tau__select-all");

  const checkboxes = goods.querySelectorAll("[name=goods]");

  new SelectAll(selectAllButton, checkboxes).init();

  return selectAllButton;
};

const addSelectAllExpandAll = () => {
  const goods = document.querySelector(".tau__first-column #div_id_goods");

  const createDivOptions = document.createElement("div");
  createDivOptions.classList.add("tau__first-column--options");

  // Adds DIV element for Select All and Expand All

  if (goods) {
    goods.insertBefore(
      createDivOptions,
      goods.firstElementChild.nextElementSibling
    );
  }

  const selectAllButton = initSelectAll(goods);

  const expandAllButton = document.createElement("button");
  expandAllButton.innerText = SHOW_ALL;
  expandAllButton.classList.add("lite-button--link");

  createDivOptions.append(selectAllButton, expandAllButton);

  // Expand all on click event.
  expandAllButton.addEventListener("click", (event) => {
    event.preventDefault();
    const targetText = event.target.innerText;
    const products = document
      .querySelector(".tau__list")
      .querySelectorAll(".govuk-details");
    if (targetText === SHOW_ALL) {
      products.forEach((product) => product.setAttribute("open", ""));
      event.target.innerText = HIDE_ALL;
    } else {
      products.forEach((product) => product.removeAttribute("open"));
      event.target.innerText = SHOW_ALL;
    }
  });
};

const headlineString = (arrayProducts, productsNumberChecks) => {
  return productsNumberChecks.number > 1
    ? `Assessing ${productsNumberChecks.number} products`
    : `Assessing ${
        arrayProducts.find((product) => product.checked)?.dataset["productName"]
      }`;
};

// Start of the main function
// ------------

const initTauAssesmentHeadline = () => {
  if (!document.querySelector(".tau")) {
    return;
  }

  const checkboxProducts = document.querySelectorAll(
    ".tau__list [id^='id_goods_']"
  );
  const arrayProducts = Array.from(checkboxProducts);
  const tauHeadline = document.querySelector(".tau__headline");
  const tauSecondColumn = document.querySelector(".tau__second-column");
  const errorMessage = document.querySelector("#tau-form .govuk-error-message");

  let productsNumberChecks = {
    number: 0,
    max: checkboxProducts.length,
  };

  // Add Select All and Expand All
  addSelectAllExpandAll();

  // Check for validation error report summary.
  if (errorMessage) {
    tauSecondColumn.classList.remove("tau__second-column--hide");
    productsNumberChecks.number = arrayProducts.filter(
      (product) => product.checked
    ).length;
    tauHeadline.innerText = headlineString(arrayProducts, productsNumberChecks);
  }

  checkboxProducts.forEach((product) =>
    product.addEventListener("input", () => {
      const checkbox = product.checked;

      if (checkbox) {
        productsNumberChecks.number += 1;
      } else {
        productsNumberChecks.number -= 1;
      }

      if (productsNumberChecks.number === 0) {
        tauSecondColumn.classList.add("tau__second-column--hide");
      } else {
        tauSecondColumn.classList.remove("tau__second-column--hide");
        tauHeadline.innerText = headlineString(
          arrayProducts,
          productsNumberChecks
        );
      }
    })
  );
};

export default initTauAssesmentHeadline;
