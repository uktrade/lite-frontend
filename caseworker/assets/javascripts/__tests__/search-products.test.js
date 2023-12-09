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
  beforeEach(() => {
    fetchMock.resetMocks();
  });

  test.each([
    ["foo", "foo"],
    ["foo bar", "bar"],
    ["foo bar baz", "baz"],
  ])("Calling data source with input value '%s'", async (inputValue, query) => {
    const $el = createElement();

    const autoCompleteMock = jest.fn();
    const suggestor = createComponent(autoCompleteMock, $el);

    suggestor.init();

    const config = autoCompleteMock.mock.calls[0][0];

    fetchMock.mockResponse(
      JSON.stringify([{ field: "a_field", value: "A value" }])
    );

    let searchField = getSearchField($el);
    searchField.value = inputValue;

    const response = await config.data.src();
    expect(fetchMock).toBeCalledWith(`/search-url/?q=${query}`, {
      headers: { Accept: "application/json" },
    });
    expect(response).toEqual([{ field: "a_field", value: "A value" }]);
  });

  test.each([
    [
      "mapped field",
      { value: { field: "a_field", value: "A value" } },
      '<td class="product-search__suggest-results-key">A field label</td><td class="product-search__suggest-results-value">A value</td>',
    ],
    [
      "wildcard field",
      { value: { field: "wildcard", value: "A value" } },
      '<td class="product-search__suggest-results-value" colspan="2">A value</td>',
    ],
  ])("Render resultItem with %s", (_, result, expected) => {
    const table = document.createElement("table");
    const itemContainer = document.createElement("tr");
    itemContainer.innerHTML = "<td>Should be removed</td>";
    table.appendChild(itemContainer);

    const $el = createElement();

    const autoCompleteMock = jest.fn();
    const suggestor = createComponent(autoCompleteMock, $el);

    suggestor.init();

    const config = autoCompleteMock.mock.calls[0][0];

    config.resultItem.content(result, itemContainer);

    expect(itemContainer.innerHTML).toEqual(expected);
  });

  test.each([
    ["", false],
    [" ", false],
    ["  ", false],
    ["f", false],
    ["     f     ", false],
    ["fo", true],
    ["foo", true],
    ["foo ", false],
    ["foo b", false],
    ["foo ba", true],
    ["foo bar", true],
  ])("Trigger condition when input is '%s'", (inputValue, expected) => {
    const $el = createElement();

    const autoCompleteMock = jest.fn();
    const suggestor = createComponent(autoCompleteMock, $el);

    suggestor.init();

    const config = autoCompleteMock.mock.calls[0][0];

    const searchField = getSearchField($el);
    searchField.value = inputValue;
    expect(config.trigger.condition()).toEqual(expected);
  });

  test.each([
    ["bar", 3, 'foo:"bar"'],
    ["starting bar", 12, 'starting foo:"bar"'],
    ["bar starting", 3, 'foo:"bar" starting'],
  ])(
    "On selection with search input value '%s'",
    (inputValue, cursorIndex, expected) => {
      const $el = createElement();

      const autoCompleteMock = jest.fn();
      const suggestor = createComponent(autoCompleteMock, $el);

      suggestor.init();

      const config = autoCompleteMock.mock.calls[0][0];

      const searchField = getSearchField($el);
      searchField.value = inputValue;
      searchField.focus();
      searchField.setSelectionRange(cursorIndex, cursorIndex);

      config.onSelection({
        selection: { value: { field: "foo", value: "bar" } },
      });

      expect(searchField).toHaveValue(expected);
    }
  );
});
