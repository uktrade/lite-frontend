import { hideUnhideExporterCle } from "./tau-exporter-suggestions.js";

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
  selectAllButton.innerText = "Select all";
  selectAllButton.classList.add("lite-button--link");
  const expandAllButton = document.createElement("button");
  expandAllButton.innerText = "Expand all";
  expandAllButton.classList.add("lite-button--link");

  createDivOptions.append(selectAllButton, expandAllButton);

  // Select all on click event.
  selectAllButton.addEventListener("click", (event) => {
    event.preventDefault();
    const selectAll = true;
    checkboxProducts.forEach((product) => {
      product.checked = true;
      hideUnhideExporterCle(product, cleList, selectAll);
    });
    productsNumberChecks.number = productsNumberChecks.max;
    tauHeadline.innerText = `Assessing ${productsNumberChecks.number} products`;
    tauSecondColumn.classList.remove("tau__second-column--hide");
  });

  // Expand all on click event.
  expandAllButton.addEventListener("click", (event) => {
    event.preventDefault();
    document
      .querySelector(".tau__list")
      .querySelectorAll(".govuk-details")
      .forEach((product) => product.setAttribute("open", ""));
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
      } else {
        tauSecondColumn.classList.remove("tau__second-column--hide");
        tauHeadline.innerText = headlineString;
      }
    })
  );
};

export default initTauAssesmentHeadline;
