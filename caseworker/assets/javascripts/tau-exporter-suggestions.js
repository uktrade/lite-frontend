const NO_CLE_STRING = "None";

// Global control list entries object pulled from back-end
export let globalCleMatchToItems = {};
// Global Control list entries active
export let globalCheckedProductsWithCle = [];

const createTokenFieldSetItem = (cleName) => {
  const tokenFieldInput = document.querySelector(
    "#control_list_entries .tokenfield-input"
  );

  tokenFieldInput.value = cleName;
  tokenFieldInput.click();

  const tokenFieldSuggestList = document.querySelector(
    "#control_list_entries .tokenfield-suggest-item"
  );
  tokenFieldSuggestList.click();
};

const clearCleList = () => {
  const notListedSuggestionItem = document
    .querySelector("#control_list_entries .tokenfield-set")
    .querySelectorAll("li");

  notListedSuggestionItem.forEach((child) => {
    child.remove();
  });
};

const createNoCleEntry = () => {
  const tokenFieldInput = document.querySelector(
    "#control_list_entries .tokenfield-input"
  );
  const notListedSuggestionField = document.querySelector(
    "#control_list_entries .tokenfield-set ul"
  );
  const newLi = document.createElement("li");
  newLi.classList.add("tokenfield-set-item");
  const newSpan = document.createElement("span");
  newSpan.classList.add("item-label");
  newSpan.innerText = NO_CLE_STRING;
  const newHref = document.createElement("a");
  newHref.classList.add("item-remove");
  newHref.tabIndex = -1;
  newHref.innerText = "×";
  newHref.addEventListener("click", () => {
    const doesNotHaveCleSentenceChecked = document.querySelector(
      "#div_id_does_not_have_control_list_entries input"
    );
    doesNotHaveCleSentenceChecked.checked = false;
  });
  newLi.append(newSpan, newHref);
  clearCleList();
  tokenFieldInput.style.display = "none";
  notListedSuggestionField.appendChild(newLi);
};

const removeNoCleEntry = () => {
  const tokenFieldInput = document.querySelector(
    "#control_list_entries .tokenfield-input"
  );
  tokenFieldInput.style.removeProperty("display");
  clearCleList();
};

const createButtonsForCle = (globalCheckedProductsWithCle) => {
  const filteredArray = globalCheckedProductsWithCle.filter(
    (cle, index, array) =>
      array.findIndex((t) => Object.values(t)[0] == Object.values(cle)[0]) ==
      index
  );
  const suggestionsDiv = document.querySelector(".tau__cle-suggestions");
  while (suggestionsDiv.firstChild) {
    suggestionsDiv.removeChild(suggestionsDiv.lastChild);
  }
  filteredArray.forEach((checked) => {
    const cleName = Object.values(checked)[0];
    const createButton = document.createElement("button");
    createButton.classList.add("lite-button--link", "control-list__list");
    createButton.innerText = `Select exporter suggestion ${cleName}`;
    createButton.addEventListener("click", (event) => {
      event.preventDefault();
      createTokenFieldSetItem(cleName);
    });

    suggestionsDiv.append(createButton);
  });
};

export const addDeleteExporterCleSuggestions = (
  product,
  globalCleMatchToItems,
  globalCheckedProductsWithCle
) => {
  const checked = product.checked;
  const id = product.value;
  if (checked) {
    globalCleMatchToItems[id].forEach((cle) => {
      const newProduct = new Object();
      newProduct[id] = cle;
      globalCheckedProductsWithCle.push(newProduct);
    });
    createButtonsForCle(globalCheckedProductsWithCle);
    return;
  }
  for (let i = 0; i < globalCheckedProductsWithCle.length; i++) {
    if (Object.keys(globalCheckedProductsWithCle[i])[0] === id) {
      globalCheckedProductsWithCle.splice(i, 1);
      i--;
    }
  }
  createButtonsForCle(globalCheckedProductsWithCle);
};

const initTauControlListEntry = () => {
  if (!document.querySelector(".tau")) {
    return;
  }

  const checkboxProducts = document.querySelectorAll(
    ".tau__list [id^='id_goods_']"
  );
  const doesNotHaveCleSentence = document.querySelector(
    "#div_id_does_not_have_control_list_entries input"
  );
  const pulledItemsList = document.querySelectorAll(
    ".govuk-list .tau__cle-object"
  );

  // Create a global array with cle suggestion objects
  pulledItemsList.forEach((product) => {
    const cleRating = JSON.parse(
      product.querySelector("#tau-cle-rating").textContent
    );
    const itemId = JSON.parse(
      product.querySelector("#tau-cle-item-id").textContent
    );

    if (globalCleMatchToItems[itemId]) {
      globalCleMatchToItems[itemId].push(cleRating);
      return;
    }
    globalCleMatchToItems[itemId] = [cleRating];
  });

  // Going through every checkbox and adding event listener or see if its checked.
  checkboxProducts.forEach((product) => {
    // Generate suggestions if checkbox already checked
    if (product.checked) {
      addDeleteExporterCleSuggestions(
        product,
        globalCleMatchToItems,
        globalCheckedProductsWithCle
      );
    }
    // Generate suggestions on click
    product.addEventListener("click", () => {
      addDeleteExporterCleSuggestions(
        product,
        globalCleMatchToItems,
        globalCheckedProductsWithCle
      );
    });
  });

  // The button event for "Select that this product is not on the control list"
  doesNotHaveCleSentence.addEventListener("click", (event) => {
    const checked = event.currentTarget.checked;
    if (checked) {
      createNoCleEntry();
      return;
    }
    removeNoCleEntry();
  });
};

export default initTauControlListEntry;
