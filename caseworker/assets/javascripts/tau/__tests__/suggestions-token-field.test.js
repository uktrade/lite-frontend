import "@testing-library/jest-dom";

import SuggestionsTokenField from "../suggestions-token-field";

let component, tokenFieldContainer, mockTokenfield;

const createElements = () => {
  document.body.innerHTML = `
    <div id="token-field-container">
    </div>
  `;

  mockTokenfield = {
    addItems: jest.fn(),
  };

  tokenFieldContainer = document.querySelector("#token-field-container");
  tokenFieldContainer.tokenfield = mockTokenfield;

  return tokenFieldContainer;
};

const createComponent = () => {
  createElements();
  component = new SuggestionsTokenField("#token-field-container");
  return component;
};

describe("Suggestions token field", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Set suggestions", () => {
    component.setSuggestions([
      { id: "1", rating: "R1" },
      { id: "2", rating: "R1a" },
    ]);
    expect(mockTokenfield.addItems).toBeCalledWith([
      { id: "R1", name: "R1" },
      { id: "R1a", name: "R1a" },
    ]);
  });
});
