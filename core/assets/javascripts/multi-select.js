import LiteTokenfield from "./lite-tokenfield";

const defaultGetItem = (option) => {
  return { id: option.value, name: option.value, classes: [] };
};

const getItems = (element, getItem) => {
  const items = [];
  const selected = [];
  for (let i = 0; i < element.options.length; i++) {
    const option = element.options.item(i);
    const item = getItem(option);
    if (option.selected) {
      selected.push(item);
    }
    items.push(item);
  }
  return { items, selected };
};

const progressivelyEnhanceMultipleSelectFactory = (TokenFieldType) => {
  const enhancer = (element, getItem = defaultGetItem) => {
    element.parentElement.classList.add("tokenfield-container");
    const { items, selected } = getItems(element, getItem);
    const tokenField = new TokenFieldType({
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

  return enhancer;
};

const progressivelyEnhanceMultipleSelectField =
  progressivelyEnhanceMultipleSelectFactory(LiteTokenfield);

export { progressivelyEnhanceMultipleSelectField };
