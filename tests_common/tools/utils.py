from time import time

from ..api_client.test_helper import build_test_helper


class Timer:
    def __init__(self):
        self.start = time()

    def restart(self):
        self.start = time()

    def get_time(self):
        return time() - self.start

    def print_time(self, context):
        print(f"Timer: {context}: {str(self.get_time())}")


def get_or_create_attr(obj, attr: str, fn):
    """
    Sets the named attribute on the given object to the specified value if it
    doesn't exist, else it'll return the attribute

    setattr(obj, 'attr', fn) is equivalent to ``obj['attr'] = fn''
    """
    if not hasattr(obj, attr):
        setattr(obj, attr, fn)
    return getattr(obj, attr)


def set_timeout_to(self, seconds: int):
    self.implicitly_wait(seconds)


def set_timeout_to_10_seconds(self):
    self.set_timeout_to(10)


# TODO: returns the helper not the client - needs fixing as this could be confusing
def get_lite_client(context, api_client_config):
    return get_or_create_attr(context, "api", build_test_helper(api_client_config["the_client"]))
