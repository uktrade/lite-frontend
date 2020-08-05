from conf.base import *

# URLs
ROOT_URLCONF = 'caseworker.urls'

# Database
DATABASES = {
    'default': env.db('DATABASE_URL_CASEWORKER')
}
