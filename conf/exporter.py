import os
from urllib.parse import urljoin

from django.urls import reverse_lazy

from conf.base import *


ROOT_URLCONF = "exporter.urls"

MOCK_SSO_ACTIVATE_ENDPOINTS = env.bool("MOCK_SSO_ACTIVATE_ENDPOINTS", False)
MOCK_SSO_USER_EMAIL = env.str("MOCK_SSO_USER_EMAIL", "")
MOCK_SSO_USER_FIRST_NAME = env.str("MOCK_SSO_USER_FIRST_NAME", "")
MOCK_SSO_USER_LAST_NAME = env.str("MOCK_SSO_USER_LAST_NAME", "")

INSTALLED_APPS += [
    "exporter.core",
    "exporter.applications",
    "exporter.organisation",
    "exporter.goods",
    "exporter.f680",
]

if MOCK_SSO_ACTIVATE_ENDPOINTS:
    INSTALLED_APPS += [
        "exporter.mock_sso",
    ]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "exporter", "templates"),
            os.path.join(BASE_DIR, "core", "forms", "templates"),
            os.path.join(BASE_DIR, "core", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "exporter.core.context_processors.export_vars",
            ],
            "builtins": ["core.builtins.custom_tags"],
        },
    },
]

LOGIN_REDIRECT_URL = reverse_lazy("core:home")

LOGOUT_URL = urljoin(AUTHBROKER_URL, "logout")
AUTHBROKER_SCOPE = "openid,email,offline_access"
AUTHBROKER_AUTHORIZATION_URL = urljoin(AUTHBROKER_URL, "authorize")
AUTHBROKER_TOKEN_URL = urljoin(AUTHBROKER_URL, "token")
AUTHBROKER_PROFILE_URL = urljoin(AUTHBROKER_URL, "userinfo")


AUTHENTICATION_BACKENDS = []

FEEDBACK_URL = env.str("FEEDBACK_URL")
INTERNAL_FRONTEND_URL = env.str("INTERNAL_FRONTEND_URL")


# static files
SVG_DIRS = [
    os.path.join(BASE_DIR, "exporter/assets/images"),
    os.path.join(BASE_DIR, "core/assets/images"),
]

STATIC_ROOT = os.path.join(DATA_DIR, "exporter/staticfiles")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "core/assets/"),
    os.path.join(BASE_DIR, "exporter/assets"),
    os.path.join(BASE_DIR, "exporter/assets/built/"),
)

LITE_CONTENT_IMPORT_PATH = "lite_content.lite_exporter_frontend.strings"

LITE_HAWK_ID = env.str("LITE_HAWK_ID", "exporter-frontend")

LITE_HAWK_KEY = env.str("LITE_EXPORTER_HAWK_KEY")

LITE_API_AUTH_HEADER_NAME = "EXPORTER-USER-TOKEN"

FEATURE_FLAG_ONLY_ALLOW_SIEL = True
FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING = env.bool("FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING", False)

SPIRE_URL = "https://www.spire.trade.gov.uk/spire/fox/espire/LOGIN/login"

FEATURE_FLAG_FIREARMS_ENABLED = env.bool("FEATURE_FLAG_FIREARMS_ENABLED", False)

# session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Ensure cache on separate redis DB
CACHEOPS_REDIS = f"{REDIS_URL}/2"

# Application Performance Monitoring
if env.str("ELASTIC_APM_SERVER_URL", ""):
    ELASTIC_APM = {
        "SERVICE_NAME": env.str("ELASTIC_APM_SERVICE_NAME", "lite-exporter-frontend"),
        "SECRET_TOKEN": env.str("ELASTIC_APM_SECRET_TOKEN"),
        "SERVER_URL": env.str("ELASTIC_APM_SERVER_URL"),
        "ENVIRONMENT": env.str("SENTRY_ENVIRONMENT"),
        "DEBUG": DEBUG,
    }
    INSTALLED_APPS.append("elasticapm.contrib.django")

MIDDLEWARE += [
    "exporter.core.middleware.ServiceErrorHandler",
    "exporter.core.middleware.OrganisationRedirectMiddleWare",
]

SURVEY_URL = env.str("SURVEY_URL", "")

# Content Security Policy reporting to sentry.  CSP_REPORT_URI has been deprecated but
# using it here as some browsers still don't support CSP_REPORT_TO which replaces it

CSP_REPORT_URI = env.tuple("EXPORTER_CSP_REPORT_URI", default=("",))
E2E_WAIT_MULTIPLIER = env.int("E2E_WAIT_MULTIPLIER", default=1)
FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS = env.list("FEATURE_FLAG_F680_ALLOWED_ORGANISATIONS", default=[])
FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS = env.list(
    "FEATURE_FLAG_INDETERMINATE_EXPORT_LICENCE_TYPE_ALLOWED_ORGANISATIONS", default=[]
)

ADDITIONAL_LOGGER_CONFIG = '{"core.client": {"handlers": ["stdout"], "level": "DEBUG", "propagate": false}}'
