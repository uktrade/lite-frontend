import Tokenfield from "tokenfield";

class LiteTokenField extends Tokenfield {
  constructor(options) {
    super(options); // Call the constructor of the parent class (Tokenfield)

    // After the parent class has been initialized, set the attribute
    const tokenfieldInput = document.querySelector(".tokenfield-input");
    if (tokenfieldInput) {
      tokenfieldInput.setAttribute("id", "screen_reader_for_cle");
    }
  }

  /**
   * Override _renderItem not to append [] to end of input name
   * @param item the selected item from the list
   * @param k index of selected item, not used here but kept for compatibility with superclass
   */
  _renderItem = function (item, k) {
    let o = this._options;

    let itemHtml = this.renderSetItemHtml(item);
    let label = itemHtml.querySelector(".item-label");
    let input = itemHtml.querySelector(".item-input");
    let remove = itemHtml.querySelector(".item-remove");

    itemHtml.key = item[this.key];
    remove.key = item[this.key];
    console.log(tokenfieldInput);
    input.setAttribute("name", item.isNew ? o.newItemName : o.itemName);

    input.value = item[item.isNew ? o.newItemValue : o.itemValue] || null;
    label.textContent = this.renderSetItemLabel(item);
    if (item.focused) {
      itemHtml.classList.add("focused");
    }
    return itemHtml;
  };
}

export default window.TokenField = LiteTokenField;
