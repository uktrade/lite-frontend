import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";

export default function initRegimeEntries() {
  const regimeEntriesField = document.getElementById(
    "regime_entries"
  );

  if (!(regimeEntriesField)) return;

  // adding place for "rating may need alternative CLC"
  const regimeEntriesTokenFieldInfo = document.createElement("div");
  regimeEntriesField.parentElement.appendChild(
    regimeEntriesTokenFieldInfo
  );

  const regimeEntriesTokenField = progressivelyEnhanceMultipleSelectField(
    regimeEntriesField
  );

  regimeEntriesTokenField.on("change", function (tokenField) {
    const note =
      " may need an alternative regime entry because of its destination";
    const messages = tokenField
      .getItems()
      .filter(function (item) {
        return item.name.match(/[a-zA-Z]$/) !== null;
      })
      .map(function (item) {
        return "<div>" + item.name + note + "</div>";
      });
    if (messages.length > 0) {
      regimeEntriesTokenFieldInfo.innerHTML =
        "<div class='govuk-inset-text'>" + messages.join("") + "</div>";
    } else {
      regimeEntriesTokenFieldInfo.innerHTML = "";
    }
  });
}
