import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import SelectAll from "../select-all";

let selectAllButton, checkboxes;

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <button class="select-all-button">Select all</button>
      <div class="checkboxes">
        <input type="checkbox" name="checkbox-1" value="checkbox-1" />
        <input type="checkbox" name="checkbox-2" value="checkbox-2" />
        <input type="checkbox" name="checkbox-3" value="checkbox-3" />
      </div>
    </div>
  `;

  const _selectAllButton = document.querySelector(".select-all-button");
  const _checkboxes = document.querySelectorAll("[type=checkbox]");

  return [_selectAllButton, _checkboxes];
};

const createComponent = () => {
  [selectAllButton, checkboxes] = createElements();
  return new SelectAll(selectAllButton, checkboxes).init();
};

test("Checkboxes set before init sets button text", () => {
  [selectAllButton, checkboxes] = createElements();
  checkboxes.forEach((checkbox) => (checkbox.checked = true));
  new SelectAll(selectAllButton, checkboxes).init();
  expect(selectAllButton).toHaveTextContent("Deselect all");
});

describe("Select all", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Clicking select all", async () => {
    await userEvent.click(selectAllButton);
    expect(selectAllButton).toHaveTextContent("Deselect all");
    for (const checkbox of checkboxes) {
      expect(checkbox).toBeChecked();
    }
  });

  test("Clicking select all and then deselect all", async () => {
    await userEvent.click(selectAllButton);
    expect(selectAllButton).toHaveTextContent("Deselect all");
    for (const checkbox of checkboxes) {
      expect(checkbox).toBeChecked();
    }

    await userEvent.click(selectAllButton);
    expect(selectAllButton).toHaveTextContent("Select all");
    for (const checkbox of checkboxes) {
      expect(checkbox).not.toBeChecked();
    }
  });

  test("Checking all sets button", async () => {
    for (const checkbox of checkboxes) {
      await userEvent.click(checkbox);
    }
    expect(selectAllButton).toHaveTextContent("Deselect all");
  });

  test("Checking all then unchecking one sets button", async () => {
    for (const checkbox of checkboxes) {
      await userEvent.click(checkbox);
    }
    await userEvent.click(checkboxes[0]);
    expect(selectAllButton).toHaveTextContent("Select all");
  });

  test("Input events called when selecting selecting all", async () => {
    for (const checkbox of checkboxes) {
      const inputSpy = jest.fn();
      checkbox.addEventListener("input", () => inputSpy());
      await userEvent.click(checkbox);
      expect(inputSpy).toHaveBeenCalled();
    }
  });
});
