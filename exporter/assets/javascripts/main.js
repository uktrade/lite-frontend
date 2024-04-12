// vendor JS
import "../../../core/assets/javascripts/common.js";

import { initAll } from "govuk-frontend";

// our JS
import "../../../core/assets/javascripts/definitions.js";
import "../../../core/assets/javascripts/back-link.js";
import { gaPushUserID } from "../../../core/assets/javascripts/ga-events.js";
import initCookierBanner from "../../../core/assets/javascripts/cookies/banner.js";
import initAddGood from "./add-good";
import initMultiSelects from "./multi-select";
import initAutoCompleteSelects from "./autocomplete-select";
import initStarRating from "../../../core/assets/javascripts/star-rating.js";
// our styles
import "../scss/styles.scss";
// init govuk
$(document).ready(function () {
  initAll();
  initAddGood();
  initMultiSelects();
  initAutoCompleteSelects();
  initCookierBanner("app-cookie-banner", "js-accept-cookie");
  gaPushUserID();
  initStarRating();
});
