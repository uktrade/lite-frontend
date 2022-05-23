import { hideUnhideExporterCle } from "./tau-exporter-suggestions.js";

const SELECT_ALL = "Select all";
const DESELECT_ALL = "Deselect all";
const SHOW_ALL = "Show all";
const HIDE_ALL = "Hide all";

const addSelectAllExpandAll = (
  checkboxProducts,
  cleList,
  productsNumberChecks,
  tauHeadline,
  tauSecondColumn
) => {
  const goods = document.querySelector(".tau__first-column #div_id_goods");

  const createDivOptions = document.createElement("div");
  createDivOptions.classList.add("tau__first-column--options");

  // Adds DIV element for Select All and Expand All
  goods.insertBefore(
    createDivOptions,
    goods.firstElementChild.nextElementSibling
  );

  const selectAllButton = document.createElement("button");
  selectAllButton.innerText = SELECT_ALL;
  selectAllButton.classList.add("lite-button--link", "tau__select-all");
  const expandAllButton = document.createElement("button");
  expandAllButton.innerText = SHOW_ALL;
  expandAllButton.classList.add("lite-button--link");

  createDivOptions.append(selectAllButton, expandAllButton);

  // Select all on click event.
  selectAllButton.addEventListener("click", (event) => {
    event.preventDefault();
    const targetText = event.target.innerText;
    if (targetText === SELECT_ALL) {
      checkboxProducts.forEach((product) => {
        product.checked = true;
        hideUnhideExporterCle(product, cleList);
      });
      productsNumberChecks.number = productsNumberChecks.max;
      tauHeadline.innerText = `Assessing ${productsNumberChecks.number} products`;
      tauSecondColumn.classList.remove("tau__second-column--hide");
      event.target.innerText = DESELECT_ALL;
    }
    if (targetText === DESELECT_ALL) {
      checkboxProducts.forEach((product) => {
        product.checked = false;
        hideUnhideExporterCle(product, cleList);
      });
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

const initTauAssesmentHeadline = () => {
  const checkboxProducts = document.querySelectorAll(
    ".tau__list [id^='id_goods_']"
  );
  const arrayProducts = Array.from(checkboxProducts);
  const cleList = document.querySelectorAll(".control-list__list");
  const tauHeadline = document.querySelector(".tau__headline");
  const tauSecondColumn = document.querySelector(".tau__second-column");

  let productsNumberChecks = {
    number: 0,
    max: checkboxProducts.length,
  };

  // Add Select All and Expand All
  addSelectAllExpandAll(
    checkboxProducts,
    cleList,
    productsNumberChecks,
    tauHeadline,
    tauSecondColumn
  );

  const selectAllInnerText = document.querySelector(".tau__select-all");

  checkboxProducts.forEach((product) =>
    product.addEventListener("click", () => {
      const checkbox = product.checked;

      if (checkbox) {
        productsNumberChecks.number += 1;
      } else {
        productsNumberChecks.number -= 1;
      }

      headlineString =
        productsNumberChecks.number > 1
          ? `Assessing ${productsNumberChecks.number} products`
          : `Assessing ${
              arrayProducts.find((product) => product.checked)?.dataset[
                "productName"
              ]
            }`;
      if (productsNumberChecks.number === 0) {
        tauSecondColumn.classList.add("tau__second-column--hide");
        selectAllInnerText.innerText = SELECT_ALL;
      } else {
        tauSecondColumn.classList.remove("tau__second-column--hide");
        tauHeadline.innerText = headlineString;
        productsNumberChecks.number === productsNumberChecks.max &&
          (selectAllInnerText.innerText = DESELECT_ALL);
      }
    })
  );
};

export default initTauAssesmentHeadline;
