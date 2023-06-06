// This function toggles whether the specified element is hidden or displayed.
// It will also toggle the show/hide links appropriately.
//
// elementId: The id of the element to toggle
// startVisible: set this to true to start with the relevant elements visible, or false to start with them hidden.
// showLinkId: id of the link that will show the element and the hide link and hide itself
// hideLinkId: id of the link that will hide the element and itself and display the show link
export function enableToggle(elementId, startVisible, showLinkId, hideLinkId) {
  if (startVisible) {
    enableSwap(elementId, null, showLinkId, hideLinkId);
  } else {
    enableSwap(null, elementId, showLinkId, hideLinkId);
  }
}

// This function swaps the visible element with the hidden element in the document.
// It will also toggle the swap/revert links appropriately.
//
// visibleElementId: The id of the visible element
// hiddenElementId: The id of the hidden element
// swapLinkId: id of the link that will hide the visible element and show the hidden one.
// revertLinkId: id of the link that will revert the two elements to their original state.
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
