export function enableToggle(elementId, startVisible, showLinkId, hideLinkId) {
  if (startVisible) {
    enableSwap(elementId, null, showLinkId, hideLinkId);
  } else {
    enableSwap(null, elementId, showLinkId, hideLinkId);
  }
}

export function enableSwap(
  visibleElementId,
  hiddenElementId,
  swapLinkId,
  revertLinkId
) {
  const visibleElement = document.getElementById(visibleElementId);
  const hiddenElement = document.getElementById(hiddenElementId);
  const swapLink = document.getElementById(swapLinkId);
  const revertLink = document.getElementById(revertLinkId);

  function swap() {
    if (visibleElement) visibleElement.classList.add("toggle-hidden");
    if (hiddenElement) hiddenElement.classList.remove("toggle-hidden");
    swapLink.classList.add("toggle-hidden");
    revertLink.classList.remove("toggle-hidden");
  }

  function revert() {
    if (visibleElement) visibleElement.classList.remove("toggle-hidden");
    if (hiddenElement) hiddenElement.classList.add("toggle-hidden");
    swapLink.classList.remove("toggle-hidden");
    revertLink.classList.add("toggle-hidden");
  }

  revert();

  swapLink.addEventListener("click", swap);
  revertLink.addEventListener("click", revert);
}
