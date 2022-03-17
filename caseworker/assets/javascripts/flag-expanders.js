
export default function initFlagListExpanders() {
	const $flagsLists = $('.app-flags--list');
	const chevronSVG = $('#js-chevron-svg').html();

	$flagsLists.each(function() {
		const $flags = $(this).find('.app-flag');

		$flags.each(function (i) {
			if (i > 2) {
				$(this)
					.addClass('app-hidden--force')
					.attr('aria-hidden', true);
			}
		});

		if ($flags.length > 3) {
			const $button = $('<button></button>');
			const $buttonText = $(`<span>3 of ${$flags.length}</span>`);

			$button
				.attr({
					class: 'app-flags__expander',
					type: 'button',
					'aria-label': 'Show more',
				})
				.append(chevronSVG)
				.append($buttonText);

			$(this)
				.parent()
				.append($button);
		}
	});

	const $flagExpanders = $('.app-flags__expander');

	$flagExpanders.on('click keypress', function (e) {
		$(this)
			.prev() // in the flags list preceding the button
			.find('.app-hidden--force')
			.removeClass('app-hidden--force')
			.attr('aria-hidden', false)
			.addClass('app-flag--animate');
		$(this)
			.attr('aria-hidden', true)
			.hide();
	})

}
