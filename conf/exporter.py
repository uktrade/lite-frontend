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
    "conf.middleware.LoggingMiddleware",
    "conf.middleware.ProtectAllViewsMiddleware",
    "conf.middleware.UploadFailedMiddleware",
    "django.middleware.gzip.GZipMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "conf.context_processors.export_vars",
            ],
            "builtins": ["core.builtins.custom_tags"],
        },
    },
]


LOGIN_REDIRECT_URL = reverse_lazy("core:home")
LOGOUT_URL = f"{AUTHBROKER_URL}/sso/accounts/logout/?next="

LITE_API_URL = env.str("LITE_API_URL")

PERMISSIONS_FINDER_URL = env.str("PERMISSIONS_FINDER_URL")

TOKEN_SESSION_KEY = env.str("TOKEN_SESSION_KEY")

FEEDBACK_URL = env.str("FEEDBACK_URL")
INTERNAL_FRONTEND_URL = env.str("INTERNAL_FRONTEND_URL")
GOOGLE_ANALYTICS_KEY = env.str("GOOGLE_ANALYTICS_KEY")
