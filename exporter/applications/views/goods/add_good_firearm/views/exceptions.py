class ServiceError(Exception):
    def __init__(self, status_code, response, log_message, user_message):
        super().__init__()
        self.status_code = status_code
        self.response = response
        self.log_message = log_message
        self.user_message = user_message
