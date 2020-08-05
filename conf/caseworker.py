import os

from django.urls import reverse_lazy

from conf.base import *


ROOT_URLCONF = 'caseworker.urls'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sass_processor",
    "django.contrib.humanize",
    "core",
    "spire",
    "svg",
    "lite_forms",
    "letter_templates",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "conf.middleware.SessionTimeoutMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "conf.middleware.ProtectAllViewsMiddleware",
    "conf.middleware.LoggingMiddleware",
    "conf.middleware.UploadFailedMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"), os.path.join(BASE_DIR, "libraries")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "conf.context_processors.current_queue",
                "conf.context_processors.export_vars",
                "conf.context_processors.lite_menu",
            ],
            "builtins": ["core.builtins.custom_tags"],
        },
    },
]


LOGIN_REDIRECT_URL = "/"
LOGOUT_URL =  f"{AUTHBROKER_URL}/logout/"

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
