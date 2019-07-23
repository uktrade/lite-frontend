import json
import os
import sys

from environ import Env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_FILE):
    Env.read_env(ENV_FILE)

env = Env(
    ALLOWED_HOSTS=(str, ''),
    DEBUG=(bool, False),
    LOG_LEVEL=(str, 'INFO'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=(kaa@ypr5v!x(s=9^f8)o!k#84f_1v@iz31+cq_)8--@kws4b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = json.loads(env('ALLOWED_HOSTS')) if env('ALLOWED_HOSTS') else []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sass_processor',
    'django.contrib.humanize',
    'apply_for_a_licence',
    'core.apps.CoreConfig',
    'libraries.forms',
    'svg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'conf.middleware.ProtectAllViewsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

LOGIN_URL = '/login'

AUTH_USER_MODEL = "core.User"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'libraries')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'conf.context_processors.export_vars',
            ],
            'builtins': ['core.builtins.custom_tags'],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

DATA_DIR = os.path.dirname(BASE_DIR)

SVG_DIRS = [
    os.path.join(BASE_DIR, 'assets/images'),
    os.path.join(BASE_DIR, 'lite-shared-assets/lite-frontend/assets/images'),
]

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(DATA_DIR, 'assets')
SASS_ROOT = os.path.join(BASE_DIR, 'assets')
SASS_PROCESSOR_ROOT = SASS_ROOT

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

SASS_PROCESSOR_INCLUDE_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
    SASS_ROOT
)

SASS_OUTPUT_STYLE = 'compressed'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)

SASS_PROCESSOR_ENABLED = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase'
        }
    }
else:
    DATABASES = {
        'default': env.db()
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '(asctime)(levelname)(message)(filename)(lineno)(threadName)(name)(thread)(created)(process)(processName)(relativeCreated)(module)(funcName)(levelno)(msecs)(pathname)',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': env('LOG_LEVEL').upper(),
        },
    }
}
