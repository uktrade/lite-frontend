function showProvisoModal() {
	LITECommon.Modal.showModal('Pick from provisos', $( '#modal-proviso-picker' ).html(), false, true, {maxWidth: '500px'});
	return false;
};

function showAdviceModal() {
	LITECommon.Modal.showModal('Pick from advice', $( '#modal-advice-picker' ).html(), false, true, {maxWidth: '500px'});
	return false;
};

function showPreviewModal(item, type) {
	var title = $(item).data( 'title' );
	var text = $('<div>').text($(item).data( 'text' )).html();
	var lastUpdated = $(item).data( 'last-updated' );

	var previewHtml = '<div class="app-picklist-picker-preview">' +
						  '<div class="app-picklist-picker-preview__text">' +
							  '<p id="picker-preview-text" class="govuk-body-m">' + text + '</p>' +
							  '<p class="govuk-caption-m">Last updated ' + lastUpdated + '</p>' +
						  '</div>' +
						  '<div class="app-picklist-picker-preview__controls">' +
							  '<button id="button-submit-' + type + '" onclick="setTextareaValue(\'' + type + '\');" type="submit" class="govuk-button" data-module="govuk-button">' +
								  'Use template' +
							  '</button>' +
						   '</div>' +
					  '</div>'

	LITECommon.Modal.showModal(title, previewHtml, false, true);
	return false;
};

function setTextareaValue(type) {
	$('#' + type).val($('#picker-preview-text').text()).keyup();
	LITECommon.Modal.closeAllModals();
}
