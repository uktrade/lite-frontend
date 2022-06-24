class CaseNote {
  TEXTAREA_FOCUSED_CLASS = "case-note__textarea--focused";

  constructor($el) {
    this.$el = $el;

    this.$isVisibleForExporterCheckbox = this.$el.querySelector(
      "[name=is-visible-to-exporter]"
    );
    this.$cancelButton = this.$el.querySelector(".case-note__cancel-button");
    this.$textarea = this.$el.querySelector("[name=text]");
  }

  init() {
    this.$el.addEventListener("submit", (evt) => this.handleSubmit(evt));
    this.$cancelButton.addEventListener("click", (evt) =>
      this.handleCancelButtonClick(evt)
    );
    this.$textarea.addEventListener("focus", (evt) =>
      this.handleTextareaFocus(evt)
    );
    this.$textarea.addEventListener("blur", (evt) =>
      this.handleTextareaBlur(evt)
    );
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
    this.$textarea.value = "";
    this.$textarea.dispatchEvent(new Event("blur"));
  }

  handleTextareaFocus() {
    this.$textarea.classList.add(this.TEXTAREA_FOCUSED_CLASS);
  }

  shouldShrinkTextarea() {
    return !this.$textarea.value;
  }

  handleTextareaBlur() {
    if (this.shouldShrinkTextarea()) {
      this.$textarea.classList.remove(this.TEXTAREA_FOCUSED_CLASS);
    }
  }
}

const initCaseNotes = () => {
  document
    .querySelectorAll("[data-module=case-note]")
    .forEach(($el) => new CaseNote($el).init());
};

export default initCaseNotes;
