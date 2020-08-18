import os

from conf.base import *


ROOT_URLCONF = "caseworker.urls"

INSTALLED_APPS += [
    "caseworker.core",
    "caseworker.spire",
    "svg",
    "lite_forms",
    "caseworker.letter_templates",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "caseworker.conf.middleware.SessionTimeoutMiddleware",
    # "csp.middleware.CSPMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "caseworker.conf.middleware.ProtectAllViewsMiddleware",
    "caseworker.conf.middleware.LoggingMiddleware",
    "caseworker.conf.middleware.UploadFailedMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "caseworker/templates"), os.path.join(BASE_DIR, "libraries")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "caseworker.conf.context_processors.current_queue",
                "caseworker.conf.context_processors.export_vars",
                "caseworker.conf.context_processors.lite_menu",
            ],
            "builtins": ["core.builtins.custom_tags"],
        },
    },
]


LOGIN_REDIRECT_URL = "/"
LOGOUT_URL = f"{AUTHBROKER_URL}/logout/"

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

# static files
SVG_DIRS = [
    os.path.join(BASE_DIR, "caseworker/assets/images"),
    os.path.join(BASE_DIR, "shared_assets/lite-frontend/assets/images"),
]

STATIC_ROOT = os.path.join(DATA_DIR, "caseworker/assets")
SASS_ROOT = os.path.join(BASE_DIR, "caseworker/assets")
SASS_PROCESSOR_ROOT = SASS_ROOT

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "caseworker/assets"),
    os.path.join(BASE_DIR, "shared_assets/node_modules/govuk-frontend/govuk/"),
    os.path.join(BASE_DIR, "shared_assets/node_modules/govuk-frontend/govuk/assets/"),
    os.path.join(BASE_DIR, "shared_assets/lite-frontend/"),
)

SASS_PROCESSOR_INCLUDE_DIRS = (os.path.join(BASE_DIR, "caseworker/assets"), SASS_ROOT)

LITE_CONTENT_IMPORT_PATH = "lite_content.lite_internal_frontend.strings"

LITE_INTERNAL_HAWK_KEY = env.str("LITE_INTERNAL_HAWK_KEY")
