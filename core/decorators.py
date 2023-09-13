from functools import wraps

from requests.exceptions import HTTPError

from .exceptions import ServiceError


def expect_status(expected_status, logger_message, error_message):
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
