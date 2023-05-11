class Customiser {
  constructor($el) {
    this.$el = $el;
    this.spec = JSON.parse(this.$el.getAttribute("data-customiser-spec"));

    this.toggleableElems = {};
    this.localStorageKey = "customiser-preferences-" + this.spec.identifier;
    this.countToggleableElements = 0;
    this.spec.toggleable_elements.forEach((toggleable_details, index, obj) => {
      const key = toggleable_details.key;
      const label = toggleable_details.label;

      let visible = false;
      if (toggleable_details.hasOwnProperty("default_visible")) {
        visible = toggleable_details.default_visible;
      }
      let $elems = $el.querySelectorAll("[data-customiser-key=" + key + "]");
      this.countToggleableElements += $elems.length;
      this.toggleableElems[key] = {
        elements: $elems,
        label: label,
        visible: visible,
      };
    });
  }

  init() {
    if (this.countToggleableElements == 0) {
      // There's nothing to toggle, so let's not set up the customiser...
      return;
    }
    this.loadPreferences();
    this.showHideElems();
    this.buildCustomiser();
  }

  showHideElems() {
    for (const [key, value] of Object.entries(this.toggleableElems)) {
      value.elements.forEach((element, index, obj) => {
        this.setElemVisibility(element, value.visible);
      });
    }
  }

  setElemVisibility(element, visible) {
    const hiddenClass = "customiser__toggleable--hidden";
    if (visible) {
      element.classList.remove(hiddenClass);
    } else {
      element.classList.add(hiddenClass);
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
        ` id="customiser__option-` +
        key +
        `"> <label class="govuk-label govuk-checkboxes__label" for="customiser__option-` +
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
        `<details class="customiser__options govuk-details lite-mobile-hide"><summary class="govuk-details__summary"><span class="govuk-details__summary-text">` +
          this.spec.options_label +
          `</span></summary><div class="govuk-details__text"><p>` +
          (this.spec.options_hint ? this.spec.options_hint : "") +
          `</p><ul class="customiser__choices">` +
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
    this.fireAnalyticsEvent(evt.target.name, evt.target.checked);
  }

  fireAnalyticsEvent(choice, visible) {
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      dataLayer.push(arguments);
    }
    let eventName = "toggle-" + choice + "-";
    if (this.spec.analytics_prefix) {
      eventName = this.spec.analytics_prefix + "-" + eventName;
    }
    if (visible) {
      eventName += "visible";
    } else {
      eventName += "hidden";
    }
    gtag("event", eventName, {});
  }

  storePreferences() {
    let preferences = {};
    for (const [key, value] of Object.entries(this.toggleableElems)) {
      preferences[key] = value.visible;
    }
    window.localStorage.setItem(
      this.localStorageKey,
      JSON.stringify(preferences)
    );
  }

  loadPreferences() {
    if (!window.localStorage.getItem(this.localStorageKey)) {
      return;
    }
    const preferences = JSON.parse(
      window.localStorage.getItem(this.localStorageKey)
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
