import {
    PREFERENCES_COOKIE_NAME,
    PREFERENCES_COOKIE_DURATION_DAYS,
    POLICY_COOKIE_NAME,
    POLICY_COOKIE_DURATION_DAYS,
} from "./consts";

const getCookie = (name) => {
    const nameEQ = name + "=";
    const cookies = document.cookie.split(";");
    for (let i = 0, len = cookies.length; i < len; i++) {
        let cookie = cookies[i];
        while (cookie.charAt(0) === " ") {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) === 0) {
            return decodeURIComponent(cookie.substring(nameEQ.length));
        }
    }
    return null;
};

const setCookie = (name, value, options) => {
    if (typeof options === "undefined") {
        options = {};
    }
    let cookieString = name + "=" + value + "; path=/";
    if (options.days) {
        let date = new Date();
        date.setTime(date.getTime() + options.days * 24 * 60 * 60 * 1000);
        cookieString = cookieString + "; expires=" + date.toGMTString();
    }
    if (document.location.protocol === "https:") {
        cookieString = cookieString + "; Secure";
    }
    document.cookie = cookieString;
};

const getDefaultPolicy = () => ({
    essential: true,
    settings: false,
    usage: false,
    campaigns: false,
});

const setPoliciesCookie = (settings, usage, campaigns) => {
    const policy = getDefaultPolicy();
    policy.settings = settings || false;
    policy.usage = usage || false;
    policy.campaigns = campaigns || false;

    const json = JSON.stringify(policy);
    setCookie(POLICY_COOKIE_NAME, json, { days: POLICY_COOKIE_DURATION_DAYS });

    return policy;
};

const setPreferencesCookie = () => {
    setCookie(PREFERENCES_COOKIE_NAME, "true", {
        days: PREFERENCES_COOKIE_DURATION_DAYS,
    });
};

export {
    getCookie,
    setCookie,
    getDefaultPolicy,
    setPoliciesCookie,
    setPreferencesCookie,
};
