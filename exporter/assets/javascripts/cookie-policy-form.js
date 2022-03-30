import initCookiePreferences from "../../../core/assets/javascripts/cookies/preferences.js";

initCookiePreferences(
  "#cookie-preferences-form",
  ".cookie-settings__confirmation",
  {
    usage: "cookies-usage",
  }
);
