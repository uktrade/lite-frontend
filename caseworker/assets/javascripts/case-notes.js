import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";
class CaseNote {
  constructor(
    $el,
    TEXTAREA_FOCUSED_CLASS,
    isUrgentCheckbox,
    mentionUsersSelector,
    cancelButtonSelector
  ) {
    this.TEXTAREA_FOCUSED_CLASS = TEXTAREA_FOCUSED_CLASS;
    this.$el = $el;
    this.$cancelButton = this.$el.querySelector(cancelButtonSelector);
    this.$submitButton = this.$el.querySelector("[type=submit]");
    this.$textarea = this.$el.querySelector("[name=text]");

    this.$isUrgentCheckbox = this.$el.querySelector(`#${isUrgentCheckbox}`);
    this.$isUrgentCheckboxDiv = this.$el.querySelector(
      `#div_${isUrgentCheckbox}`
    );

    this.$mentionUserInput = this.$el.querySelector(`#${mentionUsersSelector}`);
    this.$mentionUserInputDiv = this.$el.querySelector(
      `#div_${mentionUsersSelector}`
    );
  }

  init() {
    this.$el.addEventListener("submit", (evt) => this.handleSubmit(evt));
    this.$cancelButton.addEventListener("click", (evt) =>
      this.handleCancelButtonClick(evt)
    );
    this.$textarea.addEventListener("focus", (evt) =>
      this.handleTextareaFocus(evt)
    );
    this.$textarea.addEventListener("input", (evt) =>
      this.handleTextareaInput(evt)
    );
    this.$textarea.addEventListener("paste", (evt) =>
      this.handleTextareaInput(evt)
    );
    this.toggleSubmitButtonEnabled();
  }

  isMarkedAsVisibleForExporter() {
    return this.$isVisibleForExporterCheckbox.checked;
  }

  handleSubmit(evt) {
    if (!this.isMarkedAsVisibleForExporter()) {
      return;
    }

    const confirmed = confirm(
      "This note will be visible to the exporter, are you sure you wish to continue?"
    );
    if (!confirmed) {
      evt.preventDefault();
    }
  }

  handleCancelButtonClick(evt) {
    evt.preventDefault();
    this.$textarea.dispatchEvent(new Event("input"));
    this.toggleMentionFields(false);
    this.$el.reset();
    this.handleTextareaBlur();
  }

  handleTextareaFocus() {
    this.$textarea.classList.add(this.TEXTAREA_FOCUSED_CLASS);
    this.toggleMentionFields(true);
  }

  hasText() {
    return Boolean(this.$textarea.value);
  }

  shouldShrinkTextarea() {
    return !this.hasText();
  }

  handleTextareaBlur() {
    if (this.shouldShrinkTextarea()) {
      this.$textarea.classList.remove(this.TEXTAREA_FOCUSED_CLASS);
    }
  }

  toggleSubmitButtonEnabled() {
    this.$submitButton.disabled = !this.hasText();
  }

  displayToggle(element, show = true) {
    if (element) {
      element.style.display = "none";
      if (show) {
        element.style.display = "block";
      }
    }
  }

  toggleMentionFields(show = true) {
    this.displayToggle(this.$isUrgentCheckboxDiv, show);
    this.displayToggle(this.$mentionUserInputDiv, show);
  }

  handleTextareaInput() {
    this.toggleSubmitButtonEnabled();
  }
}

const initCaseNotesForm = () => {
  document
    .querySelectorAll("#case_notes")
    .forEach(($el) =>
      new CaseNote(
        $el,
        "case-note__textarea--focused",
        "id_is_urgent",
        "id_mentions",
        "#id_cancel"
      ).init()
    );
};

export default function initMentionUsers() {
  const mentionUserField = document.getElementById("id_mentions");

  if (!mentionUserField) return;

  const mentionUserTokenField = progressivelyEnhanceMultipleSelectField(
    mentionUserField,
    (option) => {
      return { id: option.value, name: option.label, classes: [] };
    }
  );
}

export { CaseNote, initCaseNotesForm, initMentionUsers };
