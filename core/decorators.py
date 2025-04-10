from functools import wraps

from http import HTTPStatus

from requests.exceptions import HTTPError

from django.http import Http404

from .exceptions import ServiceError


def with_logged_in_caseworker(predicate_func):
    @wraps(predicate_func)
    def wrapper(request, *args, **kwargs):
        try:
            _ = request.lite_user
        except AttributeError:
            return False

        return predicate_func(request, *args, **kwargs)

    return wrapper


def expect_status(expected_status, logger_message, error_message, reraise_404=False):
    def check_status(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                response, status_code = f(*args, **kwargs)
            except HTTPError as e:
                raise ServiceError(
                    logger_message,
                    e.response.status_code,
                    e.response,
                    f"{logger_message} - response was: %s - %s",
                    error_message,
                ) from e

            if reraise_404 and status_code == HTTPStatus.NOT_FOUND:
                raise Http404()

            if status_code != expected_status:
                raise ServiceError(
                    logger_message,
                    status_code,
                    response,
                    f"{logger_message} - response was: %s - %s",
                    error_message,
                )
            return response, status_code

        return wrapper

    return check_status
