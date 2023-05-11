from operator import itemgetter

from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings

from caseworker.cases.helpers.case import CaseworkerMixin
from core.auth.views import LoginRequiredMixin

from caseworker.cases.services import (
    get_activity,
    get_activity_filters,
    get_case,
    post_case_notes,
)
from caseworker.cases.views.main import CaseTabsMixin
from caseworker.queues.services import get_queue
from caseworker.activities.forms import NotesAndTimelineForm
from lite_forms.generators import error_page


class NotesAndTimeline(LoginRequiredMixin, CaseTabsMixin, CaseworkerMixin, TemplateView):
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
        form = False
        if settings.FEATURE_MENTIONS_ENABLED:
            form = NotesAndTimelineForm(request=self.request)

        return {
            **context,
            "activities": get_activity(self.request, self.case_id, activity_filters=self.request.GET),
            "case": self.case,
            "filtering_by": list(self.request.GET.keys()),
            "queue": self.queue,
            "team_filters": self.get_team_filters(),
            "tabs": self.get_standard_application_tabs(),
            "current_tab": "cases:activities:notes-and-timeline",
            "form": form,
        }

    def clean_post_data(self, post_data):
        for key in post_data:
            # this can't be is for some reason
            if key == "mentions":
                if post_data.get("mentions"):
                    post_data["mentions"] = [{"user": user_id} for user_id in post_data["mentions"]]
            elif key == "is_urgent":
                post_data["is_urgent"] = True
            else:
                post_data[key] = post_data[key][0]
        return post_data

    def post(self, request, **kwargs):
        if "cancel" in request.POST:
            return redirect(
                "cases:activities:notes-and-timeline",
                pk=self.case_id,
                queue_pk=self.queue_id,
            )
        post_data = dict(request.POST).copy()
        post_data = self.clean_post_data(post_data)

        response, status_code = post_case_notes(request, self.case_id, post_data)

        if status_code != 201:
            return error_page(request, response.get("errors")["text"][0])

        return redirect(
            "cases:activities:notes-and-timeline",
            pk=self.case_id,
            queue_pk=self.queue_id,
        )
