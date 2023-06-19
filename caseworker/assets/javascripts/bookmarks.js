import { enableToggle, enableSwap } from "./toggle";

function setupHiddenBookmarkNameEditField() {
  const bookmarkNameElements = document.querySelectorAll('[id^="bookmark-"]');

  for (const bookmark of bookmarkNameElements) {
    let id = bookmark.id;
    if (id.endsWith("-name")) {
      // Swap between the bookmark name link and edit name field using the edit and cancel buttons
      enableSwap(id, `${id}-edit`, `${id}-edit-button`, `${id}-edit-cancel`);
      // Similarly toggle the Save button on and off
      enableToggle(
        `${id}-save`,
        false,
        `${id}-edit-button`,
        `${id}-edit-cancel`
      );
      // Select the contents of the edit name field when you click edit for ease of renaming
      document
        .getElementById(`${id}-edit-button`)
        .addEventListener("click", () => {
          document.getElementById(`${id}-edit-field`).select();
        });
      // Make the Escape key cancel editing.
      document
        .getElementById(`${id}-edit-field`)
        .addEventListener("keydown", (evt) => {
          if (evt.key === "Escape") {
            document.getElementById(`${id}-edit-cancel`).click();
          }
        });
    }
  }
}

setupHiddenBookmarkNameEditField();
