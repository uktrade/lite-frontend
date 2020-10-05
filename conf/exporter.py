import os
from urllib.parse import urljoin

from django.urls import reverse_lazy

from conf.base import *


ROOT_URLCONF = "exporter.urls"

INSTALLED_APPS += ["exporter.core"]

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
LOGOUT_URL = f"{AUTHBROKER_URL}sso/accounts/logout/?next="
AUTHBROKER_SCOPE = "profile"
AUTHBROKER_AUTHORIZATION_URL = urljoin(AUTHBROKER_URL, "sso/oauth2/authorize/")
AUTHBROKER_TOKEN_URL = urljoin(AUTHBROKER_URL, "sso/oauth2/token/")
AUTHBROKER_PROFILE_URL = urljoin(AUTHBROKER_URL, "sso/oauth2/user-profile/v1/")

AUTHENTICATION_BACKENDS = []

FEEDBACK_URL = env.str("FEEDBACK_URL")
INTERNAL_FRONTEND_URL = env.str("INTERNAL_FRONTEND_URL")
GOOGLE_ANALYTICS_KEY = env.str("GOOGLE_ANALYTICS_KEY")


# static files
SVG_DIRS = [
    os.path.join(BASE_DIR, "dist"),
    os.path.join(BASE_DIR, "exporter/assets/images"),
    os.path.join(BASE_DIR, "core/assets/images"),
]

STATIC_ROOT = os.path.join(DATA_DIR, "exporter/staticfiles")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "dist"),
    os.path.join(BASE_DIR, "core/assets/"),
    os.path.join(BASE_DIR, "exporter/assets"),
    os.path.join(BASE_DIR, "exporter/assets/built/"),
)

LITE_CONTENT_IMPORT_PATH = "lite_content.lite_exporter_frontend.strings"

LITE_HAWK_ID = env.str("LITE_HAWK_ID", "exporter-frontend")

LITE_HAWK_KEY = env.str("LITE_EXPORTER_HAWK_KEY")

LITE_API_AUTH_HEADER_NAME = "EXPORTER-USER-TOKEN"
