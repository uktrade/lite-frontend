var moreActionsContainer = $( '.lite-more-actions__container' )

moreActionsContainer.addClass( 'lite-more-actions__container--float' ).addClass( 'lite-more-actions__container--hidden' )
secondaryText = moreActionsContainer.hasClass( 'lite-more-actions__container--secondary' ) ? 'govuk-button--secondary' : ''

// Add
moreActionsContainer.parent().css({'position': 'relative'})
moreActionsContainer.parent().append( '<a class="govuk-button ' + secondaryText + ' lite-more-actions__button">Actions</a>' )
moreActionsContainer.children().removeClass('govuk-button')

$('.lite-more-actions__button').click(function() {
	$('.lite-more-actions__button').prev().toggleClass( 'lite-more-actions__container--hidden' )
	moreActionsContainer.parent().toggleClass( 'lite-more-actions__parent-disabled-buttons' )
});
