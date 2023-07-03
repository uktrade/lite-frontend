import LiteTokenfield from "./lite-tokenfield";
import LiteTokenFieldStartsWith from "./lite-tokenfield-starts-with";

const defaultGetItem = (option) => {
  return { id: option.value, name: option.text, classes: [] };
};

const getItems = (element, getItem) => {
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
  return { items, selected };
};

const progressivelyEnhanceMultipleSelectField = (
  element,
  getItem = defaultGetItem
) => {
  element.parentElement.classList.add("tokenfield-container");
  var { items, selected } = getItems(element, getItem);
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

const progressivelyEnhanceMultipleSelectFieldStartsWith = (
  element,
  getItem = defaultGetItem
) => {
  element.parentElement.classList.add("tokenfield-container");
  var { items, selected } = getItems(element, getItem);
  var tokenField = new LiteTokenFieldStartsWith({
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

export {
  progressivelyEnhanceMultipleSelectField,
  progressivelyEnhanceMultipleSelectFieldStartsWith,
};
