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
    component.setSuggestions(["R1", "R1a"]);
    expect(mockTokenfield.addItems).toBeCalledWith([
      { id: "R1", name: "R1" },
      { id: "R1a", name: "R1a" },
    ]);
  });
  test("Set on change listener", () => {
    const tokenfield = {
      on: jest.fn(),
    };

    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    const showNcscBox = jest.fn();
    const hideNcscBox = jest.fn();

    component.setOnChangeListener(showNcscBox, hideNcscBox);
    tokenfield.on.mock.calls[0][1]({ getItems: () => [{ name: "ML2c2" }] });
    expect(showNcscBox).toHaveBeenCalled();

    tokenfield.on.mock.calls[0][1]({ getItems: () => [{ name: "PL9002" }] });
    expect(hideNcscBox).toHaveBeenCalled();
  });
});
