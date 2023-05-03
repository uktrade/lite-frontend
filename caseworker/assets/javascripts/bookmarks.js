import { enableToggle, enableSwap } from "./toggle";

enableToggle("bookmarks", false, "show-bookmarks-link", "hide-bookmarks-link");

const bookmarkNameElements = document.querySelectorAll('[id^="bookmark-"]');

for (const bookmark of bookmarkNameElements) {
  let id = bookmark.id;
  if (id.endsWith("-name")) {
    enableSwap(id, `${id}-edit`, `${id}-edit-button`, `${id}-edit-cancel`);
    enableToggle(`${id}-save`, false, `${id}-edit-button`, `${id}-edit-cancel`);
    document
      .getElementById(`${id}-edit-button`)
      .addEventListener("click", () => {
        document.getElementById(`${id}-edit-field`).select();
      });
    document
      .getElementById(`${id}-edit-field`)
      .addEventListener("keydown", (evt) => {
        if (evt.key === "Escape") {
          document.getElementById(`${id}-edit-cancel`).click();
        }
      });
  }
}

document.getElementById("show-bookmarks-link").addEventListener("click", () => {
  document.getElementById("bookmarks").scrollIntoView();
});
