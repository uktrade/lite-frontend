from django.apps import AppConfig

from health_check.plugins import plugin_dir


class CoreAppConfig(AppConfig):
    name = "core.dbt_platform_healthcheck"

    def ready(self):
        from .health_checks import SimpleHealthCheckBackend

        plugin_dir.register(SimpleHealthCheckBackend)
