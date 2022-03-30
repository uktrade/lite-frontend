import { PREFERENCES_COOKIE_NAME } from "./consts";
import { getCookie, setPoliciesCookie, setPreferencesCookie } from "./utils";

const COOKIE_PREFERENCES_CLASS_NAME = "cookie-preferences";
const SHOW_BANNER_CLASS_NAME = "app-cookie-banner--show";

class CookieBanner {
  constructor(bannerClassName, acceptAllButtonClassName) {
    this.bannerClassName = bannerClassName;
    this.banner = document.querySelector(`.${this.bannerClassName}`);
    this.acceptAllButtonClassName = acceptAllButtonClassName;
  }

  hasAcceptedCookePreferences() {
    const cookie = getCookie(PREFERENCES_COOKIE_NAME);

    return Boolean(cookie);
  }

  isExcludedPage() {
    const cookiePreferencesEl = document.querySelector(
      `.${COOKIE_PREFERENCES_CLASS_NAME}`
    );

    return Boolean(cookiePreferencesEl);
  }

  shouldDisplay() {
    return (
      Boolean(this.banner) &&
      !this.hasAcceptedCookePreferences() &&
      !this.isExcludedPage()
    );
  }

  acceptAllCookies() {
    setPoliciesCookie(false, true, false);
    setPreferencesCookie();
  }

  hide() {
    this.banner.classList.remove(SHOW_BANNER_CLASS_NAME);
  }

  attachEvents(banner) {
    const button = banner.querySelector(`.${this.acceptAllButtonClassName}`);

    button.addEventListener("click", () => {
      this.acceptAllCookies();
      this.hide();
    });
  }

  display() {
    this.banner.classList.add(SHOW_BANNER_CLASS_NAME);
    this.attachEvents(this.banner);
  }
}

const initCookieBanner = (bannerClassName, acceptAllButtonClassName) => {
  const cookieBanner = new CookieBanner(
    bannerClassName,
    acceptAllButtonClassName
  );

  if (cookieBanner.shouldDisplay()) {
    cookieBanner.display();
  }
};

export default initCookieBanner;
