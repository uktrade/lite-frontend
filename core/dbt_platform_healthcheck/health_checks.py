from health_check.backends import BaseHealthCheckBackend


class SimpleHealthCheckBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = False

    def check_status(self):
        print("API is OK")
        pass

    def identifier(self):
        return self.__class__.__name__
