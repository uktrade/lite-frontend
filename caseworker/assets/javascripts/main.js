// vendor JS
import { initAll } from 'govuk-frontend';
import '@popperjs/core/dist/umd/popper.min.js'
import 'tippy.js';

// our JS
import '../../../core/assets/javascripts/modal.js';
import '../../../core/assets/javascripts/definitions.js';
import '../../../core/assets/javascripts/back-link.js';
import '../../../core/assets/javascripts/helpers.js';
import './generic.js';
import './home.js';

// vendor styles
import 'tippy.js/dist/tippy.css';

// our styles
import '../styles/styles.scss';

initAll();
