class Customiser {
  constructor($el) {
    this.$el = $el;
    let $toggleableElems = this.$el.querySelectorAll(".customiser__toggleable");

    this.toggleableElems = {};
    $toggleableElems.forEach(($toggleableElem, index, obj) => {
      if ($toggleableElem.classList.contains("customiser__static")) {
        return;
      }

      const key = $toggleableElem.getAttribute("data-customiser-key");
      const label = $toggleableElem.getAttribute("data-customiser-label");

      let visible = false;
      if ($toggleableElem.classList.contains("customiser__default")) {
        visible = true;
      }
      const additionalElemClass = ".customiser__additional__" + key;
      let additionalElems = $el.querySelectorAll(additionalElemClass);
      this.toggleableElems[key] = {
        element: $toggleableElem,
        additionalElements: additionalElems,
        label: label,
        visible: visible,
      };
    });
  }

  init() {
    this.loadPreferences();
    this.showHideElems();
    this.buildCustomiser();
  }

  showHideElems() {
    for (const [key, value] of Object.entries(this.toggleableElems)) {
      this.setElemVisibility(value.element, value.visible);
      value.additionalElements.forEach((element, index, obj) => {
        this.setElemVisibility(element, value.visible);
      });
    }
  }

  setElemVisibility(element, visible) {
    if (visible) {
      element.classList.remove("customiser__hidden");
    } else {
      element.classList.add("customiser__hidden");
    }
  }

  buildCustomiser() {
    let customiserOptions = ``;
    for (const [key, value] of Object.entries(this.toggleableElems)) {
      const label = value.label;
      let checkbox =
        `<div class="govuk-checkboxes__item"><input type="checkbox" class="customiser__option govuk-checkboxes__input" name="` +
        key +
        `" ` +
        (value.visible ? "checked" : "") +
        ` id="customiser__option__` +
        key +
        `"> <label class="govuk-label govuk-checkboxes__label" for="customiser__option__` +
        key +
        `">` +
        label +
        `</label></div>`;
      customiserOptions += `<li>` + checkbox + `</li>`;
    }
    this.$el
      .querySelector(".customiser__header")
      .insertAdjacentHTML(
        "beforeend",
        `<details class="customiser__options govuk-details lite-mobile-hide"><summary class="govuk-details__summary"><span class="govuk-details__summary-text">Customise table columns</span></summary><div class="govuk-details__text"><ul class="customiser__choices">` +
          customiserOptions +
          `</ul></div></details>`
      );

    this.$el
      .querySelectorAll("input.customiser__option")
      .forEach(($checkbox, index, obj) => {
        $checkbox.addEventListener("click", (evt) =>
          this.handleOptionClick(evt)
        );
      });
    this.$customiserChoices = this.$el.querySelector("ul.customiser__choices");
  }

  handleOptionClick(evt) {
    this.toggleableElems[evt.target.name].visible = evt.target.checked;
    this.showHideElems();
    this.storePreferences();
  }

  storePreferences() {
    let preferences = {};
    for (const [key, value] of Object.entries(this.toggleableElems)) {
      preferences[key] = value.visible;
    }
    window.localStorage.setItem(
      "customiser-preferences",
      JSON.stringify(preferences)
    );
  }

  loadPreferences() {
    if (!window.localStorage.getItem("customiser-preferences")) {
      return;
    }
    const preferences = JSON.parse(
      window.localStorage.getItem("customiser-preferences")
    );
    for (const [key, value] of Object.entries(preferences)) {
      if (key in this.toggleableElems) {
        this.toggleableElems[key].visible = value;
      }
    }
  }
}

const initCustomisers = () => {
  document
    .querySelectorAll(".customiser")
    .forEach(($el) => new Customiser($el).init());
};

export { initCustomisers, Customiser };
