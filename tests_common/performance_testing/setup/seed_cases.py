from sys import argv

from .common import seed


def seed_cases(seed_data):
    seed_data.add_draft()
    seed_data.submit_standard_application()


if __name__ == '__main__':
    seed(argv, seed_cases)
