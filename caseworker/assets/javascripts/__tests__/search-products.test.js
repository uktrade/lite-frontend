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
    ["foo", 3, "foo"],
    ["foo bar", 7, "bar"],
    ["foo bar baz", 11, "baz"],
    ["foo bar baz", 3, "foo"],
    ["foo bar baz", 7, "bar"],
    ["&escape=me", 9, "%26escape%3Dme"],
  ])(
    "Calling data source with input value '%s'",
    async (inputValue, cursorIndex, query) => {
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
      searchField.focus();
      searchField.setSelectionRange(cursorIndex, cursorIndex);

      const response = await config.data.src();
      expect(fetchMock).toBeCalledWith(`/search-url/?q=${query}`, {
        headers: { Accept: "application/json" },
      });
      expect(response).toEqual([{ field: "a_field", value: "A value" }]);
    }
  );

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
    ["", 0, false],
    [" ", 0, false],
    ["  ", 0, false],
    ["f", 1, false],
    ["fo", 2, true],
    ["foo", 3, true],
    ["foo ", 4, false],
    ["foo b", 5, false],
    ["foo ba", 6, true],
    ["foo bar", 7, true],
    ['test_field:"this"', 17, false],
    ['test_field:"this thing"', 23, false],
    ['test_field:"this thing" foo', 27, true],
    ['test:"this" foo test:"that"', 15, true],
  ])(
    "Trigger condition when input is '%s'",
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

      expect(config.trigger.condition()).toEqual(expected);
    }
  );

  test.each([
    ["bar", 3, { value: { field: "foo", value: "bar" } }, 'foo:"bar"'],
    [
      "starting bar",
      12,
      { value: { field: "foo", value: "bar" } },
      'starting foo:"bar"',
    ],
    [
      "bar starting",
      3,
      { value: { field: "foo", value: "bar" } },
      'foo:"bar" starting',
    ],
    ["bar", 3, { value: { field: "wildcard", value: "foobar" } }, "foobar"],
  ])(
    "On selection with search input value '%s'",
    (inputValue, cursorIndex, selectionValue, expected) => {
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
        selection: selectionValue,
      });

      expect(searchField).toHaveValue(expected);
    }
  );
});
