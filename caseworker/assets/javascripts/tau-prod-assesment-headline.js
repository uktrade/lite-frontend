import { hideUnhideExporterCle } from "./tau-exporter-suggestions.js";

const addSelectAllExpandAll = (
  checkboxProducts,
  cleList,
  productsNumberChecks
) => {
  const goods = document.querySelector(".tau__first-column #div_id_goods");

  const createDivOptions = document.createElement("div");
  createDivOptions.classList.add("tau__first-column--options");

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

  selectAllButton.addEventListener("click", (event) => {
    event.preventDefault();
    const selectAll = true;
    checkboxProducts.forEach((product) => {
      product.checked = true;
      hideUnhideExporterCle(product, cleList, selectAll);
    });
    productsNumberChecks.number = productsNumberChecks.max;
    console.log(productsNumberChecks);
  });

  expandAllButton.addEventListener("click", (event) => {
    event.preventDefault();
    document
      .querySelector(".tau__list")
      .querySelectorAll(".govuk-details")
      .forEach((product) => product.setAttribute("open", ""));
  });
};

const initTauAssesmentHeadline = () => {
  const checkboxProducts = document.querySelectorAll("[id^='id_goods_']");
  const arrayProducts = Array.from(checkboxProducts);
  const cleList = document.querySelectorAll(".control-list__list");
  const tauHeadline = document.querySelector(".tau__headline");
  let productsNumberChecks = {
    number: 0,
    max: checkboxProducts.length,
    names: [],
  };

  // Add Select All and Expand All
  addSelectAllExpandAll(checkboxProducts, cleList, productsNumberChecks);

  checkboxProducts.forEach((product) =>
    product.addEventListener("click", (event) => {
      productName = product.dataset["productName"];
      checkbox = product.checked;

      if (checkbox) {
        productsNumberChecks.number += 1;
        productsNumberChecks.names.push(productName);
      } else {
        productsNumberChecks.number -= 1;
        productsNumberChecks.names.pop();
      }

      headlineString =
        productsNumberChecks.number > 1
          ? `Assessing ${productsNumberChecks.number} products`
          : `Assesing ${
              arrayProducts.find((product) => product.checked)?.dataset[
                "productName"
              ]
            }`;
      console.log(productsNumberChecks);
      if (productsNumberChecks.number === 0) {
        tauHeadline.innerText = "";
      } else {
        tauHeadline.innerText = headlineString;
      }
    })
  );
};

export default initTauAssesmentHeadline;
