import {
  fireEvent,
  getByLabelText,
  getByText,
  getAllByText,
  getByDisplayValue,
} from "@testing-library/dom";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";
import { CaseNote } from "../case-notes";

let mentionForm;

const createMentionsElement = () => {
  document.body.innerHTML = `
  <form data-module="case-note" method="post">
    <input type="hidden" name="csrfmiddlewaretoken"/>
    <div id="div_id_text" class="govuk-form-group">
      <label for="id_text" class="govuk-label"> Add a case note </label>
      <textarea name="text" cols="40" rows="2" class="govuk-textarea case-note__textarea" id="id_text"></textarea>
    </div>
    <div class="case-note-mentions">
      <div id="div_id_mentions" class="govuk-form-group tokenfield-container">
        <label for="id_mentions" class="govuk-label">
          Mention a co-worker to notify them, or ask a question (optional)
        </label>
        <div id="id_mentions_hint" class="govuk-hint">
          Type for suggestions. For example 'Technical Assessment Unit', NSCS, or
          'Olivia Smith'
        </div>
        <div class="tokenfield tokenfield-mode-tokens" id="id_mentions">
          <input class="tokenfield-copy-helper" style="display: none; position: fixed; top: -1000px; right: 1000px"
            tabindex="-1" type="text" />
          <div class="tokenfield-set">
            <ul></ul>
          </div>
          <input class="tokenfield-input" type="text" placeholder="" style="width: 100%" />
          <div class="tokenfield-suggest" style="display: none">
            <ul class="tokenfield-suggest-list"></ul>
          </div>
          <div id="tokenfield-sizer-105d31c371" style="
              width: auto;
              height: auto;
              overflow: hidden;
              white-space: pre;
              position: fixed;
              top: -10000px;
              left: 10000px;
            "></div>
        </div>
      </div>
      <div id="div_id_is_urgent" class="govuk-form-group">
        <div class="govuk-checkboxes govuk-checkboxes--small">
          <div class="govuk-checkboxes__item">
            <input type="checkbox" name="is_urgent" class="govuk-checkboxes__input" id="id_is_urgent" />
            <label class="govuk-label govuk-checkboxes__label" for="id_is_urgent">
              Mark as urgent
            </label>
          </div>
        </div>
      </div>
    </div>
    <div class="case-note__controls-buttons">
      <input type="submit" name="submit" value="Add a case note" class="govuk-button" id="submit-id-submit" disabled="" />
      <a id="id_cancel"
        class="govuk-body govuk-link govuk-link--no-visited-state case-note-cancel" type="button" draggable="false">
        Cancel
      </a>
    </div>
  </form>
  `;
  return document.querySelector("form");
};

const createMentionsComponent = () => {
  mentionForm = createMentionsElement();
  return new CaseNote(mentionForm).init();
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
    const submitButton = getByDisplayValue(mentionForm, "Add a case note");
    expect(submitButton).toBeDisabled();
  });

  test("Submit button enabled after adding text", async () => {
    const submitButton = getByDisplayValue(mentionForm, "Add a case note");
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(mentionForm, "Add a case note");
    await userEvent.click(textarea);
    await userEvent.type(textarea, "This is some text");

    expect(submitButton).not.toBeDisabled();
  });

  test("Submit button enabled after pasting text", async () => {
    const submitButton = getByDisplayValue(mentionForm, "Add a case note");
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(mentionForm, "Add a case note");
    await userEvent.click(textarea);
    fireEvent.paste(textarea, { target: { value: "Some pasted text" } });

    expect(submitButton).not.toBeDisabled();
  });

  test("Submit button disabled after removing text", async () => {
    const submitButton = getByDisplayValue(mentionForm, "Add a case note");
    expect(submitButton).toBeDisabled();

    const textarea = getByLabelText(mentionForm, "Add a case note");
    await userEvent.click(textarea);
    await userEvent.type(textarea, "This is some text");
    await userEvent.clear(textarea);

    expect(submitButton).toBeDisabled();
  });
});
