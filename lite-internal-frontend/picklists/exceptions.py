class InvalidVarException(Exception):
    """
    InvalidVarException is triggered by the django template engine when it cannot
    find a context variable. This exception should be handled in places where the
    template may use an invalid variable (user entered variables)
    """

    def __mod__(self, missing):
        raise InvalidVarException("Invalid template variable {{ %s }}" % missing)

    def __contains__(self, search):
        if search == "%s":
            return True
        return False
