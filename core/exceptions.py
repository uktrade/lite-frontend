class PermissionDeniedError(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class ServiceError(Exception):
    def __init__(self, message, status_code, response, log_message, user_message):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
        self.log_message = log_message
        self.user_message = user_message
