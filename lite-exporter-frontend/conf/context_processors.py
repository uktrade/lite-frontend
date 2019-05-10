import os


def export_vars(request):
    data = {'ENVIRONMENT_VARIABLES': dict(os.environ.items())}
    return data
