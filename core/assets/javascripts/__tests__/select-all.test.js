import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import SelectAll from "../select-all";

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

describe("Select all", () => {
  test("Checkboxes set before init calls callback", () => {
    const allSelectedSpy = jest.fn();
    checkboxes = createElements();
    checkboxes.forEach((checkbox) => (checkbox.checked = true));

    new SelectAll(checkboxes, allSelectedSpy).init();

    expect(allSelectedSpy).toBeCalledTimes(1);
    expect(allSelectedSpy).toBeCalledWith(true);
  });

  test("Checkboxes partially selected before init calls callback", () => {
    checkboxes[0].checked = true;
    const allSelectedSpy = jest.fn();
    checkboxes = createElements();

    new SelectAll(checkboxes, allSelectedSpy).init();

    expect(allSelectedSpy).toBeCalledTimes(1);
    expect(allSelectedSpy).toBeCalledWith(false);
  });

  test("Toggling checkboxes calls callback only if change in state", async () => {
    const allSelectedSpy = jest.fn();
    checkboxes = createElements();

    new SelectAll(checkboxes, allSelectedSpy).init();

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

  describe("Calling selectAll", () => {
    let selectAll, allSelectedSpy, inputSpies;

    beforeEach(() => {
      allSelectedSpy = jest.fn();
      checkboxes = createElements();
      inputSpies = [];
      for (const checkbox of checkboxes) {
        const inputSpy = jest.fn();
        checkbox.addEventListener("input", inputSpy);
        inputSpies.push(inputSpy);
      }

      selectAll = new SelectAll(checkboxes, allSelectedSpy);
      selectAll.init();
      allSelectedSpy.mockReset();
    });

    test("Selects all checkboxes", () => {
      selectAll.selectAll();

      for (const checkbox of checkboxes) {
        expect(checkbox).toBeChecked();
      }
    });

    test("Calls callback", () => {
      selectAll.selectAll();

      expect(allSelectedSpy).toBeCalledTimes(1);
      expect(allSelectedSpy).toBeCalledWith(true);
    });

    test("Input events called on checkboxes", () => {
      selectAll.selectAll();

      for (const inputSpy of inputSpies) {
        expect(inputSpy).toBeCalled();
      }
    });
  });

  describe("Calling deselectAll", () => {
    let selectAll, allSelectedSpy, inputSpies;

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

      selectAll = new SelectAll(checkboxes, allSelectedSpy);
      selectAll.init();
      allSelectedSpy.mockReset();
    });

    test("Deselects all checkboxes", () => {
      selectAll.deselectAll();

      for (const checkbox of checkboxes) {
        expect(checkbox).not.toBeChecked();
      }
    });

    test("Calls callback", () => {
      selectAll.deselectAll();

      expect(allSelectedSpy).toBeCalledTimes(1);
      expect(allSelectedSpy).toBeCalledWith(false);
    });

    test("Input events called on checkboxes", () => {
      selectAll.selectAll();

      for (const inputSpy of inputSpies) {
        expect(inputSpy).toBeCalled();
      }
    });
  });
});
