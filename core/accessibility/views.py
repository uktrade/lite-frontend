from django.views.generic import TemplateView


class AccessibilityStatementView(TemplateView):
    template_name = "accessibility/accessibility.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uri = self.request.build_absolute_uri()
        # Exclude current path and take only complete host name
        context["host"] = uri.rsplit("/", 2)[0]
        return context
