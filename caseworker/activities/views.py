from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView

from caseworker.cases.helpers.case import CaseworkerMixin
from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import get_case
from caseworker.cases.views.main import CaseTabsMixin
from caseworker.queues.services import get_queue
from caseworker.activities.forms import NotesAndTimelineForm
from caseworker.activities.mixins import NotesAndTimelineMixin


class NotesAndTimeline(LoginRequiredMixin, CaseTabsMixin, CaseworkerMixin, NotesAndTimelineMixin, FormView):
    template_name = "activities/notes-and-timeline.html"
    form_class = NotesAndTimelineForm

    @cached_property
    def case_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def case(self):
        return get_case(self.request, self.case_id)

    @cached_property
    def queue_id(self):
        return str(self.kwargs["queue_pk"])

    @cached_property
    def queue(self):
        return get_queue(self.request, self.queue_id)

    def get_view_url(self):
        return reverse("cases:activities:notes-and-timeline", kwargs={"pk": self.case_id, "queue_pk": self.queue_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "case": self.case,
            "queue": self.queue,
            "tabs": self.get_standard_application_tabs(),
            "current_tab": "cases:activities:notes-and-timeline",
        }
