import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import CheckboxClassToggler from "../checkbox-class-toggler";

let checkboxes, toToggleClass;

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <div id="checkboxes">
        <input type="checkbox" name="checkbox-1" value="checkbox-1" />
        <input type="checkbox" name="checkbox-2" value="checkbox-2" />
        <input type="checkbox" name="checkbox-3" value="checkbox-3" />
      </div>
      <div id="to-toggle-class">
      </div>
    </div>
  `;

  const _checkboxes = document.querySelectorAll("[type=checkbox]");
  const _toToggleClass = document.querySelector("#to-toggle-class");

  return [_checkboxes, _toToggleClass];
};

const createComponent = () => {
  [checkboxes, toToggleClass] = createElements();
  return new CheckboxClassToggler(checkboxes, toToggleClass, "add-me").init();
};

test("All checked on init doesn't add class", () => {
  [checkboxes, toToggleClass] = createElements();
  for (const checkbox of checkboxes) {
    checkbox.checked = true;
  }
  new CheckboxClassToggler(checkboxes, toToggleClass, "add-me").init();
  expect(toToggleClass).not.toHaveClass("add-me");
});

describe("Checkbox class toggler", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Init without checked checkboxes adds class", () => {
    new CheckboxClassToggler(checkboxes, toToggleClass, "add-me").init();
    expect(toToggleClass).toHaveClass("add-me");
  });

  test("Clicking checkbox doesn't add class", async () => {
    await userEvent.click(checkboxes[0]);
    expect(toToggleClass).not.toHaveClass("add-me");
  });

  test("Clicking checkbox then unlclicking adds class", async () => {
    await userEvent.click(checkboxes[0]);
    expect(toToggleClass).not.toHaveClass("add-me");

    await userEvent.click(checkboxes[0]);
    expect(toToggleClass).toHaveClass("add-me");
  });

  test("Checking all retains no class", async () => {
    for (const checkbox of checkboxes) {
      await userEvent.click(checkbox);
    }
    expect(toToggleClass).not.toHaveClass("add-me");
  });

  test("Partially checked retains no class", async () => {
    for (const checkbox of checkboxes) {
      await userEvent.click(checkbox);
    }
    await userEvent.click(checkboxes[0]);
    expect(toToggleClass).not.toHaveClass("add-me");
  });
});
