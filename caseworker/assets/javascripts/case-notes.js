import MultiSelector, { startsWith } from "core/multi-selector";

class CaseNote {
  TEXTAREA_FOCUSED_CLASS = "case-note__textarea--focused";
  constructor($el) {
    this.$el = $el;
    this.$mentions = this.$el.querySelector(".case-note-mentions");
    this.$cancelButton = this.$el.querySelector(".case-note-cancel");
    this.$submitButton = this.$el.querySelector("[type=submit]");
    this.$textarea = this.$el.querySelector("[name=text]");
  }

  init() {
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

  handleCancelButtonClick(evt) {
    evt.preventDefault();
    this.$el.reset();
    this.$textarea.dispatchEvent(new Event("input"));
    this.handleTextareaBlur();
    this.toggleMentionFields(false);
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
    this.displayToggle(this.$mentions, show);
  }

  handleTextareaInput() {
    this.toggleSubmitButtonEnabled();
  }
}

const initCaseNotes = () => {
  document
    .querySelectorAll("[data-module=case-note]")
    .forEach(($el) => new CaseNote($el).init());
};

const initMentionUsers = () => {
  const mentionUserField = document.getElementById("id_mentions");

  if (!mentionUserField) return;

  const multiSelector = new MultiSelector(mentionUserField, startsWith);
  multiSelector.init();
};

export { CaseNote, initCaseNotes, initMentionUsers };
