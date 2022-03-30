var html = `
	<div id="name-pane" class="govuk-inset-text">
		<p class="govuk-hint govuk-!-margin-bottom-1">This will appear to exporters as:</p>
		<p class="govuk-body-l"></p>
	</div>
`;
$("#name").parent().append(html);

function tryShowNameField(object) {
  if ($(object).val().trim().length != 0) {
    var prefix = $("#name").data("licence-name") + " (";
    $("#name-pane .govuk-body-l").text(prefix + $(object).val().trim() + ")");
    $("#name-pane").show();
  } else {
    $("#name-pane").hide();
  }
}

$("#name").on("input propertychange paste", function () {
  tryShowNameField(this);
});

tryShowNameField("#name");
