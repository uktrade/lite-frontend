var $linkSelectAll = $("#link-select-all");
var $linkDeselectAll = $("#link-deselect-all");
var $checkboxes = $("input:checkbox");

$linkSelectAll.click(function (e) {
  e.preventDefault();
  $checkboxes.prop("checked", true);
  try {
    addCheckedCheckboxesToList();
  } catch (e) {}
  setSelectLinksState();
  return false;
});

$linkDeselectAll.click(function (e) {
  e.preventDefault();
  $checkboxes.prop("checked", false);
  try {
    addCheckedCheckboxesToList();
  } catch (e) {}
  setSelectLinksState();
  return false;
});

$checkboxes.change(function () {
  setSelectLinksState();
});

function setSelectLinksState() {
  enableLink($linkSelectAll);
  enableLink($linkDeselectAll);

  if ($("input:checkbox:checked").length == $checkboxes.length) {
    disableLink($linkSelectAll);
  } else if ($("input:checkbox:checked").length == 0) {
    disableLink($linkDeselectAll);
  }
}

setSelectLinksState();
