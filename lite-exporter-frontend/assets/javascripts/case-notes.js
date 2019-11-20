const MIN_LENGTH = 1;
const VISIBLE_LENGTH = 1200;
const MAX_LENGTH = 2200;

$(".lite-expandable-textarea-controls").addClass("lite-expandable-textarea-controls--hidden");
$(".case_note-warning").addClass("govuk-hint--hidden");

setTimeout(
	function() {
		$(".lite-expandable-textarea").removeClass("lite-case-note-no-transition");
	}, 400);

$("#case_note").on('input propertychange paste', function() {
	if ($(this).val() != '') {
		$(".lite-expandable-textarea-controls").removeClass("lite-expandable-textarea-controls--hidden");
	} else {
		$(".lite-expandable-textarea-controls").addClass("lite-expandable-textarea-controls--hidden");
	}

	if ($(this).val().length > VISIBLE_LENGTH) {
		$("#case_note-warning").text("You have " + (MAX_LENGTH - $(this).val().length) + " character" + pluralize(MAX_LENGTH - $(this).val().length) + " remaining");
	} else {
		$("#case_note-warning").text("You can enter up to " + MAX_LENGTH + " characters");
	}

	if ($(this).val().length <= MIN_LENGTH) {
		$("#button-post-note").addClass("govuk-button--disabled");
		$("#button-post-note").attr("disabled", true);
	}

	if ($(this).val().length > MAX_LENGTH) {
		$("#case_note-warning").removeClass("govuk-hint");
		$("#case_note-warning").addClass("govuk-error-message");
		$("#case_note-warning").text("You have " + ($(this).val().length - MAX_LENGTH) + " character" + pluralize($(this).val().length - MAX_LENGTH) + " too many");
		$("#button-post-note").addClass("govuk-button--disabled");
		$("#button-post-note").attr("disabled", true);
		$(".lite-expandable-textarea").addClass("lite-expandable-textarea--warning");
	} else {
		$("#case_note-warning").removeClass("govuk-error-message");
		$("#case_note-warning").addClass("govuk-hint");
		$(".lite-expandable-textarea").removeClass("lite-expandable-textarea--warning");
		if ($(this).val().length > MIN_LENGTH) {
			$("#button-post-note").removeClass("govuk-button--disabled");
			$("#button-post-note").attr("disabled", false);
		}
	}
});

$("#case-note-cancel-button").on("click", function() {
	$("#case_note").val("");
	$("#case_note").trigger("input");
	return false;
});
