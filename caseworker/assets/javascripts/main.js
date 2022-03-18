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
import initDestinationsList from './show-hide-destinations.js';

// vendor styles
import 'tippy.js/dist/tippy.css';

// our styles
import '../styles/styles.scss';

$(document).ready(function() {
	// init govuk
	initAll();
	// init our JS
	initMenuTooltips();
	initQueuesMenu();
	initFlagListExpanders();
	initReviewGood();
	initCookierBanner("app-cookie-banner", "js-accept-cookie");
	initDestinationsList();
});
