import "@testing-library/jest-dom";

import SuggestionsTokenField from "../suggestions-token-field";

let component, tokenfieldInput, tokenfieldSuggestItem;

const createElements = () => {
  document.body.innerHTML = `
    <div id="token-field-container">
      <input class="tokenfield-input">
      <div class="tokenfield-suggest-item"></div>
    </div>
  `;

  tokenfieldInput = document.querySelector(".tokenfield-input");
  tokenfieldSuggestItem = document.querySelector(".tokenfield-suggest-item");

  return [tokenfieldInput, tokenfieldSuggestItem];
};

const createComponent = () => {
  createElements();
  component = new SuggestionsTokenField("#token-field-container");
  return component;
};

describe("Suggestions token", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Set suggestions", () => {
    const inputClickSpy = jest.fn();
    const suggestionItemClickSpy = jest.fn();

    tokenfieldInput.addEventListener("click", () => {
      inputClickSpy(tokenfieldInput.value);
    });

    tokenfieldSuggestItem.addEventListener("click", () => {
      suggestionItemClickSpy();
    });

    expect(tokenfieldInput).toHaveValue("");
    component.setSuggestions([{ rating: "R1" }, { rating: "R1a" }]);

    expect(inputClickSpy).toHaveBeenCalledTimes(2);
    expect(inputClickSpy).toHaveBeenNthCalledWith(1, "R1");
    expect(inputClickSpy).toHaveBeenNthCalledWith(2, "R1a");

    expect(suggestionItemClickSpy).toHaveBeenCalledTimes(2);
  });
});
