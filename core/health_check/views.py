from health_check.views import MainView


class HealthCheckPingdomView(MainView):
    template_name = "healthcheck/pingdom.xml"

    def render_to_response(self, context, status):
        print(context["plugins"])

        context["errored_plugins"] = [plugin for plugin in context["plugins"] if plugin.errors]
        print("------------------------")
        print(context["errored_plugins"])
        context["total_response_time"] = sum([plugin.time_taken for plugin in context["plugins"]])
        return super().render_to_response(context=context, status=status, content_type="text/xml")
