from django.urls import reverse
from django.utils.functional import cached_property

from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import CasePage

from caseworker.cases.objects import Slice
from caseworker.core.objects import Tab
from caseworker.queues.forms import CaseAssignmentsAllocateToMeForm
from caseworker.users.services import get_gov_user


TAU_ALIAS = "TAU"
LU_ALIAS = "LICENSING_UNIT"
FCDO_ALIAS = "FCO"
LU_POST_CIRC_FINALISE_QUEUE_ALIAS = "LU_POST_CIRC_FINALISE"
LU_PRE_CIRC_REVIEW_QUEUE_ALIAS = "LU_PRE_CIRC_REVIEW"


class Tabs:
    DETAILS = Tab("details", CasePage.Tabs.DETAILS, "details")
    QUICK_SUMMARY = Tab("quick-summary", CasePage.Tabs.QUICK_SUMMARY, "quick-summary")
    DOCUMENTS = Tab("documents", CasePage.Tabs.DOCUMENTS, "documents")
    LICENCES = Tab("licences", CasePage.Tabs.LICENCES, "licences")
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

    def is_fcdo_user(self):
        return self.caseworker["team"]["alias"] == FCDO_ALIAS

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
        approve_all_url = reverse("cases:approve_all", kwargs={"queue_pk": self.queue_id, "pk": self.case_id})
        if self.is_fcdo_user():
            approve_all_url = reverse(
                "cases:approve_all_legacy", kwargs={"queue_pk": self.queue_id, "pk": self.case_id}
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
                    "return_to": approve_all_url,
                },
            )
        )
        return {
            **context,
            "allocate_to_me_form": allocate_to_me_form,
            "allocate_and_approve_form": allocate_and_approve_form,
        }


def get_case_detail_url(case_id, case_type, queue_id):
    destinations = {
        "f680_clearance": {"url": "cases:f680:details", "kwargs": {"queue_pk": queue_id, "pk": case_id}},
        "standard": {"url": "cases:case", "kwargs": {"queue_pk": queue_id, "pk": case_id, "tab": "details"}},
    }

    url_name = destinations[case_type]["url"]
    kwargs = destinations[case_type]["kwargs"]
    return reverse(url_name, kwargs=kwargs)
