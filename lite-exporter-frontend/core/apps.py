import json

from django.apps import AppConfig

from core import lite_strings


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        with open("lite_content/lite-exporter-frontend/strings.json") as json_file:
            lite_strings.constants = json.load(json_file)
