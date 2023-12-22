from datetime import datetime
from dateutil.parser import parse
from decimal import Decimal

from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from caseworker.queues.forms import CaseAssignmentsAllocateToMeForm
from core.constants import CaseStatusEnum, SecurityClassifiedApprovalsType

from caseworker.cases.helpers.ecju_queries import get_ecju_queries
from caseworker.cases.objects import Slice, Case
from caseworker.cases.services import (
    get_case,
    get_user_case_queues,
    get_case_documents,
    get_case_additional_contacts,
    get_activity_filters,
)
from caseworker.core.constants import GENERATED_DOCUMENT
from caseworker.core.helpers import generate_activity_filters
from caseworker.core.objects import Tab
from caseworker.core.services import get_user_permissions, get_status_properties, get_permissible_statuses
from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import CasePage, ApplicationPage
from caseworker.queues.services import get_queue
from caseworker.users.services import get_gov_user


TAU_ALIAS = "TAU"
LU_ALIAS = "LICENSING_UNIT"
LU_POST_CIRC_FINALISE_QUEUE_ALIAS = "LU_POST_CIRC_FINALISE"
LU_PRE_CIRC_REVIEW_QUEUE_ALIAS = "LU_PRE_CIRC_REVIEW"


class Tabs:
    DETAILS = Tab("details", CasePage.Tabs.DETAILS, "details")
    QUICK_SUMMARY = Tab("quick-summary", CasePage.Tabs.QUICK_SUMMARY, "quick-summary")
    DOCUMENTS = Tab("documents", CasePage.Tabs.DOCUMENTS, "documents")
    LICENCES = Tab("licences", CasePage.Tabs.LICENCES, "licences")
    ADDITIONAL_CONTACTS = Tab("additional-contacts", CasePage.Tabs.ADDITIONAL_CONTACTS, "additional-contacts")
    ECJU_QUERIES = Tab("ecju-queries", CasePage.Tabs.ECJU_QUERIES, "ecju-queries")
    ACTIVITY = Tab("activity", CasePage.Tabs.CASE_NOTES_AND_TIMELINE, "activity")


class Slices:
    SUMMARY = Slice("case/slices/summary.html")
    GOODS = Slice("case/slices/goods.html")
    DESTINATIONS = Slice("case/slices/destinations.html")
    SANCTION_MATCHES = Slice("case/slices/sanctions.html")
    DENIAL_MATCHES = Slice("case/slices/denial-matches.html")
    DELETED_ENTITIES = Slice("case/slices/deleted-entities.html")
    END_USER_DOCUMENTS = Slice("case/slices/end-user-documents.html")
    LOCATIONS = Slice("components/locations.html")
    SECURITY_APPROVALS = Slice("components/security-approvals.html")
    F680_DETAILS = Slice("case/slices/f680-details.html", "F680 details")
    EXHIBITION_DETAILS = Slice("case/slices/exhibition-details.html", "Exhibition details")
    END_USE_DETAILS = Slice("case/slices/end-use-details.html", "End use details")
    ROUTE_OF_GOODS = Slice("case/slices/route-of-goods.html", "Route of goods")
    SUPPORTING_DOCUMENTS = Slice("case/slices/supporting-documents.html", "Supporting documents")
    HMRC_NOTE = Slice("case/slices/hmrc-note.html", "HMRC note")
    END_USER_DETAILS = Slice("case/slices/end-user-details.html", "End user details")
    TEMPORARY_EXPORT_DETAILS = Slice("case/slices/temporary-export-details.html", "Temporary export details")
    OPEN_APP_PARTIES = Slice("case/slices/open-app-parties.html")
    OPEN_GENERAL_LICENCE = Slice("case/slices/open-general-licence.html")
    COMPLIANCE_LICENCES = Slice("case/slices/compliance-licences.html")
    OPEN_LICENCE_RETURNS = Slice("case/slices/open-licence-returns.html", cases.OpenLicenceReturns.TITLE)
    COMPLIANCE_VISITS = Slice("case/slices/compliance-visits.html", "Visit reports")
    COMPLIANCE_VISIT_DETAILS = Slice("case/slices/compliance-visit-details.html")
    FREEDOM_OF_INFORMATION = Slice("case/slices/freedom-of-information.html", "Freedom of Information")
    APPEAL_DETAILS = Slice("case/slices/appeal-details.html", "Appeal")


class CaseworkerMixin:
    @cached_property
    def caseworker(self):
        user, _ = get_gov_user(self.request, str(self.request.session["lite_api_user_id"]))
        return user["user"]

    def is_tau_user(self):
        return self.caseworker["team"]["alias"] == TAU_ALIAS

    def is_lu_user(self):
        return self.caseworker["team"]["alias"] == LU_ALIAS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allocate_to_me_form = (
            None
            if self.queue["is_system_queue"]
            else CaseAssignmentsAllocateToMeForm(
                initial={
                    "queue_id": self.queue_id,
                    "user_id": self.caseworker["id"],
                    "case_id": self.case_id,
                    "return_to": self.request.build_absolute_uri(),
                }
            )
        )
        allocate_and_approve_form = (
            None
            if self.queue["is_system_queue"]
            else CaseAssignmentsAllocateToMeForm(
                auto_id="allocate-approve-%s",
                initial={
                    "queue_id": self.queue_id,
                    "user_id": self.caseworker["id"],
                    "case_id": self.case_id,
                    "return_to": reverse("cases:approve_all", kwargs={"queue_pk": self.queue_id, "pk": self.case_id}),
                },
            )
        )
        return {
            **context,
            "allocate_to_me_form": allocate_to_me_form,
            "allocate_and_approve_form": allocate_and_approve_form,
        }


class CaseView(CaseworkerMixin, TemplateView):
    case_id = None
    case: Case = None
    queue_id = None
    queue = None
    permissions = None
    tabs = None
    slices = None
    additional_context = {}

    def is_only_on_post_circ_queue(self):
        queue_alias = tuple(queue.get("alias") for queue in self.case.queue_details)
        return self.is_lu_user() and queue_alias == (LU_POST_CIRC_FINALISE_QUEUE_ALIAS,)

    def get_goods_summary(self):
        goods_summary = {
            "names": list(),
            "cles": set(),
            "regimes": set(),
            "report_summaries": set(),
            "total_value": 0,
        }
        for good in self.case.goods:
            goods_summary["cles"].update(list(cle["rating"] for cle in good["control_list_entries"]))
            goods_summary["regimes"].update(list(regime["name"] for regime in good["regime_entries"]))
            goods_summary["names"].append(good["good"]["name"])
            if "report_summary_subject" in good and good["report_summary_subject"]:
                report_summary = good["report_summary_subject"]["name"]
                if "report_summary_prefix" in good and good["report_summary_prefix"]:
                    report_summary = f"{good['report_summary_prefix']['name']} {report_summary}"
                goods_summary["report_summaries"].add(report_summary)
            # support legacy report_summary field until it is removed
            elif good.get("report_summary"):
                goods_summary["report_summaries"].add(good["report_summary"])

            goods_summary["total_value"] += Decimal(good["value"])
        return goods_summary

    def get_destination_countries(self):
        destination_countries = set()
        all_parties = self.case.data["ultimate_end_users"] + self.case.data["third_parties"]
        if self.case.data["end_user"]:
            all_parties.append(self.case.data["end_user"])
        if self.case.data["consignee"]:
            all_parties.append(self.case.data["consignee"])
        for party in all_parties:
            destination_countries.add(party["country"]["name"])
        return destination_countries

    def get_context(self):
        if not self.tabs:
            self.tabs = []
        if not self.slices:
            self.slices = []
        open_ecju_queries, closed_ecju_queries = get_ecju_queries(self.request, self.case_id)
        user_assigned_queues = get_user_case_queues(self.request, self.case_id)[0]
        status_props, _ = get_status_properties(self.request, self.case.data["status"]["key"])
        can_set_done = (
            status_props["is_terminal"]
            and self.case.data["status"]["key"] != CaseStatusEnum.APPLICANT_EDITING
            and not self.is_tau_user()
        )
        future_next_review_date = (
            True
            if self.case.next_review_date
            and datetime.strptime(self.case.next_review_date, "%Y-%m-%d ").date() > timezone.localtime().date()
            else False
        )

        context = super().get_context_data()
        default_tab = "quick-summary"
        current_tab = default_tab if self.kwargs["tab"] == "default" else self.kwargs["tab"]

        return {
            **context,
            "tabs": self.tabs if self.tabs else self.get_tabs(),
            "current_tab": current_tab,
            "slices": [Slices.SUMMARY, *self.slices],
            "case": self.case,
            "queue": self.queue,
            "is_system_queue": self.queue["is_system_queue"],
            "goods_summary": self.get_goods_summary(),
            "destination_countries": self.get_destination_countries(),
            "user_assigned_queues": user_assigned_queues,
            "case_documents": get_case_documents(self.request, self.case_id)[0]["documents"],
            "open_ecju_queries": open_ecju_queries,
            "closed_ecju_queries": closed_ecju_queries,
            "additional_contacts": get_case_additional_contacts(self.request, self.case_id),
            "permissions": self.permissions,
            "is_tau_user": self.is_tau_user(),
            "hide_im_done": self.is_tau_user() or self.is_only_on_post_circ_queue(),
            "can_set_done": can_set_done
            and (self.queue["is_system_queue"] and user_assigned_queues)
            or not self.queue["is_system_queue"],
            "generated_document_key": GENERATED_DOCUMENT,
            "permissible_statuses": get_permissible_statuses(self.request, self.case),
            "filters": generate_activity_filters(get_activity_filters(self.request, self.case_id), ApplicationPage),
            "is_terminal": status_props["is_terminal"],
            "is_read_only": status_props["is_read_only"],
            "security_classified_approvals_types": SecurityClassifiedApprovalsType,
            "has_future_next_review_date": future_next_review_date,
            "user": self.caseworker,
            **self.additional_context,
        }

    def _transform_data(self):
        self.case.total_days_elapsed = (timezone.now() - parse(self.case.submitted_at)).days
        if self.case.queue_details:
            for queue_detail in self.case.queue_details:
                queue_detail["days_on_queue_elapsed"] = (timezone.now() - parse(queue_detail["joined_queue_at"])).days

    def get(self, request, **kwargs):
        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)
        self.permissions = get_user_permissions(self.request)

        self._transform_data()

        if hasattr(self, "get_" + self.case.sub_type + "_" + self.case.type):
            getattr(self, "get_" + self.case.sub_type + "_" + self.case.type)()
        else:
            getattr(self, "get_" + self.case.sub_type)()
        return render(request, "case/case.html", self.get_context())
