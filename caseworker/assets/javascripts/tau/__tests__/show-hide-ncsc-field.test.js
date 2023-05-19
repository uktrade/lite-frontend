import "@testing-library/jest-dom";

import EventEmitter from "events";

import ShowHideNcscField from "../show-hide-ncsc-field";

class MockTokenfield extends EventEmitter {
  constructor(mockCLEArray) {
    super();
    this.mockCLEArray = mockCLEArray;
  }

  getItems() {
    return this.mockCLEArray;
  }
}

let checkboxInput;
let component;
let displayContainer;
let tokenFieldElement;

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <div id="token-field"></div>
      <div id="display-container" style="display: none;">
        <input id="checkbox" type="checkbox" />
      </div>
    </div>
  `;

  return [
    document.querySelector("#token-field"),
    document.querySelector("#display-container"),
    document.querySelector("#checkbox"),
  ];
};

const createComponent = () => {
  [tokenFieldElement, displayContainer, checkboxInput] = createElements();
  component = new ShowHideNcscField("#token-field", displayContainer);
  return component;
};
describe("ShowHideNCSCField", () => {
  beforeEach(() => {
    createComponent();
  });

  test('showField sets the display property to "revert"', () => {
    component.showField();
    expect(displayContainer.style.display).toBe("revert");
  });

  test('hideField sets the display property to "none"', () => {
    component.hideField();
    expect(displayContainer.style.display).toBe("none");
  });

  test('toggleField shows ncscBox if "ML" is present in tokenfield items', () => {
    const tokenfield = new MockTokenfield([{ name: "ML2c2" }]);
    tokenFieldElement.tokenfield = tokenfield;

    component.toggleField();

    expect(displayContainer.style.display).toBe("revert");
  });

  test('setOnChangeListener hides ncscBox if "ML" is not present in tokenfield items', () => {
    displayContainer.style.display = "revert";
    checkboxInput.setAttribute("type", "checkbox");
    checkboxInput.checked = true;

    const tokenfield = new MockTokenfield([{ name: "1e2" }]);
    tokenFieldElement.tokenfield = tokenfield;

    const showHideNcscField = new ShowHideNcscField(
      "#token-field",
      displayContainer
    );

    showHideNcscField.setOnChangeListener();
    tokenfield.emit("change");

    expect(displayContainer.style.display).toBe("none");
    expect(displayContainer.querySelector("input").checked).toBeFalsy();
  });

  test('setOnChangeListener hides ncscBox if "ML" is only at start of string in tokenfield items', () => {
    displayContainer.style.display = "revert";
    checkboxInput.setAttribute("type", "checkbox");
    checkboxInput.checked = true;

    const tokenfield = new MockTokenfield([{ name: "123ML123" }]);
    tokenFieldElement.tokenfield = tokenfield;

    const showHideNcscField = new ShowHideNcscField(
      "#token-field",
      displayContainer
    );

    showHideNcscField.setOnChangeListener();
    tokenfield.emit("change");

    expect(displayContainer.style.display).toBe("none");
    expect(displayContainer.querySelector("input").checked).toBeFalsy();
  });

  test('setOnChangeListener shows ncscBox if "ML" is present in tokenfield items', () => {
    displayContainer.style.display = "none";
    const tokenfield = new MockTokenfield([{ name: "ML123" }]);
    tokenFieldElement.tokenfield = tokenfield;

    const showHideNcscField = new ShowHideNcscField(
      "#token-field",
      displayContainer
    );

    showHideNcscField.setOnChangeListener();
    tokenfield.emit("change");

    expect(displayContainer.style.display).toBe("revert");
  });
});
