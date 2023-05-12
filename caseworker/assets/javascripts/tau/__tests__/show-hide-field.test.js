import "@testing-library/jest-dom";

import ShowHideFormField from "../show-hide-field";

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
  component = new ShowHideFormField(displayContainer);
  return component;
};
describe("ShowHideFormField", () => {
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
});
