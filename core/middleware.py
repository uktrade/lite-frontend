import time

import requests
from s3chunkuploader.file_handler import UploadFailed

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

from lite_content.lite_internal_frontend.strings import cases
from lite_forms.generators import error_page


SESSION_TIMEOUT_KEY = "_session_timeout_seconds_"


class UploadFailedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, UploadFailed):
            return None

        return error_page(request, cases.Manage.Documents.AttachDocuments.FILE_TOO_LARGE)


class SessionTimeoutMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        start = request.session.get(SESSION_TIMEOUT_KEY, time.time())

        timeout = settings.SESSION_EXPIRE_SECONDS

        end = time.time()

        # Expire the session if more than start time + timeout time has occurred
        if end - start > timeout:
            request.session.flush()
            logout(request)
            return redirect(settings.LOGOUT_URL)

        request.session[SESSION_TIMEOUT_KEY] = end

        return self.get_response(request)


class RequestsSessionMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # when making several requests to the same host, the underlying TCP connection will be reused, which can result
        # in a significant performance increase
        request.requests_session = requests.Session()
        return self.get_response(request)
