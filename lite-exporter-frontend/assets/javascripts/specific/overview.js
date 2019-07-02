function showCancelApplication() {
	LITECommon.Modal.showModal("Are you sure you want to delete this application?", $("#cancel-application").html(), true);
	return false;
};

function showCountries() {
	LITECommon.Modal.showModal("Countries", $("#countries-data").html(), false);
	return false;
};
