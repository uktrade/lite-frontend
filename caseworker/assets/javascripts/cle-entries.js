import { progressivelyEnhanceMultipleSelectField } from "core/multi-select";

export default function initCLEEntries() {
  const controlListEntriesField = document.getElementById(
    "control_list_entries"
  );
  const controlRationgField = document.getElementById("control_rating");

  if (!(controlListEntriesField || controlRationgField)) return;

  if (controlRationgField) {
    controlRationgField.style.display = "none";

    progressivelyEnhanceMultipleSelectField(controlRationgField);
  }

  // adding place for "rating may need alternative CLC"
  const controlListEntriesTokenFieldInfo = document.createElement("div");
  controlListEntriesField.parentElement.appendChild(
    controlListEntriesTokenFieldInfo
  );

  const controlListEntriesTokenField = progressivelyEnhanceMultipleSelectField(
    controlListEntriesField
  );

  controlListEntriesTokenField.on("change", function (tokenField) {
    const note =
      " may need an alternative control list entry because of its destination";
    const messages = tokenField
      .getItems()
      .filter(function (item) {
        return item.name.match(/[a-zA-Z]$/) !== null;
      })
      .map(function (item) {
        return "<div>" + item.name + note + "</div>";
      });
    if (messages.length > 0) {
      controlListEntriesTokenFieldInfo.innerHTML =
        "<div class='govuk-inset-text'>" + messages.join("") + "</div>";
    } else {
      controlListEntriesTokenFieldInfo.innerHTML = "";
    }
  });
}
