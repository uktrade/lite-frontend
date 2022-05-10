const SLICED_WORDS = 3; // Select exporter suggestion "ML1"
const NO_CLE_STRING = "None";

const createTokenFieldSetItem = (suggestionSentence) => {
  const sentenceSplit = suggestionSentence.split(" ");
  const cleName = sentenceSplit.slice(SLICED_WORDS).join(" ");

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

export const hideUnhideExporterCle = (product, cleList, selectAll = false) => {
  const checked = product.checked;
  const id = product.value;

  cleList.forEach((cle) => {
    // Hide items.
    if (checked) {
      id === cle.getAttribute("name") &&
        cle.classList.remove("app-hidden--force");
      return;
    }
    // Unhide items.
    !selectAll &&
      id === cle.getAttribute("name") &&
      cle.classList.add("app-hidden--force");
  });
};

const initTauControlListEntry = () => {
  const cleList = document.querySelectorAll(".control-list__list");
  const checkboxProducts = document.querySelectorAll(
    ".tau__list [id^='id_goods_']"
  );
  const doesNotHaveCleSentence = document.querySelector(
    "#div_id_does_not_have_control_list_entries input"
  );

  // Create CLE in the input field after click
  cleList.forEach((cle) =>
    cle.addEventListener("click", (event) => {
      if (!doesNotHaveCleSentence.checked) {
        createTokenFieldSetItem(event.target.innerText);
      }
    })
  );

  checkboxProducts.forEach((product) => {
    product.addEventListener("click", () => {
      hideUnhideExporterCle(product, cleList);
    });
  });

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
