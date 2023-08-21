import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import SelectAllButton from "../select-all-button";

const createElements = () => {
  document.body.innerHTML = `
    <form id="form">
      <button id="button"></button>
    </form>
  `;

  return [document.querySelector("#button"), document.querySelector("#form")];
};

describe("Select all button", () => {
  test("Renders button text on init", () => {
    const [button] = createElements();

    new SelectAllButton(button).init();

    expect(button).toHaveTextContent("Select all");
  });

  test("Setting selected state", () => {
    const [button] = createElements();

    const selectAllButton = new SelectAllButton(button);
    selectAllButton.init();

    selectAllButton.setSelected(true);
    expect(button).toHaveTextContent("Deselect all");

    selectAllButton.setSelected(false);
    expect(button).toHaveTextContent("Select all");
  });

  test("Clicking sends event", async () => {
    const [button] = createElements();

    const selectAllButton = new SelectAllButton(button);
    selectAllButton.init();

    const callbackSpy = jest.fn();
    selectAllButton.on("click", callbackSpy);

    // The default is that this is "Select all"
    await userEvent.click(button);
    expect(callbackSpy).toHaveBeenCalledWith(true);
    callbackSpy.mockReset();

    selectAllButton.setSelected(true);
    await userEvent.click(button);
    expect(callbackSpy).toHaveBeenCalledWith(false);
    callbackSpy.mockReset();

    selectAllButton.setSelected(false);
    await userEvent.click(button);
    expect(callbackSpy).toHaveBeenCalledWith(true);
    callbackSpy.mockReset();
  });

  test("Form not submitted on button click", async () => {
    const [button, form] = createElements();

    const selectAllButton = new SelectAllButton(button);
    selectAllButton.init();

    const submitSpy = jest.fn();
    form.addEventListener("submit", submitSpy);

    await userEvent.click(button);

    expect(submitSpy).not.toHaveBeenCalled();
  });
});
