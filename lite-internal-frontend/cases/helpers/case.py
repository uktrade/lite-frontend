from django.shortcuts import render
from django.views.generic import TemplateView

from cases.objects import Slice
from cases.services import (
    get_case,
    get_user_case_queues,
    get_case_documents,
    get_case_additional_contacts,
    get_activity,
    get_activity_filters,
)
from cases.helpers.ecju_queries import get_ecju_queries
from conf.constants import Statuses, GENERATED_DOCUMENT
from core.objects import Tab, TabCollection
from core.services import get_user_permissions, get_status_properties, get_permissible_statuses
from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import CasePage
from lite_forms.components import FiltersBar, Select, Option, DateInput
from queues.services import get_queue


class Tabs:
    DETAILS = Tab("details", CasePage.Tabs.DETAILS, "details")
    DOCUMENTS = Tab("documents", CasePage.Tabs.DOCUMENTS, "documents")
    ADDITIONAL_CONTACTS = Tab("additional-contacts", CasePage.Tabs.ADDITIONAL_CONTACTS, "additional-contacts")
    ECJU_QUERIES = Tab("ecju-queries", CasePage.Tabs.ECJU_QUERIES, "ecju-queries")
    ACTIVITY = Tab("activity", CasePage.Tabs.CASE_NOTES_AND_TIMELINE, "activity")
    ADVICE = TabCollection(
        "advice",
        CasePage.Tabs.ADVICE_AND_DECISION,
        children=[
            Tab("user-advice", CasePage.Tabs.USER_ADVICE, "user-advice"),
            Tab("team-advice", CasePage.Tabs.TEAM_ADVICE, "team-advice"),
            Tab("final-advice", CasePage.Tabs.FINAL_ADVICE, "final-advice"),
        ],
    )


class Slices:
    SUMMARY = Slice("summary")
    GOODS = Slice("goods")
    DESTINATIONS = Slice("destinations")
    DELETED_ENTITIES = Slice("deleted-entities")
    LOCATIONS = Slice("locations")
    F680_DETAILS = Slice("f680-details", "F680 details")
    EXHIBITION_DETAILS = Slice("exhibition-details", "Exhibition details")
    END_USE_DETAILS = Slice("end-use-details", "End use details")
    ROUTE_OF_GOODS = Slice("route-of-goods", "Route of goods")
    SUPPORTING_DOCUMENTS = Slice("supporting-documents", "Supporting documents")
    GOODS_QUERY = Slice("goods-query", "Query details")
    GOODS_QUERY_RESPONSE = Slice("goods-query-response")
    HMRC_NOTE = Slice("hmrc-note", "HMRC note")
    END_USER_ADVISORY = Slice("end-user-advisory", "End user details")


def get_timeline_filters(request, case_id):
    activity_filters = get_activity_filters(request, case_id)

    def make_options(values):
        return [Option(option["key"], option["value"]) for option in values]

    return FiltersBar(
        [
            Select(
                title=cases.ApplicationPage.ActivityFilters.USER,
                name="user_id",
                options=make_options(activity_filters["users"]),
            ),
            Select(
                title=cases.ApplicationPage.ActivityFilters.TEAM,
                name="team_id",
                options=make_options(activity_filters["teams"]),
            ),
            Select(
                title=cases.ApplicationPage.ActivityFilters.USER_TYPE,
                name="user_type",
                options=make_options(activity_filters["user_types"]),
            ),
            Select(
                title=cases.ApplicationPage.ActivityFilters.ACTIVITY_TYPE,
                name="activity_type",
                options=make_options(activity_filters["activity_types"]),
            ),
            DateInput(title=cases.ApplicationPage.ActivityFilters.DATE_FROM, prefix="from_"),
            DateInput(title=cases.ApplicationPage.ActivityFilters.DATE_TO, prefix="to_"),
        ]
    )


class CaseView(TemplateView):
    case_id = None
    case = None
    queue_id = None
    queue = None
    permissions = None
    tabs = None
    slices = None
    additional_context = {}

    def get_context(self):
        if not self.tabs:
            self.tabs = []
        if not self.slices:
            self.slices = []
        open_ecju_queries, closed_ecju_queries = get_ecju_queries(self.request, self.case_id)
        user_assigned_queues = get_user_case_queues(self.request, self.case_id)[0]
        status_props, _ = get_status_properties(self.request, self.case.data["status"]["key"])
        can_set_done = not status_props["is_terminal"] and self.case.data["status"]["key"] != Statuses.APPLICANT_EDITING
        activity_tab = Tabs.ACTIVITY
        activity_tab.count = "!" if self.case["audit_notification"] else None

        return {
            "tabs": [
                Tabs.DETAILS,
                *self.tabs,
                Tabs.ADDITIONAL_CONTACTS,
                Tabs.ECJU_QUERIES,
                Tabs.DOCUMENTS,
                activity_tab,
            ],
            "current_tab": self.kwargs["tab"],
            "slices": [Slices.SUMMARY, *self.slices],
            "case": self.case,
            "queue": self.queue,
            "is_system_queue": self.queue["is_system_queue"],
            "user_assigned_queues": user_assigned_queues,
            "case_documents": get_case_documents(self.request, self.case_id)[0]["documents"],
            "open_ecju_queries": open_ecju_queries,
            "closed_ecju_queries": closed_ecju_queries,
            "additional_contacts": get_case_additional_contacts(self.request, self.case_id),
            "activity": get_activity(self.request, self.case_id, activity_filters=self.request.GET),
            "permissions": self.permissions,
            "can_set_done": can_set_done
            and (self.queue["is_system_queue"] and user_assigned_queues)
            or not self.queue["is_system_queue"],
            "generated_document_key": GENERATED_DOCUMENT,
            "permissible_statuses": get_permissible_statuses(self.request, self.case["case_type"]),
            "filters": get_timeline_filters(self.request, self.case_id),
            "is_terminal": status_props["is_terminal"],
            "is_read_only": status_props["is_read_only"],
            **self.additional_context,
        }

    def get(self, request, **kwargs):
        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)
        self.permissions = get_user_permissions(self.request)

        if hasattr(self, "get_" + self.case.sub_type + "_" + self.case.type):
            getattr(self, "get_" + self.case.sub_type + "_" + self.case.type)()

        return render(request, "case/case.html", self.get_context())
