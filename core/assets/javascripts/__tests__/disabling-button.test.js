import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import DisablingButton from "../disabling-button";

const createComponent = (button) => {
  return new DisablingButton(button);
};

describe("Disabling button", () => {
  test("Clicking input button disables it", async () => {
    document.body.innerHTML = `<input id="button" value="Input" />`;

    const button = document.querySelector("#button");
    const component = createComponent(button);

    component.init();
    await userEvent.click(button);
    expect(button).toBeDisabled();
  });

  test("Clicking button button disables it", async () => {
    document.body.innerHTML = `<button id="button">Button</button>`;

    const button = document.querySelector("#button");
    const component = createComponent(button);

    component.init();
    await userEvent.click(button);
    expect(button).toBeDisabled();
  });

  test("Clicking allows for to submit", async () => {
    document.body.innerHTML = `
      <form id="form">
        <input id="button" type="submit" value="Submit" />
      </form>
    `;

    const form = document.querySelector("#form");
    const button = document.querySelector("#button");
    const component = createComponent(button);

    const submitSpy = jest.fn();
    form.addEventListener("submit", (evt) => {
      evt.preventDefault();
      submitSpy();
    });

    component.init();
    await userEvent.click(button);
    expect(submitSpy).toBeCalled();
  });
});
