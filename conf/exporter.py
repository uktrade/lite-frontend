import os

from django.urls import reverse_lazy

from conf.base import *


ROOT_URLCONF = 'exporter.urls'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sass_processor",
    "django.contrib.humanize",
    "exporter.core",
    "svg",
    "lite_forms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "exporter.conf.middleware.LoggingMiddleware",
    "exporter.conf.middleware.ProtectAllViewsMiddleware",
    "exporter.conf.middleware.UploadFailedMiddleware",
    "django.middleware.gzip.GZipMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "exporter/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "exporter.conf.context_processors.export_vars",
            ],
            "builtins": ["core.builtins.custom_tags"],
        },
    },
]


LOGIN_REDIRECT_URL = reverse_lazy("core:home")
LOGOUT_URL = f"{AUTHBROKER_URL}/sso/accounts/logout/?next="

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "exporter.auth.backends.AuthbrokerBackend",
]

PERMISSIONS_FINDER_URL = env.str("PERMISSIONS_FINDER_URL")

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

LITE_CONTENT_IMPORT_PATH = 'lite_content.lite_exporter_frontend.strings'