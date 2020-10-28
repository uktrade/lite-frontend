from importlib import import_module, reload
import sys

from django.conf import settings
from django.urls import clear_url_caches


def reload_urlconf(urlconfs=[settings.ROOT_URLCONF]):
    clear_url_caches()
    for urlconf in urlconfs:
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
        else:
            import_module(urlconf)
