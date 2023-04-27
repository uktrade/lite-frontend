class Customiser {
  constructor($el) {
    this.$el = $el;
    let $headers = this.$el.querySelectorAll("th");
    let $rows = this.$el.querySelectorAll("tr");
    this.customisableColumns = {};
    $headers.forEach(($header, columnIndex, obj) => {
      if ($header.classList.contains("customiser__static")) {
        return;
      }

      const columnIdentifier = $header.textContent;
      let $columns = [];
      $rows.forEach(($row, rowIndex, obj) => {
        const column = $row.querySelectorAll("td")[columnIndex];
        if (column) {
          $columns.push(column);
        }
      });

      let visible = false;
      if ($header.classList.contains("customiser__default")) {
        visible = true;
      }
      this.customisableColumns[columnIdentifier] = {
        headerElement: $headers[columnIndex],
        columnElements: $columns,
        visible: visible,
      };
    });
  }

  init() {
    this.loadPreferences();
    this.showHideColumns();
    this.buildCustomiser();
  }

  showHideColumns() {
    for (const [key, value] of Object.entries(this.customisableColumns)) {
      this.setColumnVisibility(value, value.visible);
    }
  }

  setColumnVisibility(value, visible) {
    value["headerElement"].hidden = !visible;
    value["columnElements"].forEach(($column) => {
      $column.hidden = !visible;
    });
  }

  buildCustomiser() {
    let customiserOptions = ``;
    for (const [key, value] of Object.entries(this.customisableColumns)) {
      let checkbox =
        `<div class="govuk-checkboxes__item"><input type="checkbox" class="customiser__option govuk-checkboxes__input" name="` +
        key +
        `" ` +
        (value.visible ? "checked" : "") +
        ` id="` +
        key +
        `"> <label class="govuk-label govuk-checkboxes__label" for="` +
        key +
        `">` +
        key +
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
    this.customisableColumns[evt.target.name].visible = evt.target.checked;
    this.showHideColumns();
    this.storePreferences();
  }

  storePreferences() {
    let preferences = {};
    for (const [key, value] of Object.entries(this.customisableColumns)) {
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
      if (key in this.customisableColumns) {
        this.customisableColumns[key].visible = value;
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
