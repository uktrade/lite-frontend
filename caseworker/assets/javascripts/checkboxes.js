function enableControls($selector) {
  $selector.find(".govuk-button").each(function () {
    enableButton($(this));
  });
}

function disableControls($selector) {
  $selector.find(".govuk-button").each(function () {
    disableButton($(this));
  });
}

$("[data-enable-on-checkboxes]").each(function () {
  var $controls = $(this);
  var $parentSelector = $($(this).data("enable-on-checkboxes"));
  var $checkboxesSelector = $(
    $(this).data("enable-on-checkboxes") + " .govuk-checkboxes__input"
  );

  if ($parentSelector.find(":checked").length > 0) {
    enableControls($controls);
  } else {
    disableControls($controls);
  }

  $checkboxesSelector.change(function () {
    if ($parentSelector.find(":checked").length > 0) {
      enableControls($controls);
    } else {
      disableControls($controls);
    }
  });
});
