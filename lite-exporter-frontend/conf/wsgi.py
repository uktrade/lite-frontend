import os

from django.core.wsgi import get_wsgi_application
from gunicorn.http.wsgi import Response
from functools import wraps

from whitenoise import WhiteNoise


def wrap_default_headers(func):
    @wraps(func)
    def default_headers(*args, **kwargs):
        # patch wsgi.Response.default_headers to remove the 'Server: ' header from all server responses
        return [header for header in func(*args, **kwargs) if not header.startswith("Server: ")]

    return default_headers


Response.default_headers = wrap_default_headers(Response.default_headers)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

application = get_wsgi_application()
application = WhiteNoise(application)
