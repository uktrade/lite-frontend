const NO_CLE_STRING = "None";

// Global control list entries object pulled from back-end
export let globalCleMatchToItems = {};
// Checked object with product id and global control list entries in an array
export let globalCheckedProductsWithCle = [];

// Helper functions below this comment
// ------------

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

const removeNoneCleEntry = () => {
  const tokenFieldInput = document.querySelector(
    "#control_list_entries .tokenfield-input"
  );
  tokenFieldInput.style.removeProperty("display");
  clearCleList();
};

const createNoneCleEntry = () => {
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
    removeNoneCleEntry();
  });
  newLi.append(newSpan, newHref);
  clearCleList();
  tokenFieldInput.style.display = "none";
  notListedSuggestionField.appendChild(newLi);
};

const createButtonsForCle = (globalCheckedProductsWithCle) => {
  // We filter the duplicate cle-s at this point using filter prototype
  const filteredArray = globalCheckedProductsWithCle.filter(
    (cle_outer, index, innerArrayLoop) => {
      // if the value matches it will return the index so it gets compared and put into the new array
      const matchedIndex = innerArrayLoop.findIndex(
        (cle_inner) =>
          Object.values(cle_inner)[0] == Object.values(cle_outer)[0]
      );

      return matchedIndex == index;
    }
  );

  // Start making a div for buttons to live within
  const suggestionsDiv = document.querySelector(".tau__cle-suggestions");
  while (suggestionsDiv.firstChild) {
    suggestionsDiv.removeChild(suggestionsDiv.lastChild);
  }

  // Going through a clean array without duplicates and make the buttons
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

  // See if product is checked if YES then create buttons.
  if (checked) {
    // Early return if exporter did not pick cle.
    if (!globalCleMatchToItems[id]) {
      return;
    }
    globalCleMatchToItems[id].forEach((cle) => {
      const newProduct = new Object();
      newProduct[id] = cle;
      globalCheckedProductsWithCle.push(newProduct);
    });
    createButtonsForCle(globalCheckedProductsWithCle);
    return;
  }

  // If it is not checked we remove the product from the array
  for (let i = 0; i < globalCheckedProductsWithCle.length; i++) {
    if (Object.keys(globalCheckedProductsWithCle[i])[0] === id) {
      globalCheckedProductsWithCle.splice(i, 1);
      i--;
    }
  }
  createButtonsForCle(globalCheckedProductsWithCle);
};

// Start of the main function
// ------------

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
    ".tau__cle-suggestion-buttons .tau__cle-object"
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
    // Generate suggestion on click
    product.addEventListener("click", () => {
      addDeleteExporterCleSuggestions(
        product,
        globalCleMatchToItems,
        globalCheckedProductsWithCle
      );
    });
  });

  if (!doesNotHaveCleSentence) {
    return;
  }

  // Check for TAU edit page if CLE is None
  if (doesNotHaveCleSentence.checked) {
    createNoneCleEntry();
  }
  // The button event for "Select that this product is not on the control list"
  doesNotHaveCleSentence.addEventListener("click", (event) => {
    const checked = event.currentTarget.checked;
    if (checked) {
      createNoneCleEntry();
      return;
    }
    removeNoneCleEntry();
  });
};

export default initTauControlListEntry;
