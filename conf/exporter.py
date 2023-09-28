import os
from urllib.parse import urljoin

from django.urls import reverse_lazy

from conf.base import *


ROOT_URLCONF = "exporter.urls"

INSTALLED_APPS += [
    "exporter.core",
    "exporter.applications",
    "exporter.organisation",
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

FEATURE_FLAG_DJANGO_FORMS_REGISTRATION_ENABLED = env.bool("FEATURE_FLAG_DJANGO_FORMS_REGISTRATION_ENABLED", False)

# TODO: Remove this before merging (it will break CI though)
#       Temporarily force authbroker URL to verify CI works
AUTHBROKER_URL = "http://localhost:8300/"

MOCK_SSO_ACTIVATE_ENDPOINTS = env.bool("MOCK_SSO_ACTIVATE_ENDPOINTS", False)
if MOCK_SSO_ACTIVATE_ENDPOINTS:
    INSTALLED_APPS += [
        "core.mock_sso",
    ]
    # When Mocking GovOne SSO core.views.AuthbrokerLogoutView redirect has no prefix:
    LOGOUT_URL = ""

    # MOCK SSO defaults are setup here, since the selenium just calls as via http during e2e
    # (setup can't be placed in conftest, and there is not a separate settings file for tests)
    MOCK_SSO_USER_EMAIL = env.str("MOCK_SSO_USER_EMAIL", "test-uat-user@digital.trade.gov.uk")
    MOCK_SSO_USER_FIRST_NAME = env.str("MOCK_SSO_FIRST_NAME", "LITE")
    MOCK_SSO_USER_LAST_NAME = env.str("MOCK_SSO_USER_EMAIL", "Testing")
    # Secret key is derived from the example data in mock_sso
    MOCK_SSO_SECRET_KEY = env.str(
        "MOCK_SSO_SECRET_KEY", "cd8a0206dee80a90c61bb1251637b4785e5716e13ce4d064fdd932ffc0546682"
    )
else:
    LOGOUT_URL = f"{AUTHBROKER_URL}/logout"

AUTHBROKER_SCOPE = "openid,email,offline_access"

# Setup authbroker URLs in the style of GovUK OneLogin
AUTHBROKER_AUTHORIZATION_URL = urljoin(AUTHBROKER_URL, "/authorize/")
AUTHBROKER_TOKEN_URL = urljoin(AUTHBROKER_URL, "/token/")
AUTHBROKER_PROFILE_URL = urljoin(AUTHBROKER_URL, "/userinfo/")

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

FEATURE_FLAG_ONLY_ALLOW_SIEL = env.bool("FEATURE_FLAG_ONLY_ALLOW_SIEL", True)
FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING = env.bool("FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING", False)
FEATURE_FLAG_APPEALS = env.bool("FEATURE_FLAG_APPEALS", True)

SPIRE_URL = "https://www.spire.trade.gov.uk/spire/fox/espire/LOGIN/login"

FEATURE_FLAG_FIREARMS_ENABLED = env.bool("FEATURE_FLAG_FIREARMS_ENABLED", False)

if "redis" in VCAP_SERVICES:
    REDIS_URL = VCAP_SERVICES["redis"][0]["credentials"]["uri"]
else:
    REDIS_URL = env.str("REDIS_URL", "")

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
