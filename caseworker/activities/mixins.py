from operator import itemgetter
from http import HTTPStatus

from django.utils.functional import cached_property

from caseworker.cases.services import (
    get_activity,
    get_activity_filters,
    get_mentions,
    post_case_notes,
    update_mentions,
)
from lite_forms.generators import error_page


class NotesAndTimelineMixin:

    @cached_property
    def mentions(self):
        case_note_mentions = get_mentions(self.request, self.case_id)
        return case_note_mentions.get("results")

    def get_team_filter_url(self, team):
        return f"{self.get_view_url()}?team_id={team['key']}"

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

    def update_mentions(self):
        if "mentions" in list(self.request.GET.keys()):
            my_unread_mentions = [
                {"id": m["id"], "is_accessed": True}
                for m in self.mentions
                if not m["is_accessed"] and m["user"]["id"] == self.request.session["lite_api_user_id"]
            ]
            if my_unread_mentions:
                update_mentions(self.request, my_unread_mentions)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {
            "filtering_by": list(self.request.GET.keys()),
            "team_filters": self.get_team_filters(),
            "activities": get_activity(self.request, self.case_id, activity_filters=self.request.GET),
            "current_view_url": self.get_view_url(),
        }

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        self.update_mentions()
        return response

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["request"] = self.request
        form_kwargs["view_url"] = self.get_view_url()
        return form_kwargs

    def form_valid(self, form):
        response, status_code = post_case_notes(self.request, self.case_id, form.cleaned_data)
        if status_code != HTTPStatus.CREATED:
            return error_page(self.request, response.get("errors")["text"][0])
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_view_url()
