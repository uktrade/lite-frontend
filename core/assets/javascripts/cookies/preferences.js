import { POLICY_COOKIE_NAME } from "./consts";
import {
    getCookie,
    getDefaultPolicy,
    setPoliciesCookie,
    setPreferencesCookie,
} from "./utils";

class CookiePreferences {
    constructor(formSelector, confirmationSelector, radioButtons) {
        this.formSelector = formSelector;
        this.confirmationSelector = confirmationSelector;
        this.radioButtons = radioButtons;

        this.form = document.querySelector(this.formSelector);
    }

    boolToValue(b) {
        return b ? "on" : "off";
    }

    valueToBool(value) {
        return value === "on";
    }

    getPolicyOrDefault() {
        const cookie = getCookie(POLICY_COOKIE_NAME);
        const policy = getDefaultPolicy();

        if (!cookie) return policy;

        try {
            const parsed = JSON.parse(cookie);

            policy.campaigns = parsed.campaigns || false;
            policy.usage = parsed.usage || false;
            policy.settings = parsed.settings || false;
        } catch (e) {
            return policy;
        }

        return policy;
    }

    initFormValues() {
        const policy = this.getPolicyOrDefault();

        Object.entries(this.radioButtons).forEach(([cookieKey, inputName]) => {
            this.form[inputName].value = this.boolToValue(policy[cookieKey]);
        });
    }

    setPoliciesCookie() {
        const policy = {
            settings: false,
            usage: false,
            campaigns: false,
        };

        Object.entries(this.radioButtons).forEach(([cookieKey, inputName]) => {
            policy[cookieKey] = this.valueToBool(this.form[inputName].value);
        });

        setPoliciesCookie(policy.settings, policy.usage, policy.campaigns);
    }

    displayConfirmation() {
        const confirmationEl = document.querySelector(this.confirmationSelector);

        confirmationEl.style.display = "block";
    }

    bindForm() {
        this.form.addEventListener("submit", (evt) => {
            evt.preventDefault();

            this.setPoliciesCookie();
            setPreferencesCookie();
            this.displayConfirmation();

            window.scrollTo(0, 0);

            return false;
        });
    }
}

const initCookiePreferences = (
    formSelector,
    confirmationSelector,
    radioButtons
) => {
    const cookiePreferences = new CookiePreferences(
        formSelector,
        confirmationSelector,
        radioButtons
    );

    cookiePreferences.initFormValues();
    cookiePreferences.bindForm();
};

export default initCookiePreferences;
