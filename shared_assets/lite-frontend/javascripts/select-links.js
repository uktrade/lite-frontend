$linkSelectAll = $( '#link-select-all' );
$linkDeselectAll = $( '#link-deselect-all' );
$checkboxes = $( 'input:checkbox' );

$linkSelectAll.click(function() {
	$checkboxes.prop('checked', true);
	addCheckedCheckboxesToList();
	setSelectLinksState();
	return false;
});

$linkDeselectAll.click(function() {
	$checkboxes.prop('checked', false);
	addCheckedCheckboxesToList();
	setSelectLinksState();
	return false;
});

$checkboxes.change(function() {
	setSelectLinksState();
});

function setSelectLinksState() {
	enableLink($linkSelectAll);
	enableLink($linkDeselectAll);

	if ($( 'input:checkbox:checked' ).length == $checkboxes.length) {
		disableLink($linkSelectAll);
	} else if ($( 'input:checkbox:checked' ).length == 0) {
		disableLink($linkDeselectAll);
	}
}

setSelectLinksState();
