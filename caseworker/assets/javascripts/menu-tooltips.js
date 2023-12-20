import tippy from "tippy.js";
import { hideOnEsc, makeFocusable } from "./tippy-plugins";

export default function initMenuTooltips() {
  $("#link-menu").attr("href", "#");

  // deliberately written in vanilla JS not jquery
  const menu = document.getElementById("lite-menu");
  if (!menu) return;

  menu.style.display = "block";

  tippy("#link-menu", {
    content: menu,
    allowHTML: true,
    interactive: true,
    animation: "scale-subtle",
    trigger: "click",
    theme: "light",
    placement: "bottom",
  });

  tippy("*[data-tooltip]", {
    content(reference) {
      return reference.getAttribute("data-tooltip");
    },
    allowHTML: true,
    animation: "scale-subtle",
    interactive: true,
    plugins: [hideOnEsc, makeFocusable],
  });

  tippy(".app-flag--label", {
    content(reference) {
      return reference.getAttribute("data-label");
    },
    interactive: true,
    plugins: [hideOnEsc, makeFocusable],
  });
}
