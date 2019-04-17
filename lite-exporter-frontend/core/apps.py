import json

from django.apps import AppConfig

from core import strings


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        with open('lite-content/lite-exporter-frontend/strings.json') as json_file:
            strings.constants = json.load(json_file)
