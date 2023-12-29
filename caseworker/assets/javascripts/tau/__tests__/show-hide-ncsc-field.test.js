import "@testing-library/jest-dom";

import ShowHideNcscField from "../show-hide-ncsc-field";

let checkboxInput;
let component;
let displayContainer;

const createElements = () => {
  document.body.innerHTML = `
    <div id="display-container" style="display: none;">
      <input id="checkbox" type="checkbox" />
    </div>
  `;

  return [
    document.querySelector("#display-container"),
    document.querySelector("#checkbox"),
  ];
};

const createComponent = () => {
  [displayContainer, checkboxInput] = createElements();
  component = new ShowHideNcscField(displayContainer);
  return component;
};
describe("ShowHideNCSCField", () => {
  beforeEach(() => {
    createComponent();
  });

  test('showField sets the display property to "revert"', () => {
    displayContainer.style.display = "none";
    component.showField();
    expect(displayContainer.style.display).toEqual("revert");
  });

  test('hideField sets the display property to "none"', () => {
    displayContainer.style.display = "revert";
    component.hideField();
    expect(displayContainer.style.display).toEqual("none");
  });

  test.each([
    [[], "none"],
    [["123"], "none"],
    [["ML"], "revert"],
    [["ML123"], "revert"],
    [["123", "ML"], "revert"],
    [["123", "ML123"], "revert"],
  ])("toggleField with ratings '%s'", (ratings, display) => {
    component.toggleField(ratings);

    expect(displayContainer.style.display).toEqual(display);
  });

  test("toggleField resets checked", () => {
    checkboxInput.checked = true;
    component.toggleField([]);
    expect(checkboxInput.checked).toBeFalsy();
  });
});
