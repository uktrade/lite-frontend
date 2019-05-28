// Show Cancel Application modal
/*$(document).on("click", "a[href*='/delete/']", function(e) {
	var link = $(this).attr("href");
	var draftId = link.substring(link.indexOf("=") + 1, link.lastIndexOf("&"));
	var returnTo = link.substring(link.lastIndexOf("&"));

	LITECommon.Modal.showModal("Are you sure you want to delete this application?", " \
		<p class='govuk-caption-m'>You won't be able to recover it if you delete it.</p> \
		<div class='buttons-row'> \
			<a href='/apply_for_a_licence/" + draftId + "/delete/" + returnTo + "' role='button' draggable='false' class='govuk-button govuk-button--warning govuk-!-margin-right-2'>Delete Application</a> \
			<a onclick='LITECommon.Modal.closeAllModals()' role='button' draggable='false' class='govuk-button govuk-button--secondary'>Cancel</a> \
		</div>", true);

	return false;
});*/
