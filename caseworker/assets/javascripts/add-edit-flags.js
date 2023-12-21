tippy(".app-radios--flag-colours .govuk-radios__input", {
  content(reference) {
    return reference.getAttribute("data-presentation-value");
  },
  onCreate: (instance) => {
    const element = instance.reference;
    element.setAttribute("tabindex", 0);
  },
  interactive: true,
});

$("#pane_label").addClass("govuk-inset-text");

$("input[type=radio]").change(function () {
  updateLabelVisibility();
});

function updateLabelVisibility() {
  if ($(".govuk-radios__input:checked").val() == "default") {
    $("#pane_label").hide();
  } else {
    $("#pane_label").show();
  }
}

updateLabelVisibility();
