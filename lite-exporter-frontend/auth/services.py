import requests

from conf.constants import AUTHENTICATION_URL
from conf.settings import env


def authenticate_exporter_user(json):
    data = requests.post(env('LITE_API_URL') + AUTHENTICATION_URL,
                         json=json)
    return data.json(), data.status_code
