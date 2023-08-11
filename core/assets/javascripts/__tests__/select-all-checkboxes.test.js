import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import SelectAllCheckboxes from "../select-all-checkboxes";

let checkboxes;

const createElements = () => {
  document.body.innerHTML = `
    <div>
      <div class="checkboxes">
        <input type="checkbox" name="checkbox-1" value="checkbox-1" />
        <input type="checkbox" name="checkbox-2" value="checkbox-2" />
        <input type="checkbox" name="checkbox-3" value="checkbox-3" />
      </div>
    </div>
  `;

  const _checkboxes = document.querySelectorAll("[type=checkbox]");

  return _checkboxes;
};

describe("Select all checkboxes", () => {
  test("Checkboxes set before init emits event", () => {
    const allSelectedSpy = jest.fn();
    checkboxes = createElements();
    checkboxes.forEach((checkbox) => (checkbox.checked = true));

    const selectAllCheckboxes = new SelectAllCheckboxes(checkboxes);
    selectAllCheckboxes.on("change", allSelectedSpy);
    selectAllCheckboxes.init();

    expect(allSelectedSpy).toBeCalledTimes(1);
    expect(allSelectedSpy).toBeCalledWith(true);
  });

  test("Checkboxes partially selected before init emits event", () => {
    checkboxes[0].checked = true;
    const allSelectedSpy = jest.fn();
    checkboxes = createElements();

    const selectAllCheckboxes = new SelectAllCheckboxes(checkboxes);
    selectAllCheckboxes.on("change", allSelectedSpy);
    selectAllCheckboxes.init();

    expect(allSelectedSpy).toBeCalledTimes(1);
    expect(allSelectedSpy).toBeCalledWith(false);
  });

  test("Toggling checkboxes emits event only if change in state", async () => {
    const allSelectedSpy = jest.fn();
    checkboxes = createElements();

    const selectAllCheckboxes = new SelectAllCheckboxes(checkboxes);
    selectAllCheckboxes.on("change", allSelectedSpy);
    selectAllCheckboxes.init();

    expect(allSelectedSpy).toBeCalledTimes(1);
    expect(allSelectedSpy).toBeCalledWith(false);

    await userEvent.click(checkboxes[0]);
    expect(allSelectedSpy).toBeCalledTimes(1);
    expect(allSelectedSpy).toBeCalledWith(false);

    await userEvent.click(checkboxes[1]);
    expect(allSelectedSpy).toBeCalledTimes(1);

    await userEvent.click(checkboxes[2]);
    expect(allSelectedSpy).toBeCalledTimes(2);
    expect(allSelectedSpy).toBeCalledWith(true);

    await userEvent.click(checkboxes[2]);
    expect(allSelectedSpy).toBeCalledTimes(3);
    expect(allSelectedSpy).toBeCalledWith(false);
  });

  describe("Selecting all", () => {
    let selectAllCheckboxes, allSelectedSpy, inputSpies;

    beforeEach(() => {
      allSelectedSpy = jest.fn();
      checkboxes = createElements();
      inputSpies = [];
      for (const checkbox of checkboxes) {
        const inputSpy = jest.fn();
        checkbox.addEventListener("input", inputSpy);
        inputSpies.push(inputSpy);
      }

      selectAllCheckboxes = new SelectAllCheckboxes(checkboxes);
      selectAllCheckboxes.on("change", allSelectedSpy);
      selectAllCheckboxes.init();
      allSelectedSpy.mockReset();
    });

    test("Selects all checkboxes", () => {
      selectAllCheckboxes.selectAll(true);

      for (const checkbox of checkboxes) {
        expect(checkbox).toBeChecked();
      }
    });

    test("Calls callback", () => {
      selectAllCheckboxes.selectAll(true);

      expect(allSelectedSpy).toBeCalledTimes(1);
      expect(allSelectedSpy).toBeCalledWith(true);
    });

    test("Input events called on checkboxes", () => {
      selectAllCheckboxes.selectAll(true);

      for (const inputSpy of inputSpies) {
        expect(inputSpy).toBeCalled();
      }
    });
  });

  describe("Deselecting all", () => {
    let selectAllCheckboxes, allSelectedSpy, inputSpies;

    beforeEach(() => {
      allSelectedSpy = jest.fn();
      checkboxes = createElements();
      for (const checkbox of checkboxes) {
        checkbox.checked = true;
      }
      inputSpies = [];
      for (const checkbox of checkboxes) {
        const inputSpy = jest.fn();
        checkbox.addEventListener("input", inputSpy);
        inputSpies.push(inputSpy);
      }

      selectAllCheckboxes = new SelectAllCheckboxes(checkboxes);
      selectAllCheckboxes.on("change", allSelectedSpy);
      selectAllCheckboxes.init();
      allSelectedSpy.mockReset();
    });

    test("Deselects all checkboxes", () => {
      selectAllCheckboxes.selectAll(false);

      for (const checkbox of checkboxes) {
        expect(checkbox).not.toBeChecked();
      }
    });

    test("Calls callback", () => {
      selectAllCheckboxes.selectAll(false);

      expect(allSelectedSpy).toBeCalledTimes(1);
      expect(allSelectedSpy).toBeCalledWith(false);
    });

    test("Input events called on checkboxes", () => {
      selectAllCheckboxes.selectAll(false);

      for (const inputSpy of inputSpies) {
        expect(inputSpy).toBeCalled();
      }
    });
  });
});
