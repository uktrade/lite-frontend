import {
  fireEvent,
  getByLabelText,
  getByText,
  getAllByText,
} from "@testing-library/dom";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";
import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";
import { CaseNote } from "../case-notes";

let form;
let mentionForm;

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
  return new CaseNote(
    form,
    "case-note__textarea--focused",
    "[name=is-visible-to-exporter]",
    "",
    "",
    ".case-note__cancel-button"
  ).init();
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

  test("Blurring textarea doesn't remove focused class", async () => {
    const textarea = getByLabelText(form, "Add case note");
    expect(textarea).not.toHaveClass("case-note__textarea--focused");

    await userEvent.click(textarea);
    expect(textarea).toHaveClass("case-note__textarea--focused");

    textarea.blur();
    expect(textarea).toHaveClass("case-note__textarea--focused");
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

const createMentionsElement = () => {
  document.body.innerHTML = `
  <form method="post"> <input type="hidden" name="csrfmiddlewaretoken"
      value="">
    <div id="div_id_text" class="govuk-form-group"> <label for="id_text" class="govuk-label">
        Add a case note
      </label> <textarea name="text" cols="40" rows="2" class="govuk-textarea case-note__textarea"
        id="id_text"></textarea> </div>
    <div id="div_id_mentions" class="govuk-form-group tokenfield-container"> <label for="id_mentions" class="govuk-label">
        Mention a co-worker or team to notify them, or ask a question.
      </label>
      <div id="id_mentions_hint" class="govuk-hint">Type for suggestions. For example 'Technical Assessment Unit', NSCS,
        or 'Olivia Smith'</div>
      <div class="tokenfield tokenfield-mode-tokens" id="id_mentions">
        <input class="tokenfield-copy-helper" style="display:none;position:fixed;top:-1000px;right:1000px;" tabindex="-1"
          type="text">
        <div class="tokenfield-set">
          <ul></ul>
        </div>
        <input class="tokenfield-input" type="text" placeholder="" style="width: 100%;">
        <div class="tokenfield-suggest" style="display: none;">
          <ul class="tokenfield-suggest-list"></ul>
        </div>
        <div id="tokenfield-sizer-100df1ead9"
          style="width: auto; height: auto; overflow: hidden; white-space: pre; position: fixed; top: -10000px; left: 10000px;">
        </div>
      </div>
    </div>
    <div id="div_id_is_urgent" class="govuk-form-group">
      <div class="govuk-checkboxes govuk-checkboxes--small">
        <div class="govuk-checkboxes__item"> <input type="checkbox" name="is_urgent" class="govuk-checkboxes__input"
            id="id_is_urgent"> <label class="govuk-label govuk-checkboxes__label" for="id_is_urgent">
            Mark as urgent
          </label> </div>
      </div>
    </div> <input type="submit" name="submit" value="Add a case note" class="govuk-button" id="submit-id-submit"
      disabled="">
    <button name="cancel" class="govuk-button govuk-button--secondary" id="id_cancel"
      data-module="govuk-button">Cancel</button>
  </form>
  `;
  return document.querySelector("form");
};

const createMentionsComponent = () => {
  mentionForm = createMentionsElement();
  return new CaseNote(
    mentionForm,
    "case-note__textarea--focused",
    false,
    "id_is_urgent",
    "id_mentions",
    "#id_cancel"
  ).init();
};

describe("Case notes mentions", () => {
  beforeEach(() => {
    createMentionsComponent();
  });

  test("Focussing textarea sets focused class", async () => {
    const textarea = getByLabelText(mentionForm, "Add a case note");
    expect(textarea).not.toHaveClass("case-note__textarea--focused");

    await userEvent.click(textarea);
    expect(textarea).toHaveClass("case-note__textarea--focused");
  });

  test("Blurring textarea doesn't remove focused class", async () => {
    const textarea = getByLabelText(mentionForm, "Add a case note");
    expect(textarea).not.toHaveClass("case-note__textarea--focused");

    await userEvent.click(textarea);
    expect(textarea).toHaveClass("case-note__textarea--focused");

    textarea.blur();
    expect(textarea).toHaveClass("case-note__textarea--focused");
  });

  test("Blurring textarea with input keeps focused class", async () => {
    const textarea = getByLabelText(mentionForm, "Add a case note");
    expect(textarea).not.toHaveClass("case-note__textarea--focused");

    await userEvent.click(textarea);
    expect(textarea).toHaveClass("case-note__textarea--focused");

    await userEvent.type(textarea, "This is some text");
    textarea.blur();
    expect(textarea).toHaveClass("case-note__textarea--focused");
  });

  test("Cancel button resets", async () => {
    const textarea = getByLabelText(mentionForm, "Add a case note");
    await userEvent.click(textarea);
    await userEvent.type(textarea, "This is some text");

    const checkbox = getByLabelText(mentionForm, "Mark as urgent");
    await userEvent.click(checkbox);

    const cancelButton = getByText(mentionForm, "Cancel");
    await userEvent.click(cancelButton);

    expect(textarea).not.toHaveClass("case-note__textarea--focused");
    expect(textarea).not.toHaveFocus();
    expect(textarea).not.toHaveValue();

    expect(checkbox).not.toBeChecked();
  });

  test("Submit button is not enabled by default", () => {
    const submitButton = getAllByText(mentionForm, "Add a case note")[1];
    expect(submitButton).toBeDisabled();
  });

  test("Submit button enabled after adding text", async () => {
    const submitButton = getAllByText(mentionForm, "Add a case note")[1];
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(mentionForm, "Add a case note");
    await userEvent.click(textarea);
    await userEvent.type(textarea, "This is some text");

    expect(submitButton).not.toBeDisabled();
  });

  test("Submit button enabled after pasting text", async () => {
    const submitButton = getAllByText(mentionForm, "Add a case note")[1];
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(mentionForm, "Add a case note");
    await userEvent.click(textarea);
    fireEvent.paste(textarea, { target: { value: "Some pasted text" } });

    expect(submitButton).not.toBeDisabled();
  });

  test("Submit button disabled after removing text", async () => {
    const submitButton = getAllByText(mentionForm, "Add a case note")[1];
    console.log(submitButton);
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(mentionForm, "Add a case note");
    await userEvent.click(textarea);
    await userEvent.type(textarea, "This is some text");
    await userEvent.clear(textarea);

    expect(submitButton).toBeDisabled();
  });
});
