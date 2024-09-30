from core.feedback.views import FeedbackView
from exporter.core.feedback.forms import ExporterFeedbackForm
from django.urls import reverse_lazy


class ExporterFeedbackView(FeedbackView):
    form_class = ExporterFeedbackForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["help_support_url"] = reverse_lazy("exporter-help-support")
        return kwargs
