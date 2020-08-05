from conf.base import *

# URLs
ROOT_URLCONF = 'internal.urls'

# Database
DATABASES = {
    'default': env.db('DATABASE_URL_INTERNAL')
}
