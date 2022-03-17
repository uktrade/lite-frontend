// vendor JS
import { initAll } from 'govuk-frontend';

// our JS
import '../../../core/assets/javascripts/definitions.js';
import '../../../core/assets/javascripts/back-link.js';
import initCookierBanner from '../../../core/assets/javascripts/cookies/banner.js';

// core
// TODO: can't rewrite these as ES6 imports yet as they are used by other templates
import '../../../core/assets/javascripts/select-buttons.js';
import '../../../core/assets/javascripts/filter-bar.js';
import './checkboxes.js';
import './snackbar-hide.js';

// caseworker
import initMenuTooltips from './menu-tooltips.js'
import initQueuesMenu from './queues-menu.js';
import initFlagListExpanders from './flag-expanders.js';
import initReviewGood from './review-good.js';

// vendor styles
import 'tippy.js/dist/tippy.css';

// our styles
import '../styles/styles.scss';

// Hide show destinatios list.
const hideItems = (array) => {
		for (const [index, country] of array.entries()) {
			if (index > 2) {
				country.classList.add('app-hidden--force')
		}
	}
}

(destinationsList = () => {
	const destinationsList = document.getElementsByClassName('destinations__list')

	for (const destinations of destinationsList) {
		const destinationsHtmlCollection = destinations.getElementsByTagName("li")

		if (destinationsHtmlCollection.length > 3) {
			array = [...destinationsHtmlCollection]

			hideItems(array)
			const td = destinations.parentElement
			const link = td.appendChild(document.createElement('a'))
			link.setAttribute("data-hide", true)
			link.innerText = `View all(${destinationsHtmlCollection.length})`
			link.href = ""
			link.className = "destinations__show-all"
			link.addEventListener("click", (e) => {
				e.preventDefault()
				
				const showHideButton = e.currentTarget
				const countryList = [...showHideButton.parentElement.getElementsByTagName("li")]

				if (showHideButton.dataset.hide === "true") {
					for (country of countryList) {
						country.classList.remove('app-hidden--force')
						showHideButton.dataset.hide = false
						showHideButton.innerText = "View less"
					}
				} else {
					hideItems(countryList)
					showHideButton.dataset.hide = true
					showHideButton.innerText = `View all(${countryList.length})`
				}
			})
		}
	}
})()


$(document).ready(function() {
	// init govuk
	initAll();
	// init our JS
	initMenuTooltips();
	initQueuesMenu();
	initFlagListExpanders();
	initReviewGood();
	initCookierBanner("app-cookie-banner", "js-accept-cookie");
});

