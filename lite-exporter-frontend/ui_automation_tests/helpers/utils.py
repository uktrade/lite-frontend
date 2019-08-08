import time


class Timer:
    def __init__(self):
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_time(self):
        return time.time() - self.start

    def print_time(self, context):
        print("timer: "+context+": " + str(self.get_time()))


def get_or_create_attr(obj, attr, fn):
    if not hasattr(obj, attr):
        setattr(obj, attr, fn())
    return getattr(obj, attr)
