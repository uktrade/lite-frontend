const SELECT_ALL = "Select all";
const DESELECT_ALL = "Deselect all";
const SHOW_ALL = "Show all";
const HIDE_ALL = "Hide all";

// Helper functions below this comment
// ------------

const addSelectAllExpandAll = (
  checkboxProducts,
  productsNumberChecks,
  tauHeadline,
  tauSecondColumn
) => {
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

  const selectAllButton = document.createElement("button");
  selectAllButton.innerText = SELECT_ALL;
  selectAllButton.classList.add("lite-button--link", "tau__select-all");
  const expandAllButton = document.createElement("button");
  expandAllButton.innerText = SHOW_ALL;
  expandAllButton.classList.add("lite-button--link");

  createDivOptions.append(selectAllButton, expandAllButton);

  let isAllSelected = false;
  selectAllButton.addEventListener("click", (event) => {
    event.preventDefault();
    if (!isAllSelected) {
      checkboxProducts.forEach((product) => {
        product.checked = true;
        product.dispatchEvent(new Event("input"));
      });
      isAllSelected = true;

      productsNumberChecks.number = productsNumberChecks.max;
      tauHeadline.innerText = `Assessing ${productsNumberChecks.number} products`;
      tauSecondColumn.classList.remove("tau__second-column--hide");
      event.target.innerText = DESELECT_ALL;
    } else {
      checkboxProducts.forEach((product) => {
        product.checked = false;
        product.dispatchEvent(new Event("input"));
      });
      isAllSelected = false;

      productsNumberChecks.number = 0;
      tauSecondColumn.classList.add("tau__second-column--hide");
      event.target.innerText = SELECT_ALL;
    }
  });

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
  addSelectAllExpandAll(
    checkboxProducts,
    productsNumberChecks,
    tauHeadline,
    tauSecondColumn
  );

  // Check for validation error report summary.
  if (errorMessage) {
    tauSecondColumn.classList.remove("tau__second-column--hide");
    productsNumberChecks.number = arrayProducts.filter(
      (product) => product.checked
    ).length;
    tauHeadline.innerText = headlineString(arrayProducts, productsNumberChecks);
  }

  const selectAllInnerText = document.querySelector(".tau__select-all");

  checkboxProducts.forEach((product) =>
    product.addEventListener("click", () => {
      const checkbox = product.checked;

      if (checkbox) {
        productsNumberChecks.number += 1;
      } else {
        productsNumberChecks.number -= 1;
      }

      if (productsNumberChecks.number === 0) {
        tauSecondColumn.classList.add("tau__second-column--hide");
        selectAllInnerText.innerText = SELECT_ALL;
      } else {
        tauSecondColumn.classList.remove("tau__second-column--hide");
        tauHeadline.innerText = headlineString(
          arrayProducts,
          productsNumberChecks
        );
        productsNumberChecks.number === productsNumberChecks.max &&
          (selectAllInnerText.innerText = DESELECT_ALL);
      }
    })
  );
};

export default initTauAssesmentHeadline;
