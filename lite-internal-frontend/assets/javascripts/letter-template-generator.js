preview = $( '#paragraph-list' );

console.log('wha!');

$( '#standard-advice-list' ).sortable({
	stop: function(event, ui) {
		preview.empty();
		$('.app-letter-generator__picklist-item-text').each(function() {
			preview.append('<p id="' + $(this).parent().data('id') + '">' + $(this).parent().data('text')  + '</p>');
		});
	}
});

$( '.app-letter-generator__picklist-item' ).hover(function() {
	$( '#paragraph-list p:not(#' + $(this).data('id') + ')' ).addClass('fade-out-text');
}, function() {
	$( '.fade-out-text' ).removeClass('fade-out-text');
});
