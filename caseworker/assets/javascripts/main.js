// vendor JS
import { initAll } from "govuk-frontend";

// our JS
import "../../../core/assets/javascripts/definitions.js";
import "../../../core/assets/javascripts/back-link.js";
import initCannedSnippetsTextArea from "../../../core/assets/javascripts/canned-snippets-textarea.js";
import initCookierBanner from "../../../core/assets/javascripts/cookies/banner.js";
import { gaPushUserID } from "../../../core/assets/javascripts/ga-events.js";

// core
// TODO: can't rewrite these as ES6 imports yet as they are used by other templates
import "./checkboxes.js";
import "./snackbar-hide.js";
// caseworker
import initMenuTooltips from "./menu-tooltips.js";
import initQueuesMenu from "./queues-menu.js";
import initCLEEntries from "./cle-entries.js";
import initRegimeEntries from "./regime-entries.js";
import initDestinationsList from "./show-hide-destinations.js";
import { initCaseNotes, initMentionUsers } from "./case-notes";
import { initExpanders } from "./list-expander";
import { initCustomisers } from "./customiser";
import { initRadioTextArea } from "./radio-populate-textarea.js";
import initSelectAllTables from "./select-all-tables.js";
import { initTableExpanders } from "./table-expander.js";

// vendor styles
import "tippy.js/dist/tippy.css";

// our styles
import "../styles/styles.scss";

// init govuk
initAll();

// init our JS
initMenuTooltips();
initQueuesMenu();
initCLEEntries();
initRegimeEntries();
initCookierBanner("app-cookie-banner", "js-accept-cookie");
initDestinationsList();
initCaseNotes();
initMentionUsers();
initExpanders();
initCustomisers();
initRadioTextArea();
initSelectAllTables();
initTableExpanders();
initCannedSnippetsTextArea();

// Push GA user_id
gaPushUserID();
