// vendor JS
import { initAll } from 'govuk-frontend';
import 'jquery';

// our JS
import '../../../core/assets/javascripts/modal.js';
import '../../../core/assets/javascripts/definitions.js';
import '../../../core/assets/javascripts/back-link.js';
import '../../../core/assets/javascripts/helpers.js';

// core
import initSelectButtons from '../../../core/assets/javascripts/select-buttons.js';

// TODO: can't rewrite these as ES6 imports yet as they are used by other templates
import '../../../core/assets/javascripts/filter-bar.js';
import './checkboxes.js';
import './snackbar-hide.js';

// caseworker
import initQueuesMenu from './queues-menu.js';
import initFlagListExpanders from './flag-expanders.js';

// vendor styles
import 'tippy.js/dist/tippy.css';

// our styles
import '../styles/styles.scss';

// init govuk
initAll();

// init our JS
$(document).ready(function() {
	initSelectButtons();
	initQueuesMenu();
	initFlagListExpanders();
});
