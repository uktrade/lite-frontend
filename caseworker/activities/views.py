from operator import itemgetter

from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import (
    get_activity,
    get_activity_filters,
    get_case,
)
from caseworker.queues.services import get_queue


class NotesAndTimeline(LoginRequiredMixin, TemplateView):
    template_name = "activities/notes-and-timeline.html"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {
            **context,
            "activities": get_activity(self.request, self.case_id, activity_filters=self.request.GET),
            "case": self.case,
            "filtering_by": list(self.request.GET.keys()),
            "queue": self.queue,
            "team_filters": self.get_team_filters(),
        }
