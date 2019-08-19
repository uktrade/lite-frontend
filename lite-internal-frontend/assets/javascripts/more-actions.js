var moreActionsContainer = $( '.app-more-actions__container' )

moreActionsContainer.addClass( 'app-more-actions__container--float' ).addClass( 'app-more-actions__container--hidden' )

// Add
moreActionsContainer.parent().css({'position': 'relative'})
moreActionsContainer.parent().prepend( '<a class="govuk-button app-more-actions__button">Actions</a>' )
moreActionsContainer.children().removeClass('govuk-button')

$('.app-more-actions__button').click(function() {
	$('.app-more-actions__button').next().toggleClass( 'app-more-actions__container--hidden' )
});
