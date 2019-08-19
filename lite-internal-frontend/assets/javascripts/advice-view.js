var buttonGiveAdvice = $("#button-give-advice")

function setGiveAdviceAbility() {
	// Disable the give advice button unless a checkbox is selected
	if ($("input[type='checkbox']:checked").length == 0) {
		disableButton(buttonGiveAdvice)
	} else {
		enableButton(buttonGiveAdvice)
	}
}

setGiveAdviceAbility();

$("input[type='checkbox']").change(function() {
	setGiveAdviceAbility();
});
