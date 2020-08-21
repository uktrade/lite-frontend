import os

from django.urls import reverse_lazy

from conf.base import *


ROOT_URLCONF = "exporter.urls"

INSTALLED_APPS += [
    "exporter.core",
    "svg",
    "lite_forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "exporter.conf.middleware.LoggingMiddleware",
    "exporter.conf.middleware.ProtectAllViewsMiddleware",
    "exporter.conf.middleware.UploadFailedMiddleware",
]

if FEATURE_DEBUG_TOOLBAR_ON:
    index = MIDDLEWARE.index("django.middleware.gzip.GZipMiddleware")
    MIDDLEWARE.insert(index + 1, "debug_toolbar.middleware.DebugToolbarMiddleware")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "exporter/templates")],
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
LOGOUT_URL = f"{AUTHBROKER_URL}/sso/accounts/logout/?next="

AUTHENTICATION_BACKENDS = []

FEEDBACK_URL = env.str("FEEDBACK_URL")
INTERNAL_FRONTEND_URL = env.str("INTERNAL_FRONTEND_URL")
GOOGLE_ANALYTICS_KEY = env.str("GOOGLE_ANALYTICS_KEY")


# static files
SVG_DIRS = [
    os.path.join(BASE_DIR, "exporter/assets/images"),
    os.path.join(BASE_DIR, "shared_assets/lite-frontend/assets/images"),
]

STATIC_ROOT = os.path.join(DATA_DIR, "exporter/assets")
SASS_ROOT = os.path.join(BASE_DIR, "exporter/assets")
SASS_PROCESSOR_ROOT = SASS_ROOT

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "exporter/assets"),
    os.path.join(BASE_DIR, "shared_assets/node_modules/govuk-frontend/govuk/"),
    os.path.join(BASE_DIR, "shared_assets/node_modules/govuk-frontend/govuk/assets/"),
    os.path.join(BASE_DIR, "shared_assets/lite-frontend/"),
)

SASS_PROCESSOR_INCLUDE_DIRS = (os.path.join(BASE_DIR, "exporter/assets"), SASS_ROOT)

LITE_CONTENT_IMPORT_PATH = "lite_content.lite_exporter_frontend.strings"

LITE_EXPORTER_HAWK_KEY = env.str("LITE_EXPORTER_HAWK_KEY")
