import LiteTokenfield from "./lite-tokenfield";

class LiteTokenFieldCustomSearch extends LiteTokenfield {
  /**
   * Override __filterData to sort by startswith
   * @param val the user search term
   * @param data list of all data items
   */
  _filterData = function (val, data) {
    val = val.toLowerCase();
    return data
      .filter((v) => v.name.toLowerCase().includes(val))
      .sort((a, b) => {
        const aName = a.name;
        const bName = b.name;
        const aStarts = aName.toLowerCase().startsWith(val);
        const bStarts = bName.toLowerCase().startsWith(val);
        if (aStarts && bStarts) return aName.localeCompare(bName);
        if (aStarts && !bStarts) return -1;
        if (!aStarts && bStarts) return 1;
        return aName.localeCompare(bName);
      });
  };
}

export default window.TokenField = LiteTokenFieldCustomSearch;
