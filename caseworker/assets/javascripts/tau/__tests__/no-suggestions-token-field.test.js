import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import NoSuggestionsTokenField from "../no-suggestions-token-field";

let component, noCleCheckbox;

const createElements = () => {
  document.body.innerHTML = '<input type="checkbox" name="no-cle" />';

  noCleCheckbox = document.querySelector("[name=no-cle]");

  return [noCleCheckbox];
};

const createComponent = () => {
  createElements();
  component = new NoSuggestionsTokenField(noCleCheckbox);
  component.init();
  return component;
};

describe("No suggestions token field", () => {
  let user;

  beforeEach(() => {
    createComponent();
    user = userEvent.setup();
  });

  test("reset", () => {
    const onInputSpy = jest.fn();
    noCleCheckbox.addEventListener("input", () => onInputSpy());

    const onChangeSpy = jest.fn();
    component.on("change", (checked) => onChangeSpy(checked));

    noCleCheckbox.checked = true;
    component.reset();
    expect(noCleCheckbox.checked).toBeFalsy();
    expect(onInputSpy).toBeCalledTimes(1);
    expect(onChangeSpy).toBeCalledTimes(1);
    expect(onChangeSpy).toBeCalledWith(false);
  });

  test("onChange", async () => {
    const onChangeSpy = jest.fn();
    component.on("change", (checked) => onChangeSpy(checked));

    await user.click(noCleCheckbox);
    expect(onChangeSpy).toBeCalledTimes(1);
    expect(onChangeSpy).toBeCalledWith(true);

    await user.click(noCleCheckbox);
    expect(onChangeSpy).toBeCalledTimes(2);
    expect(onChangeSpy).toBeCalledWith(false);
  });
});
