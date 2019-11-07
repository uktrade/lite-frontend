import time

from ..seed_data import main


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


def set_timeout_to(self, time=0):
    self.implicitly_wait(time)


def set_timeout_to_10_seconds(self):
    self.implicitly_wait(10)


def get_lite_client(context, seed_data_config):
    """
    Returns the existing LITE API client, or creates a new one
    """
    seed_data = main.SeedData(seed_data_config=seed_data_config)
    return get_or_create_attr(context, 'api', seed_data)
