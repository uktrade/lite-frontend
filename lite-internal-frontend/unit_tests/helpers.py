from importlib import import_module, reload
import sys

from django.conf import settings
from django.urls import clear_url_caches


def reload_urlconf(urlconf=None):
    clear_url_caches()
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
    else:
        import_module(urlconf)
