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
            os.path.join(BASE_DIR, "exporter/templates"),
            os.path.join(BASE_DIR, "core/forms/templates"),
            os.path.join(BASE_DIR, "core/templates"),
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

LOGOUT_URL = f"{AUTHBROKER_URL}/sso/accounts/logout/?next="
AUTHBROKER_SCOPE = "profile"
AUTHBROKER_AUTHORIZATION_URL = urljoin(AUTHBROKER_URL, "sso/oauth2/authorize/")
AUTHBROKER_TOKEN_URL = urljoin(AUTHBROKER_URL, "sso/oauth2/token/")
AUTHBROKER_PROFILE_URL = urljoin(AUTHBROKER_URL, "sso/oauth2/user-profile/v1/")
LOGIN_REDIRECT_URL = reverse_lazy("core:home")

FEATURE_FLAG_GOVUK_SIGNIN_ENABLED = env.bool("FEATURE_FLAG_GOVUK_SIGNIN_ENABLED", False)

if FEATURE_FLAG_GOVUK_SIGNIN_ENABLED:
    LOGOUT_URL = f"{AUTHBROKER_URL}/logout"
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

FEATURE_FLAG_ONLY_ALLOW_SIEL = env.bool("FEATURE_FLAG_ONLY_ALLOW_SIEL", True)
FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING = env.bool("FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING", False)

SPIRE_URL = "https://www.spire.trade.gov.uk/spire/fox/espire/LOGIN/login"

FEATURE_FLAG_FIREARMS_ENABLED = env.bool("FEATURE_FLAG_FIREARMS_ENABLED", False)
FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = env.bool("FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS", False)
FEATURE_FLAG_PRODUCT_2_0 = env.bool("FEATURE_FLAG_PRODUCT_2_0", False)

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
