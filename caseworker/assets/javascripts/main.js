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

// caseworker
import setEnableOnCheckboxes from './checkboxes.js';
import initTooltips from './menu-tooltips.js';
import initQueuesMenu from './queues-menu.js';
import initFlagListExpanders from './flag-expanders.js';
import snackbarHide from './snackbar-hide.js';

// vendor styles
import 'tippy.js/dist/tippy.css';

// our styles
import '../styles/styles.scss';

// init govuk
initAll();

// init our JS
$(document).ready(function() {
	initSelectButtons();
	snackbarHide();
	initTooltips();
	initQueuesMenu();
	initFlagListExpanders();
	setEnableOnCheckboxes();
});
