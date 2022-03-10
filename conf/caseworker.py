import os
from urllib.parse import urljoin

from conf.base import *


ROOT_URLCONF = "caseworker.urls"

INSTALLED_APPS += [
    "rest_framework",
    "caseworker.core",
    "caseworker.spire",
    "caseworker.letter_templates",
    "caseworker.external_data",
    "caseworker.advice",
    "caseworker.tau",
    "caseworker.teams",
    "caseworker.cases",
]

MIDDLEWARE.append("core.middleware.SessionTimeoutMiddleware")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "caseworker/templates"),
            os.path.join(BASE_DIR, "libraries"),
            os.path.join(BASE_DIR, "core/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "caseworker.core.context_processors.current_queue",
                "caseworker.core.context_processors.export_vars",
                "caseworker.core.context_processors.lite_menu",
                "caseworker.core.context_processors.current_user",
            ],
            "builtins": ["core.builtins.custom_tags"],
        },
    },
]


LOGIN_REDIRECT_URL = "/"
LOGOUT_URL = f"{AUTHBROKER_URL}/logout/?next="
AUTHBROKER_SCOPE = "read write"
AUTHBROKER_AUTHORIZATION_URL = urljoin(AUTHBROKER_URL, "/o/authorize/")
AUTHBROKER_TOKEN_URL = urljoin(AUTHBROKER_URL, "/o/token/")
AUTHBROKER_PROFILE_URL = urljoin(AUTHBROKER_URL, "/api/v1/user/me/")

AUTHENTICATION_BACKENDS = []

# The maximum number of parameters that may be received via GET or POST
# before a SuspiciousOperation (TooManyFields) is raised.
# Increased due to potential of selecting all control list entries
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3500

# LITE SPIRE archive API client
FEATURE_SPIRE_SEARCH_ON = env.bool("FEATURE_SPIRE_SEARCH_ON", False)
LITE_SPIRE_ARCHIVE_CLIENT_BASE_URL = env.str("LITE_SPIRE_ARCHIVE_CLIENT_BASE_URL")
LITE_SPIRE_ARCHIVE_CLIENT_HAWK_SECRET = env.str("LITE_SPIRE_ARCHIVE_CLIENT_HAWK_SECRET")
LITE_SPIRE_ARCHIVE_CLIENT_HAWK_SENDER_ID = env.str("LITE_SPIRE_ARCHIVE_CLIENT_HAWK_SENDER_ID", "lite-internal-frontend")
LITE_SPIRE_ARCHIVE_CLIENT_DEFAULT_TIMEOUT = env.int("LITE_SPIRE_ARCHIVE_CLIENT_DEFAULT_TIMEOUT", 2000)
LITE_SPIRE_ARCHIVE_EXAMPLE_ORGANISATION_ID = env.int("LITE_SPIRE_ARCHIVE_EXAMPLE_ORGANISATION_ID")

LITE_API_SEARCH_ENABLED = env.bool("LITE_API_SEARCH_ENABLED", False)

# static files
SVG_DIRS = [
    os.path.join(BASE_DIR, "caseworker/assets/built/"),
    os.path.join(BASE_DIR, "caseworker/assets/images"),
    os.path.join(BASE_DIR, "core/assets/images"),
]

STATIC_ROOT = os.path.join(DATA_DIR, "caseworker/staticfiles")


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "caseworker/assets/built/"),
    os.path.join(BASE_DIR, "caseworker/assets/"),
    os.path.join(BASE_DIR, "core/assets/"),
)

LITE_CONTENT_IMPORT_PATH = "lite_content.lite_internal_frontend.strings"

LITE_HAWK_ID = env.str("LITE_HAWK_ID", "internal-frontend")

LITE_HAWK_KEY = env.str("LITE_INTERNAL_HAWK_KEY")

LITE_API_AUTH_HEADER_NAME = "GOV-USER-TOKEN"

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

FEATURE_PRODUCTPEDIA_ON = env.bool("FEATURE_PRODUCTPEDIA_ON", False)

# Application Performance Monitoring
if env.str("ELASTIC_APM_SERVER_URL", ""):
    ELASTIC_APM = {
        "SERVICE_NAME": env.str("ELASTIC_APM_SERVICE_NAME", "lite-internal-frontend"),
        "SECRET_TOKEN": env.str("ELASTIC_APM_SECRET_TOKEN"),
        "SERVER_URL": env.str("ELASTIC_APM_SERVER_URL"),
        "ENVIRONMENT": env.str("SENTRY_ENVIRONMENT"),
        "DEBUG": DEBUG,
    }
    INSTALLED_APPS.append("elasticapm.contrib.django")

LITE_FEEDBACK_EMAIL = env.str("LITE_FEEDBACK_EMAIL", "")
