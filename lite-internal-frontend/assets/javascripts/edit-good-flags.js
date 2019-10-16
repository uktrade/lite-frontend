var buttonGiveAdvice = $("#button-review-goods")
var buttonSetFlags = $("#button-edit-goods-flags")

function setEditGoodsFlagsAbility() {
	// Disable the edit goods flags button unless a goods checkbox is selected
	if ($("input[name='goods']:checked").length == 0) {
		disableButton(buttonGiveAdvice);
		disableButton(buttonSetFlags)
	} else {
		enableButton(buttonGiveAdvice);
		enableButton(buttonSetFlags)
	}
}

setEditGoodsFlagsAbility();

$("input[type='checkbox']").change(function() {
	setEditGoodsFlagsAbility();
});
