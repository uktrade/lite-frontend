class Customiser {
  constructor($el) {
    this.$el = $el;
    this.spec = JSON.parse(this.$el.getAttribute("data-customiser-spec"));

    this.toggleableElems = {};
    this.localStorageKey = "customiser-preferences-" + this.spec.identifier;
    this.countToggleableElements = 0;
    this.spec.toggleable_elements.forEach((toggleableDetails) => {
      const key = toggleableDetails.key;
      const label = toggleableDetails.label;

      const visible = Boolean(toggleableDetails.default_visible);
      let $elems = $el.querySelectorAll(`[data-customiser-key=${key}]`);
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
    for (const [, value] of Object.entries(this.toggleableElems)) {
      value.elements.forEach((element) => {
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
      let checkbox = `<div class="govuk-checkboxes__item">
          <input type="checkbox" class="customiser__option govuk-checkboxes__input" name="${key}" ${
        value.visible ? "checked" : ""
      } id="customiser__option-${key}">
          <label class="govuk-label govuk-checkboxes__label" for="customiser__option-${key}">${label}</label>
         </div>`;
      customiserOptions += `<li>${checkbox}</li>`;
    }

    const $header = this.$el.querySelector(".customiser__header");
    $header.insertAdjacentHTML(
      "beforeend",
      `
          <details class="customiser__options govuk-details">
            <summary class="govuk-details__summary">
              <span class="govuk-details__summary-text customiser__label"></span>
            </summary>
            <div class="govuk-details__text">
              <p class="customiser__hint"></p>
              <ul class="customiser__choices">
                ${customiserOptions}
              </ul>
            </div>
          </details>
        `
    );

    $header.querySelector(".customiser__label").textContent =
      this.spec.options_label;
    $header.querySelector(".customiser__hint").textContent = this.spec
      .options_hint
      ? this.spec.options_hint
      : "";

    this.$el
      .querySelectorAll("input.customiser__option")
      .forEach(($checkbox) => {
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
