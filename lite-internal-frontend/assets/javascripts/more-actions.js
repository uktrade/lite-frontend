var moreActionsContainer = $( '.app-more-actions__container' )

moreActionsContainer.addClass( 'app-more-actions__container--float' ).addClass( 'app-more-actions__container--hidden' )
secondaryText = moreActionsContainer.hasClass( 'app-more-actions__container--secondary' ) ? 'govuk-button--secondary' : ''

console.log(secondaryText)

// Add
moreActionsContainer.parent().css({'position': 'relative'})
moreActionsContainer.parent().append( '<a class="govuk-button ' + secondaryText + ' app-more-actions__button">Actions</a>' )
moreActionsContainer.children().removeClass('govuk-button')

$('.app-more-actions__button').click(function() {
	$('.app-more-actions__button').prev().toggleClass( 'app-more-actions__container--hidden' )
});
