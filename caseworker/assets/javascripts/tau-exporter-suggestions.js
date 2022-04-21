const createTokenFieldSetItem = (cleName) => {
  suggestionSplit = cleName.split(" ");
  suggestion = suggestionSplit[suggestionSplit.length - 1];

  const inputSuggestion = document
    .querySelector("#control_list_entries")
    .querySelector(".tokenfield-set")
    .querySelector("ul");
  const newLi = document.createElement("li");
  newLi.classList.add("tokenfield-set-item");

  const newSpan = document.createElement("span");
  newSpan.classList.add("item-label");
  newSpan.innerText = suggestion;

  const newHref = document.createElement("a");
  newHref.classList.add("item-remove");
  newHref.tabIndex = -1;
  newHref.innerText = "×";
  newHref.href = "#";

  const newInput = document.createElement("input");
  newInput.classList.add("item-input");
  newInput.type = "hidden";
  newInput.name = "control_list_entries";
  newInput.value = suggestion;

  newLi.append(newSpan, newHref, newInput);

  inputSuggestion.appendChild(newLi);
};

const initTauControlListEntry = () => {
  const cleList = document.querySelectorAll(".control-list__list");
  const checkboxProducts = document.querySelectorAll("[id^='id_goods_']");

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
        cle.classList.add("app-hidden--force");
      });
    });
  });
};

export default initTauControlListEntry;
