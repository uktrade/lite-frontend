import os

from environ import Env
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django_log_formatter_ecs import ECSFormatter

from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_FILE):
    Env.read_env(ENV_FILE)

env = Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# django-allow-cidr
ALLOWED_CIDR_NETS = ["10.0.0.0/8"]

WSGI_APPLICATION = "conf.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.humanize",
    "svg",
    "lite_forms",
    "health_check",
    "health_check.cache",
    "health_check.storage",
    "core.api",
    "core.forms",
    "crispy_forms",
    "crispy_forms_gds",
    "core.feedback",
    "formtools",
    "core.cookies",
    "core.goods",
    "django_chunk_upload_handlers",
    "rules.apps.AutodiscoverRulesConfig",
    "extra_views",
]

MIDDLEWARE = [
    "allow_cidr.middleware.AllowCIDRMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.auth.middleware.AuthbrokerClientMiddleware",
    "core.middleware.UploadFailedMiddleware",
    "core.middleware.RequestsSessionMiddleware",
    "core.middleware.NoCacheMiddleware",
    "core.middleware.ValidateReturnToMiddleware",
    "core.middleware.XRobotsTagMiddleware",
    "core.middleware.SessionTimeoutMiddleware",
    "core.middleware.HttpErrorHandlerMiddleware",
]

if not DEBUG:
    MIDDLEWARE += ["core.middleware.AuthBrokerTokenIntrospectionMiddleware"]


FEATURE_CSP_MIDDLEWARE_ENABLED = env.bool("FEATURE_CSP_MIDDLEWARE_ENABLED", True)

if FEATURE_CSP_MIDDLEWARE_ENABLED:
    MIDDLEWARE += [
        "csp.middleware.CSPMiddleware",
    ]

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", True)
SESSION_COOKIE_NAME = env.str("SESSION_COOKIE_NAME", default="exporter")
TOKEN_SESSION_KEY = env.str("TOKEN_SESSION_KEY")

# messages
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CRISPY_ALLOWED_TEMPLATE_PACKS = ["gds"]
CRISPY_TEMPLATE_PACK = "gds"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/assets/"


# Authbroker config
AUTHBROKER_URL = env.str("AUTHBROKER_URL")
AUTHBROKER_CLIENT_ID = env.str("AUTHBROKER_CLIENT_ID")
AUTHBROKER_CLIENT_SECRET = env.str("AUTHBROKER_CLIENT_SECRET")
AUTHBROKER_LOW_SECURITY = env.str("AUTHBROKER_LOW_SECURITY", False)


HAWK_AUTHENTICATION_ENABLED = env.bool("HAWK_AUTHENTICATION_ENABLED", True)
HAWK_RECEIVER_NONCE_EXPIRY_SECONDS = 60

LOGIN_URL = reverse_lazy("auth:login")

DATA_DIR = os.path.dirname(BASE_DIR)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Cache static files
STATICFILES_STORAGE = env.str("STATICFILES_STORAGE", "whitenoise.storage.CompressedManifestStaticFilesStorage")

# File Upload
# https://github.com/uktrade/django-chunk-s3-av-upload-handlers
STREAMING_CHUNK_SIZE = 8192
FILE_UPLOAD_HANDLERS = env.list("FILE_UPLOAD_HANDLERS", default=["core.file_handler.SafeS3FileUploadHandler"])
ACCEPTED_FILE_UPLOAD_MIME_TYPES = env.list(
    "ACCEPTED_FILE_UPLOAD_MIME_TYPES",
    default=(
        # Default file-types supported by LITE are pdf, doc, docx,
        # rtf, jpeg, png and tiff
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/rtf",
        "application/xml",
        "text/xml",
        "text/plain",
        "text/csv",
        "image/jpeg",
        "image/png",
        "image/tiff",
    ),
)
# AV is performed by the API, but these empty settings are required by django-chunk-s3-av-upload-handlers
CLAM_AV_USERNAME = env.str("CLAM_AV_USERNAME", "")
CLAM_AV_PASSWORD = env.str("CLAM_AV_PASSWORD", "")
CLAM_AV_DOMAIN = env.str("CLAM_AV_DOMAIN", "")

# AWS
VCAP_SERVICES = env.json("VCAP_SERVICES", {})

AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL", None)
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
AWS_REGION = env.str("AWS_REGION")
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = env.str("AWS_DEFAULT_ACL", None)
AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL", None)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "{asctime} {levelname} {message}", "style": "{"},
        "ecs_formatter": {"()": ECSFormatter},
    },
    "handlers": {
        "stdout": {"class": "logging.StreamHandler", "formatter": "simple"},
        "ecs": {"class": "logging.StreamHandler", "formatter": "ecs_formatter"},
    },
    "root": {"handlers": ["stdout", "ecs"], "level": env.str("LOG_LEVEL", "info").upper()},
}
additional_logger_config = env.json("ADDITIONAL_LOGGER_CONFIG", default=None)
if additional_logger_config:
    LOGGING["loggers"] = additional_logger_config

# Enable security features in hosted environments

SECURE_HSTS_ENABLED = env.bool("SECURE_HSTS_ENABLED", False)
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365 if SECURE_HSTS_ENABLED else None  # 1 year
SECURE_BROWSER_XSS_FILTER = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG

SESSION_COOKIE_SECURE = not DEBUG
SESSION_EXPIRE_SECONDS = env.int("SESSION_EXPIRE_SECONDS", default=60 * 60)

CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = not DEBUG

X_FRAME_OPTIONS = "SAMEORIGIN"

# Content Security Policy

CSP_DEFAULT_SRC = env.tuple("CSP_DEFAULT_SRC", default=("'self'",))
CSP_STYLE_SRC = env.tuple("CSP_STYLE_SRC", default=("'self'",))
CSP_SCRIPT_SRC = env.tuple("CSP_SCRIPT_SRC", default=("'self'",))
CSP_FONT_SRC = env.tuple("CSP_FONT_SRC", default=("'self'",))
CSP_REPORT_ONLY = env.bool("CSP_REPORT_ONLY", False)
CSP_INCLUDE_NONCE_IN = env.tuple("CSP_INCLUDE_NONCE_IN", default=("script-src",))

if DEBUG:
    import pkg_resources

    try:
        pkg_resources.get_distribution("django_extensions")
    except pkg_resources.DistributionNotFound:
        pass
    else:
        INSTALLED_APPS.append("django_extensions")
    try:
        pkg_resources.get_distribution("django_pdb")
    except pkg_resources.DistributionNotFound:
        pass
    else:
        INSTALLED_APPS.append("django_pdb")
        POST_MORTEM = False
        MIDDLEWARE.append("django_pdb.middleware.PdbMiddleware")

# Sentry
if env.str("SENTRY_DSN", ""):
    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        environment=env.str("SENTRY_ENVIRONMENT"),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )

LITE_API_URL = env.str("LITE_API_URL")

PERMISSIONS_FINDER_URL = env.str("PERMISSIONS_FINDER_URL")

if env.str("DIRECTORY_SSO_API_CLIENT_BASE_URL", ""):
    DIRECTORY_SSO_API_CLIENT_API_KEY = env("DIRECTORY_SSO_API_CLIENT_API_KEY")
    DIRECTORY_SSO_API_CLIENT_BASE_URL = env("DIRECTORY_SSO_API_CLIENT_BASE_URL")
    DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT = 30
    DIRECTORY_SSO_API_CLIENT_SENDER_ID = "lite"


FEATURE_DEBUG_TOOLBAR_ON = env.bool("FEATURE_DEBUG_TOOLBAR_ON", False)

if FEATURE_DEBUG_TOOLBAR_ON:
    INSTALLED_APPS += ["debug_toolbar", "requests_panel"]
    DEBUG_TOOLBAR_PANELS = [
        "requests_panel.panel.RequestsDebugPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

    index = MIDDLEWARE.index("django.middleware.gzip.GZipMiddleware")
    MIDDLEWARE.insert(index + 1, "debug_toolbar.middleware.DebugToolbarMiddleware")

AUTHBROKER_TOKEN_INTROSPECTION_TTL = env.int("AUTHBROKER_TOKEN_INTROSPECTION_TTL", default=60 * 5)

# Gov.uk Notify
NOTIFY_KEY = env.str("NOTIFY_KEY", default="notify-test")
NOTIFY_FEEDBACK_TEMPLATE_ID = env.str("NOTIFY_FEEDBACK_TEMPLATE_ID")
NOTIFY_FEEDBACK_EMAIL = env.str("NOTIFY_FEEDBACK_EMAIL")

# GA/GTM KEY
GTM_ID = env.str("GTM_ID", default="")
