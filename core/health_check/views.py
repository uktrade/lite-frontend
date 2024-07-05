from hfrom django.http import HttpResponse
from django.http import HttpResponse

class HealthCheckPingdomView(MainView):
    template_name = "healthcheck/pingdom.xml"

    def render_to_response(self, context, status):
        return HttpResponse('')

        #context["errored_plugins"] = [plugin for plugin in context["plugins"] if plugin.errors]
        #context["total_response_time"] = sum([plugin.time_taken for plugin in context["plugins"]])
        #return super().render_to_response(context=context, status=status, content_type="text/xml")
