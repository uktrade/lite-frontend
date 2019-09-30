import time

from helpers.seed_data import SeedData


class Timer:
    def __init__(self):
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_time(self):
        return time.time() - self.start

    def print_time(self, context):
        print(f'Timer: {context}: {str(self.get_time())}')


def get_or_create_attr(obj, attr: str, fn):
    """
    Sets the named attribute on the given object to the specified value if it
    doesn't exist, else it'll return the attribute

    setattr(obj, 'attr', fn) is equivalent to ``obj['attr'] = fn''
    """
    if not hasattr(obj, attr):
        setattr(obj, attr, fn)
    return getattr(obj, attr)


def get_lite_client(context, api_url):
    """
    Returns the existing LITE API client, or creates a new one
    """
    return get_or_create_attr(context, 'api', SeedData(api_url=api_url))
