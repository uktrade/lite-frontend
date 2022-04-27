const createTokenFieldSetItem = (suggestionSentence) => {
  sentenceSplit = suggestionSentence.split(" ");
  cleName = sentenceSplit.slice(3).join(" ");

  const tokenFieldInput = document
    .querySelector("#control_list_entries")
    .querySelector(".tokenfield-input");

  tokenFieldInput.value = cleName;
  tokenFieldInput.click();

  const tokenFieldSuggestList = document
    .querySelector("#control_list_entries")
    .querySelectorAll(".tokenfield-suggest-item");
  tokenFieldSuggestList[0].click();
};

const createNoCleEntry = () => {
  const tokenFieldInput = document
    .querySelector("#control_list_entries")
    .querySelector(".tokenfield-input");
  const notListedSuggestionField = document
    .querySelector("#control_list_entries")
    .querySelector(".tokenfield-set")
    .querySelector("ul");
  const newLi = document.createElement("li");
  newLi.classList.add("tokenfield-set-item");

  const newSpan = document.createElement("span");
  newSpan.classList.add("item-label");
  newSpan.innerText = "Not Listed";

  const newHref = document.createElement("a");
  newHref.classList.add("item-remove");
  newHref.tabIndex = -1;
  newHref.innerText = "×";
  newHref.href = "#";

  const newInput = document.createElement("input");
  newInput.classList.add("item-input");
  newInput.type = "hidden";
  newInput.name = "control_list_entries";

  newLi.append(newSpan, newHref, newInput);

  tokenFieldInput.style.display = "none";
  notListedSuggestionField.appendChild(newLi);
};

const removeNoCleEntry = () => {
  const tokenFieldInput = document
    .querySelector("#control_list_entries")
    .querySelector(".tokenfield-input");
  const notListedSuggestionItem = document
    .querySelector("#control_list_entries")
    .querySelector(".tokenfield-set")
    .querySelector("li");
  tokenFieldInput.style.removeProperty("display");
  notListedSuggestionItem.remove();
};

const initTauControlListEntry = () => {
  const cleList = document.querySelectorAll(".control-list__list");
  const checkboxProducts = document.querySelectorAll("[id^='id_goods_']");
  const doesNotHaveCleSentence = document
    .querySelector("#div_id_does_not_have_control_list_entries")
    .querySelector("input");

  cleList.forEach((cle) =>
    cle.addEventListener("click", (event) => {
      createTokenFieldSetItem(event.target.innerText);
    })
  );

  checkboxProducts.forEach((product) => {
    product.addEventListener("click", () => {
      checked = product.checked;
      id = product.value;

      cleList.forEach((cle) => {
        if (checked) {
          id === cle.getAttribute("name") &&
            cle.classList.remove("app-hidden--force");
          return;
        }
        id === cle.getAttribute("name") &&
          cle.classList.add("app-hidden--force");
      });
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
