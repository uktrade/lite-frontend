import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import SelectAllCheckbox from "../select-all-checkbox";

const createElements = () => {
  document.body.innerHTML = `
    <input id="checkbox" type="checkbox">
    <label id="label"></label>
  `;

  return [
    document.querySelector("#checkbox"),
    document.querySelector("#label"),
  ];
};

describe("Select all checkbox", () => {
  test("Renders label text on init", () => {
    const [checkbox, label] = createElements();

    new SelectAllCheckbox(checkbox, label).init();

    expect(label).toHaveTextContent("Select all");
  });

  test("Setting selected state", () => {
    const [checkbox, label] = createElements();

    const selectAllCheckbox = new SelectAllCheckbox(checkbox, label);
    selectAllCheckbox.init();

    selectAllCheckbox.setSelected(true);
    expect(label).toHaveTextContent("Deselect all");
    expect(checkbox).toBeChecked();

    selectAllCheckbox.setSelected(false);
    expect(label).toHaveTextContent("Select all");
    expect(checkbox).not.toBeChecked();
  });

  test("Clicking sends event", async () => {
    const [checkbox, label] = createElements();

    const selectAllCheckbox = new SelectAllCheckbox(checkbox, label);
    selectAllCheckbox.init();

    const callbackSpy = jest.fn();
    selectAllCheckbox.on("change", callbackSpy);

    // The default is that this is "Select all"
    await userEvent.click(checkbox);
    expect(callbackSpy).toHaveBeenCalledWith(true);
    callbackSpy.mockReset();

    selectAllCheckbox.setSelected(true);
    await userEvent.click(checkbox);
    expect(callbackSpy).toHaveBeenCalledWith(false);
    callbackSpy.mockReset();

    selectAllCheckbox.setSelected(false);
    await userEvent.click(checkbox);
    expect(callbackSpy).toHaveBeenCalledWith(true);
    callbackSpy.mockReset();
  });

  test("Keyboard events send event", async () => {
    const [checkbox, label] = createElements();

    const selectAllCheckbox = new SelectAllCheckbox(checkbox, label);
    selectAllCheckbox.init();

    const callbackSpy = jest.fn();
    selectAllCheckbox.on("change", callbackSpy);

    // The default is that this is "Select all"
    checkbox.focus();
    await userEvent.keyboard("[Space]");
    expect(callbackSpy).toHaveBeenCalledWith(true);
    callbackSpy.mockReset();

    selectAllCheckbox.setSelected(true);
    await userEvent.keyboard("[Space]");
    expect(callbackSpy).toHaveBeenCalledWith(false);
    callbackSpy.mockReset();

    selectAllCheckbox.setSelected(false);
    await userEvent.keyboard("[Space]");
    expect(callbackSpy).toHaveBeenCalledWith(true);
    callbackSpy.mockReset();
  });
});
