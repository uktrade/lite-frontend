import "@testing-library/jest-dom";
import fetchMock from "jest-fetch-mock";

import { ProductSearchSuggestor } from "../search-products";

const createElement = () => {
  const labels = {
    ["a_field"]: "A field label",
  };
  document.body.innerHTML = `
    <div id="product-search">
      <form class="product-search__form" data-product-filter-labels='${JSON.stringify(
        labels
      )}' data-search-url="/search-url/">
        <input class="product-search__search-field" type="text">
      </form>
    </div>
  `;
  return document.querySelector("#product-search");
};

const createComponent = (autoCompleter, $el) => {
  return new ProductSearchSuggestor(autoCompleter, $el);
};

const getSearchField = ($el) => {
  return $el.querySelector(".product-search__search-field");
};

describe("ProductSearchSuggestor", () => {
  test("Calling data source", async () => {
    const $el = createElement();

    const autoCompleteMock = jest.fn();
    const suggestor = createComponent(autoCompleteMock, $el);

    suggestor.init();

    const config = autoCompleteMock.mock.calls[0][0];

    fetchMock.mockResponse(
      JSON.stringify([{ field: "a_field", value: "A value" }])
    );

    let searchField = getSearchField($el);
    searchField.value = "test";

    const response = await config.data.src();
    expect(fetchMock).toBeCalledWith("/search-url/?q=test", {
      headers: { Accept: "application/json" },
    });
    expect(response).toEqual([{ field: "a_field", value: "A value" }]);
  });

  describe("Render resultItem", () => {
    let itemContainer;

    beforeEach(() => {
      const table = document.createElement("table");
      itemContainer = document.createElement("tr");
      itemContainer.innerHTML = "<td>Should be removed</td>";
      table.appendChild(itemContainer);
    });

    test("Field mapped to label", () => {
      const $el = createElement();

      const autoCompleteMock = jest.fn();
      const suggestor = createComponent(autoCompleteMock, $el);

      suggestor.init();

      const config = autoCompleteMock.mock.calls[0][0];

      config.resultItem.content(
        { value: { field: "a_field", value: "A value" } },
        itemContainer
      );

      expect(itemContainer.innerHTML).toEqual(
        '<td class="product-search__suggest-results-key">A field label</td><td class="product-search__suggest-results-value">A value</td>'
      );
    });

    test("Wildcard field", () => {
      const $el = createElement();

      const autoCompleteMock = jest.fn();
      const suggestor = createComponent(autoCompleteMock, $el);

      suggestor.init();

      const config = autoCompleteMock.mock.calls[0][0];

      config.resultItem.content(
        { value: { field: "wildcard", value: "A value" } },
        itemContainer
      );

      expect(itemContainer.innerHTML).toEqual(
        '<td class="product-search__suggest-results-value" colspan="2">A value</td>'
      );
    });
  });
});
