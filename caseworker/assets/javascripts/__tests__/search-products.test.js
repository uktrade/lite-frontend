import "@testing-library/jest-dom";
import fetchMock from "jest-fetch-mock";

import { ProductSearchSuggestor } from "../search-products";

const createElement = () => {
  const labels = {
    ["a_field"]: "A field label",
  };
  document.body.innerHTML = `
    <div id="query-search">
      <form class="query-search__form" data-product-filter-labels='${JSON.stringify(
        labels
      )}' data-search-url="/search-url/">
        <input class="query-search__search-field" type="text">
      </form>
    </div>
  `;
  return document.querySelector("#query-search");
};

const createComponent = (autoCompleter, $el) => {
  return new ProductSearchSuggestor(autoCompleter, $el);
};

const getSearchField = ($el) => {
  return $el.querySelector(".query-search__search-field");
};

describe("ProductSearchSuggestor", () => {
  beforeEach(() => {
    fetchMock.resetMocks();
  });

  test.each([
    ["foo", 3, "foo"],
    ["foo bar", 7, "foo%20bar"],
    ["foo bar baz", 11, "foo%20bar%20baz"],
    ["foo bar baz", 3, "foo%20bar%20baz"],
    ["foo bar baz", 7, "foo%20bar%20baz"],
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
      '<td class="query-search__suggest-results-key">A field label</td><td class="query-search__suggest-results-value">A value</td>',
    ],
    [
      "wildcard field",
      { value: { field: "wildcard", value: "A value" } },
      '<td class="query-search__suggest-results-value" colspan="2">A value</td>',
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
    ["foo ", 4, true],
    ["foo b", 5, true],
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
    ["bar", 3, { value: { field: "foo", value: "bar" } }, 'foo:"bar" ', 10],
    [
      "starting bar",
      12,
      { value: { field: "foo", value: "bar" } },
      'foo:"bar" ',
      10,
    ],
    [
      "bar starting",
      3,
      { value: { field: "foo", value: "bar" } },
      'foo:"bar" ',
      10,
    ],
    [
      'foo:"bar" baz',
      13,
      { value: { field: "quux", value: "baz" } },
      'foo:"bar" quux:"baz" ',
      14,
    ],
    [
      'foo:"bar" AND baz',
      17,
      { value: { field: "quux", value: "baz" } },
      'foo:"bar" AND quux:"baz" ',
      18,
    ],
    ["bar", 3, { value: { field: "wildcard", value: "foobar" } }, "foobar ", 7],
    [
      "foo AND bar",
      11,
      { value: { field: "baz", value: "bar" } },
      'foo AND baz:"bar" ',
      18,
    ],
    [
      "foo OR bar",
      10,
      { value: { field: "baz", value: "bar" } },
      'foo OR baz:"bar" ',
      17,
    ],
    [
      "foo NOT bar",
      11,
      { value: { field: "baz", value: "bar" } },
      'foo NOT baz:"bar" ',
      18,
    ],
  ])(
    "On selection with search input value '%s'",
    (inputValue, cursorIndex, selectionValue, expectedValue) => {
      const $el = createElement();

      const autoCompleteMock = jest.fn();
      const suggestor = createComponent(autoCompleteMock, $el);

      suggestor.init();

      const config = autoCompleteMock.mock.calls[0][0];

      const searchField = getSearchField($el);
      searchField.value = inputValue;
      searchField.focus();
      searchField.setSelectionRange(cursorIndex, cursorIndex);

      searchField.blur();
      config.onSelection({
        selection: selectionValue,
      });

      expect(searchField).toHaveValue(expectedValue);
      expect(searchField).toHaveFocus();

      // expect(searchField.selectionStart).toEqual(expectedSelectionStart);
      // expect(searchField.selectionStart).toEqual(searchField.selectionEnd);
      // Ideally we want to check that setRangeText is being called with "end"
      // and to do that we want to check that the selectionStart is ending up
      // in the place that we would expect.
      // However, we seem to be getting the wrong value back, there is a commit
      // in jsdom that shows this used to be a bug that they've fixed but even
      // an upgrade to jsdom doesn't seem to have fixed it.
      // My theory is that jest-environment-jsdom is installing an earlier
      // version of jsdom that has the bug that's being used in our test
      // environments instead.
      // https://github.com/jsdom/jsdom/releases/tag/21.1.2
    }
  );
});
