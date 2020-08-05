from conf.base import *

# URLs
ROOT_URLCONF = 'exporter.urls'

# Database
DATABASES = {
    'default': env.db('DATABASE_URL_EXPORTER')
}
