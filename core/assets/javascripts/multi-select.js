import LiteTokenfield from "./lite-tokenfield";

const defaultGetItem = (option) => {
  return { id: option.value, name: option.value, classes: [] };
};

const progressivelyEnhanceMultipleSelectField = (
  element,
  getItem = defaultGetItem
) => {
  element.parentElement.classList.add("tokenfield-container");

  var items = [];
  var selected = [];
  for (var i = 0; i < element.options.length; i++) {
    var option = element.options.item(i);
    var item = getItem(option);
    if (option.selected) {
      selected.push(item);
    }
    items.push(item);
  }
  var tokenField = new LiteTokenfield({
    el: element,
    items: items,
    newItems: false,
    addItemOnBlur: true,
    filterSetItems: false,
    addItemsOnPaste: true,
    minChars: 1,
    itemName: element.name,
    setItems: selected,
    keepItemsOrder: false,
  });
  tokenField._renderItems();
  tokenField._html.container.id = element.id;
  element.remove();
  return tokenField;
};

export { progressivelyEnhanceMultipleSelectField };
