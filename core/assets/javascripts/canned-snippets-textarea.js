class PopulateTextOnAddButtonsClick {
  constructor($el) {
    this.$addButtons = $el.querySelectorAll("a[data-snippet-key]");
    this.$textArea = $el.querySelector("textarea");
    this.$lookup = JSON.parse(
      $el.querySelector(`#${this.$textArea.name}`).textContent,
    );
  }

  init() {
    this.$addButtons.forEach((input) => {
      input.addEventListener("click", (event) => {
        event.preventDefault();
        const text = this.$lookup[input.getAttribute("data-snippet-key")];
        if (this.$textArea.value == "") {
          this.$textArea.value = text;
        } else {
          this.$textArea.value = text + "\n\n--------\n" + this.$textArea.value;
        }
      });
    });
  }
}

export default function initCannedSnippetsTextArea() {
  document
    .querySelectorAll("[data-module=canned-snippets-textarea]")
    .forEach(($el) => new PopulateTextOnAddButtonsClick($el).init());
}

export { initCannedSnippetsTextArea };
