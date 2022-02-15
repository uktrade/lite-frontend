import CookieBanner from "../../../core/assets/javascripts/cookie-banner";

var cookiePolicy = new CookieBanner();
cookiePolicy.bindForm(
  "#cookie-preferences-form",
  ".cookie-settings__confirmation",
  {
    usage: "cookies-usage",
    campaigns: "cookies-campaigns",
    settings: "cookies-settings",
  }
);
