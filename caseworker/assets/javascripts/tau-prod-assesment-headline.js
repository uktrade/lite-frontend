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
