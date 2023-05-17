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

let component;
let displayContainer;

const createElements = () => {
  document.body.innerHTML = `
    <div id="display-container" style="display: none;"></div>
  `;

  return document.querySelector("#display-container");
};

const createComponent = () => {
  displayContainer = createElements();
  component = new ShowHideNcscField("#control_list_entries", displayContainer);
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
    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    component.toggleField();

    expect(displayContainer.style.display).toBe("revert");
  });

  test('setOnChangeListener hides ncscBox if "ML" is not present in tokenfield items', () => {
    const displayContainer = document.createElement("div");
    displayContainer.style.display = "revert";
    const checkboxInput = document.createElement("INPUT");
    checkboxInput.setAttribute("type", "checkbox");
    checkboxInput.checked = true;
    displayContainer.append(checkboxInput);
    const tokenfield = new MockTokenfield([{ name: "1e2" }]);

    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    const showHideNcscField = new ShowHideNcscField(
      "#control_list_entries",
      displayContainer
    );

    showHideNcscField.setOnChangeListener();
    tokenfield.emit("change");

    expect(displayContainer.style.display).toBe("none");
    expect(displayContainer.querySelector("input").checked).toBeFalsy();
  });

  test('setOnChangeListener hides ncscBox if "ML" is only at start of string in tokenfield items', () => {
    const displayContainer = document.createElement("div");
    displayContainer.style.display = "revert";
    const checkboxInput = document.createElement("INPUT");
    checkboxInput.setAttribute("type", "checkbox");
    checkboxInput.checked = true;
    displayContainer.append(checkboxInput);
    const tokenfield = new MockTokenfield([{ name: "123ML123" }]);

    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    const showHideNcscField = new ShowHideNcscField(
      "#control_list_entries",
      displayContainer
    );

    showHideNcscField.setOnChangeListener();
    tokenfield.emit("change");

    expect(displayContainer.style.display).toBe("none");
    expect(displayContainer.querySelector("input").checked).toBeFalsy();
  });

  test('setOnChangeListener shows ncscBox if "ML" is present in tokenfield items', () => {
    const displayContainer = document.createElement("div");
    displayContainer.style.display = "none";
    const tokenfield = new MockTokenfield([{ name: "ML123" }]);
    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    const showHideNcscField = new ShowHideNcscField(
      "#control_list_entries",
      displayContainer
    );

    showHideNcscField.setOnChangeListener();
    tokenfield.emit("change");

    expect(displayContainer.style.display).toBe("revert");
  });
});
