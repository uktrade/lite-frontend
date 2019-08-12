function enableButton(button) {
	$(button).prop('disabled', false)
			 .removeClass("govuk-button--disabled")
			 .attr('aria-disabled', false);
}

function disableButton(button) {
	$(button).prop('disabled', true)
			 .addClass("govuk-button--disabled")
			 .attr('aria-disabled', true);
}
