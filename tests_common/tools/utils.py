from time import time

from ..api_client.test_helper import TestHelper


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


def build_test_helper(api_client):
    test_helper = TestHelper(api_client)

    if not test_helper.api_client.headers_initialised:
        test_helper.api_client.auth_gov_user()
        test_helper.organisations.setup_org()
        test_helper.organisations.setup_org_for_switching_organisations()
        test_helper.api_client.auth_exporter_user()
        test_helper.api_client.headers_initialised = True

    test_helper.goods.add_good()

    return test_helper
