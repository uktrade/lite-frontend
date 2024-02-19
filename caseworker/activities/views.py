from operator import itemgetter

from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView

from caseworker.cases.helpers.case import CaseworkerMixin
from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import (
    get_activity,
    get_activity_filters,
    get_case,
    post_case_notes,
    get_mentions,
    update_mentions,
)
from caseworker.cases.views.main import CaseTabsMixin
from caseworker.queues.services import get_queue
from caseworker.activities.forms import NotesAndTimelineForm
from core.views import error_page


class NotesAndTimeline(LoginRequiredMixin, CaseTabsMixin, CaseworkerMixin, FormView):
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

    @cached_property
    def mentions(self):
        case_note_mentions = get_mentions(self.request, self.case_id)
        return case_note_mentions.get("results")

    def get_team_filter_url(self, team):
        url = reverse(
            "cases:activities:notes-and-timeline",
            kwargs={
                "pk": self.case_id,
                "queue_pk": self.queue_id,
            },
        )
        return f"{url}?team_id={team['key']}"

    def get_is_filtered_by_team(self, team):
        return self.request.GET.get("team_id") == team["key"]

    def get_team_filters(self):
        activity_filters = get_activity_filters(self.request, self.case_id)
        teams = activity_filters["teams"]
        sorted_teams = sorted(teams, key=itemgetter("value"))
        team_filters = [
            (
                team["key"],
                team["value"],
                self.get_team_filter_url(team),
                self.get_is_filtered_by_team(team),
            )
            for team in sorted_teams
        ]
        return team_filters

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if "mentions" in list(request.GET.keys()):
            my_unread_mentions = [
                {"id": m["id"], "is_accessed": True}
                for m in self.mentions
                if not m["is_accessed"] and m["user"]["id"] == self.request.session["lite_api_user_id"]
            ]
            if my_unread_mentions:
                update_mentions(request, my_unread_mentions)
        return response

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "case": self.case,
            "filtering_by": list(self.request.GET.keys()),
            "queue": self.queue,
            "team_filters": self.get_team_filters(),
            "tabs": self.get_standard_application_tabs(),
            "current_tab": "cases:activities:notes-and-timeline",
            "activities": get_activity(self.request, self.case_id, activity_filters=self.request.GET),
        }

    def form_valid(self, form):
        response, status_code = post_case_notes(self.request, self.case_id, form.cleaned_data)
        if status_code != 201:
            return error_page(self.request, response.get("errors")["text"][0])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:activities:notes-and-timeline", kwargs={"pk": self.case_id, "queue_pk": self.queue_id})
