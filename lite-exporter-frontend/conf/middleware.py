from lite_content.lite_exporter_frontend import strings
import logging
import time
import uuid

from django.shortcuts import redirect
from django.urls import resolve

from auth.urls import app_name as auth_app_name
from conf import settings
from lite_forms.generators import error_page
from s3chunkuploader.file_handler import UploadFailed


class ProtectAllViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if resolve(request.path).app_name != auth_app_name and not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        response = self.get_response(request)

        return response


class UploadFailedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, UploadFailed):
            return None
        return error_page(request, strings.Goods.Documents.AttachDocuments.FILE_TOO_LARGE)


class LoggingMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        request.correlation = uuid.uuid4().hex
        data = {
            "message": "liteolog exporter",
            "corrID": request.correlation,
            "type": "http request",
            "method": request.method,
            "url": request.path,
        }
        response = self.get_response(request)
        data["type"] = "http response"
        data["elapsed_time"] = time.time() - start
        logging.info(data)
        return response
