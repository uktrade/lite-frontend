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
        id === cle.getAttribute("name") &&
          cle.classList.add("app-hidden--force");
      });
    });
  });
};

export default initTauControlListEntry;
