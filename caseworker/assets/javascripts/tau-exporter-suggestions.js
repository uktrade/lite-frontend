const NO_CLE_STRING = "None";

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

// Start of the main function
// ------------

const initTauControlListEntry = () => {
  if (!document.querySelector(".tau")) {
    return;
  }

  const doesNotHaveCleSentence = document.querySelector(
    "#div_id_does_not_have_control_list_entries input"
  );

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
