import "@testing-library/jest-dom";

import ShowHideNcscField from "../show-hide-ncsc-field";

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

  test('hideFieldAtLoad shows ncscBox if "ML" is present in tokenfield items at load', () => {
    const tokenfield = {
      getItems: jest.fn().mockReturnValue([{ name: "ML2c2" }]),
    };
    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    component.hideFieldAtLoad();

    expect(displayContainer.style.display).toBe("revert");
  });

  test('setOnChangeListener hides ncscBox if "ML" is not present in tokenfield items', () => {
    const displayContainer = document.createElement("div");
    displayContainer.style.display = "revert";
    const checkboxInput = document.createElement("INPUT");
    checkboxInput.setAttribute("type", "checkbox");
    checkboxInput.checked = true;
    displayContainer.append(checkboxInput);

    const tokenfield = {
      on: jest.fn().mockImplementation((event, callback) => {
        callback();
      }),
      getItems: jest.fn().mockReturnValue([{ name: "1e2" }]),
    };

    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    const showHideNcscField = new ShowHideNcscField(
      "#control_list_entries",
      displayContainer
    );
    showHideNcscField.setOnChangeListener();

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

    const tokenfield = {
      on: jest.fn().mockImplementation((event, callback) => {
        callback();
      }),
      getItems: jest.fn().mockReturnValue([{ name: "123ML123" }]),
    };

    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    const showHideNcscField = new ShowHideNcscField(
      "#control_list_entries",
      displayContainer
    );
    showHideNcscField.setOnChangeListener();

    expect(displayContainer.style.display).toBe("none");
    expect(displayContainer.querySelector("input").checked).toBeFalsy();
  });

  test('setOnChangeListener shows ncscBox if "ML" is present in tokenfield items', () => {
    const displayContainer = document.createElement("div");
    const tokenfield = {
      on: jest.fn().mockImplementation((event, callback) => {
        callback();
      }),
      getItems: jest.fn().mockReturnValue([{ name: "ML2c2" }]),
    };
    jest.spyOn(document, "querySelector").mockReturnValue({ tokenfield });

    const showHideNcscField = new ShowHideNcscField(
      "#control_list_entries",
      displayContainer
    );

    showHideNcscField.setOnChangeListener();

    expect(displayContainer.style.display).toBe("revert");
  });
});
