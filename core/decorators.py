import inspect

from functools import wraps

from http import HTTPStatus

from requests.exceptions import HTTPError

from django.http import Http404

from .exceptions import ServiceError


def with_logged_in_caseworker(predicate_func):
    @wraps(predicate_func)
    def wrapper(*args):
        request = args[0]
        try:
            _ = request.lite_user
        except AttributeError:
            return False

        if not request.lite_user:
            return False

        # Some of the rules use multiple predicates and each of them
        # have different number of arguments. If you pass all arguments
        # then some of the earlier predicates fail as they are expecting
        # less number of arguments. For those cases, check the signature
        # and only pass the expected number of arguments
        sig = inspect.signature(predicate_func)
        arguments = args[: len(sig.parameters)]
        return predicate_func(*arguments)

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
