var buttonSetDestinationFlags = $("#button-edit-destinations-flags")

function setEditDestinationsFlagsAbility() {
	// Disable the edit destinations flags button unless a destinations checkbox is selected
	if ($("input[name='destinations']:checked").length == 0) {
		disableButton(buttonSetDestinationFlags)
	} else {
		enableButton(buttonSetDestinationFlags)
	}
}

setEditDestinationsFlagsAbility();

$("input[type='checkbox']").change(function() {
	setEditDestinationsFlagsAbility();
});

$('.lite-button-checkbox' ).click(function() {
	setEditDestinationsFlagsAbility();
});
