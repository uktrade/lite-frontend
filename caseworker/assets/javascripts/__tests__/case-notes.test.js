import { fireEvent, getByLabelText, getByText } from "@testing-library/dom";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";

import { CaseNote } from "../case-notes";

let form;

const createElement = () => {
  document.body.innerHTML = `
    <form class="notes-and-timeline-case-note" data-module="case-note" method="post">
      <div class="notes-and-timeline-case-note__wrapper">
        <label class="govuk-label govuk-visually-hidden" for="input-case-note">
          Add case note
        </label>
        <div class="case-note__container">
          <textarea id="input-case-note" name="text" cols="80" class="govuk-textarea case-note__textarea"></textarea>
          <div class="case-note__controls">
            <div class="govuk-checkboxes govuk-checkboxes--small">
              <div class="govuk-checkboxes__item">
                <input class="govuk-checkboxes__input" type="checkbox" id="is-visible-to-exporter" name="is-visible-to-exporter" value="True">
                <label class="govuk-label govuk-checkboxes__label" for="is-visible-to-exporter">
                  Make visible to exporter
                </label>
              </div>
            </div>
            <div class="case-note__controls-buttons">
              <a id="link-case-note-cancel" href="/" class="govuk-body govuk-link govuk-link--no-visited-state case-note__cancel-button" type="button" draggable="false">
                Cancel
              </a>
              <button id="button-case-note-post" class="govuk-button" type="submit">
                Add a case note
              </button>
            </div>
          </div>
        </div>
      </div>
    </form>
  `;
  return document.querySelector("form");
};

const createComponent = () => {
  form = createElement();
  return new CaseNote(form).init();
};

describe("Case notes", () => {
  beforeEach(() => {
    createComponent();
  });

  test("Focussing textarea sets focused class", async () => {
    const textarea = getByLabelText(form, "Add case note");
    expect(textarea).not.toHaveClass("case-note__textarea--focused");

    await userEvent.click(textarea);
    expect(textarea).toHaveClass("case-note__textarea--focused");
  });

  test("Blurring textarea removes focused class", async () => {
    const textarea = getByLabelText(form, "Add case note");
    expect(textarea).not.toHaveClass("case-note__textarea--focused");

    await userEvent.click(textarea);
    expect(textarea).toHaveClass("case-note__textarea--focused");

    textarea.blur();
    expect(textarea).not.toHaveClass("case-note__textarea--focused");
  });

  test("Blurring textarea with input keeps focused class", async () => {
    const textarea = getByLabelText(form, "Add case note");
    expect(textarea).not.toHaveClass("case-note__textarea--focused");

    await userEvent.click(textarea);
    expect(textarea).toHaveClass("case-note__textarea--focused");

    await userEvent.type(textarea, "This is some text");
    textarea.blur();
    expect(textarea).toHaveClass("case-note__textarea--focused");
  });

  test("Submitting with 'Is visible to exporter' raises confirmation", async () => {
    const confirmSpy = jest.spyOn(window, "confirm");
    confirmSpy.mockImplementation(jest.fn(() => false));

    const textarea = getByLabelText(form, "Add case note");
    await userEvent.type(textarea, "This is some text");

    const checkbox = getByLabelText(form, "Make visible to exporter");
    await userEvent.click(checkbox);

    const submitButton = getByText(form, "Add a case note");
    await userEvent.click(submitButton);

    expect(confirmSpy).toHaveBeenCalledWith(
      "This note will be visible to the exporter, are you sure you wish to continue?"
    );
    confirmSpy.mockReset();
  });

  test("Submitting without 'Is visible to exporter' does not raise confirmation", async () => {
    form.addEventListener("submit", (evt) => {
      evt.preventDefault();
    });

    const confirmSpy = jest.spyOn(window, "confirm");
    confirmSpy.mockImplementation(jest.fn(() => false));

    const textarea = getByLabelText(form, "Add case note");
    await userEvent.type(textarea, "This is some text");

    const submitButton = getByText(form, "Add a case note");
    await userEvent.click(submitButton);

    expect(confirmSpy).not.toHaveBeenCalled();
  });

  test("Cancel button resets", async () => {
    const textarea = getByLabelText(form, "Add case note");
    await userEvent.click(textarea);
    await userEvent.type(textarea, "This is some text");

    const checkbox = getByLabelText(form, "Make visible to exporter");
    await userEvent.click(checkbox);

    const submitButton = getByText(form, "Add a case note");
    await userEvent.click(submitButton);

    const cancelButton = getByText(form, "Cancel");
    await userEvent.click(cancelButton);

    expect(textarea).not.toHaveClass("case-note__textarea--focused");
    expect(textarea).not.toHaveFocus();
    expect(textarea).not.toHaveValue();

    expect(checkbox).not.toBeChecked();
  });

  test("Submit button is not enabled by default", () => {
    const submitButton = getByText(form, "Add a case note");
    expect(submitButton).toBeDisabled();
  });

  test("Submit button enabled after adding text", async () => {
    const submitButton = getByText(form, "Add a case note");
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(form, "Add case note");
    await userEvent.click(textarea);
    await userEvent.type(textarea, "This is some text");

    expect(submitButton).not.toBeDisabled();
  });

  test("Submit button enabled after pasting text", async () => {
    const submitButton = getByText(form, "Add a case note");
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(form, "Add case note");
    await userEvent.click(textarea);
    fireEvent.paste(textarea, { target: { value: "Some pasted text" } });

    expect(submitButton).not.toBeDisabled();
  });

  test("Submit button disabled after removing text", async () => {
    const submitButton = getByText(form, "Add a case note");
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(form, "Add case note");
    await userEvent.click(textarea);
    await userEvent.type(textarea, "This is some text");
    await userEvent.clear(textarea);

    expect(submitButton).toBeDisabled();
  });
});
