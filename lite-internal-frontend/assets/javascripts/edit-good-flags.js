var buttonGiveAdvice = $("#button-review-goods")
var buttonSetGoodFlags = $("#button-edit-goods-flags")

function setEditGoodsFlagsAbility() {
	// Disable the edit goods flags button unless a goods checkbox is selected
	if ($("input[name='goods']:checked").length == 0) {
		disableButton(buttonGiveAdvice);
		disableButton(buttonSetGoodFlags)
	} else {
		enableButton(buttonGiveAdvice);
		enableButton(buttonSetGoodFlags)
	}
}

setEditGoodsFlagsAbility();

$("input[type='checkbox']").change(function() {
	setEditGoodsFlagsAbility();
});

$('.lite-button-checkbox' ).click(function() {
	setEditGoodsFlagsAbility();
});