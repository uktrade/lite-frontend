// vendor JS
import '../../../core/assets/javascripts/common.js';

import { initAll } from 'govuk-frontend';


// our JS
import '../../../core/assets/javascripts/definitions.js';
import '../../../core/assets/javascripts/back-link.js';
import initAddGood from "./add-good";

// our styles
import '../scss/styles.scss';

// init govuk
$(document).ready(function() {
	initAll();
	initAddGood();
});
