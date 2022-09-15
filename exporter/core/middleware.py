import logging

from django.conf import settings

from lite_forms.generators import error_page

from core.exceptions import ServiceError


logger = logging.getLogger(__name__)


class ServiceErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, ServiceError):
            return None

        logger.error(
            exception.log_message,
            exception.status_code,
            exception.response,
            exc_info=True,
        )
        if settings.DEBUG:
            raise exception
        return error_page(request, exception.user_message)
