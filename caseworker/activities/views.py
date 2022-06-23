from django.conf import settings
from django.http import Http404
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import (
    get_activity,
    get_case,
)


class NotesAndTimelineAll(LoginRequiredMixin, TemplateView):
    template_name = "activities/notes-and-timeline-all.html"

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAG_NOTES_TIMELINE_2_0:
            raise Http404("Feature flag disabled")
        return super().dispatch(*args, **kwargs)

    @cached_property
    def case_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def case(self):
        return get_case(self.request, self.case_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {
            **context,
            "activities": get_activity(self.request, self.case_id),
            "case": self.case,
        }
