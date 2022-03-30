function showHideInformationDisclosureDetails() {
  var textarea = $("#foi_reason");
  var label = $('label[for="foi_reason"]');

  if ($("input[name='agreed_to_foi']").is(":checked")) {
    label.show();
    textarea.show();
  } else {
    label.hide();
    textarea.hide();
  }
}

$("input[name='agreed_to_foi']").change(function () {
  showHideInformationDisclosureDetails();
});

(function () {
  showHideInformationDisclosureDetails();
})();
