from health_check.views import MainView
from django.http import HttpResponse
from rest_framework import status


class HealthCheckPingdomView(MainView):
    template_name = "healthcheck/pingdom.xml"

    def render_to_response(self, context, status):
        context["errored_plugins"] = [plugin for plugin in context["plugins"] if plugin.errors]
        context["total_response_time"] = sum([plugin.time_taken for plugin in context["plugins"]])
        return super().render_to_response(context=context, status=status, content_type="text/xml")


class ServiceAvailableHealthCheckView(MainView):
    def get(self, request, *args, **kwargs):
        return self.render_to_response()

    def render_to_response(self):
        return HttpResponse(status.HTTP_200_OK)
